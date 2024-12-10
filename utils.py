import functools
import itertools
import random as insecure_random
import re
import time

from collections import defaultdict, deque
from copy import copy, deepcopy
from contextlib import contextmanager
from dataclasses import dataclass as basedataclass
from functools import cache
from itertools import count
from math import ceil, floor, inf, lcm, sqrt
from operator import add, eq, ge, gt, itemgetter, lt, le, mul, ne, sub
from queue import PriorityQueue, Queue
from typing import Iterator as BaseIterator
from typing import TypeVar

from frozendict import frozendict
from tqdm import tqdm
import numpy as np


class RequirementException(Exception):
    pass


def require(cond, msg="", *args, _exc=RequirementException, **kw):
    """functionally the same as `assert cond, msg.format(args)` but does not raise an AssertionError to avoid conflicts in tests"""
    if not cond:
        raise _exc(str(msg).format(*args, **kw))


class Sentinel:
    def __init__(self, name, bool=False):
        self.name = name
        self.bool = bool

    def __repr__(self):
        return self.name

    def __bool__(self):
        return self.bool


# used as a default argument to distinguish explicitly passed None vs unpassed
Unset = Sentinel("Unset")


T = TypeVar("T")


class EmptyPeekException(Exception):
    pass


class EmptyReduceException(Exception):
    pass


def timestamp(clock=time.time):
    def inner(item):
        return clock(), item

    return inner


def t(fn):
    """
    Convert a function of N arguments to a function of one N-degree tuple

    Useful with higher order functions that expect single argument function as inputs. This is given as an alternative
    to implementing a star_map, star_for_each, star_flat_map, etc functions for all collections.

    Example:
        def add(a, b):
            return a + b

        pairs = fit([(1, 2), (2, 4), (3, 6)])
        pairs.map(lambda pair: add(pair[0], pair[1]))
        pairs.map(t(add))  # no manual decomposition of the pair, use functions that weren't written for use with HOFs
        pairs.map(t(lambda a, b: a + b))  # use more readable lambdas
    """

    @functools.wraps(fn)
    def tuplized(args):
        return fn(*args)

    return tuplized


def kw(fn):
    """
    Convert a function to take a single dictionary of keyword arguments

    Similar to, but more explicit that `t`
    Example:
         def add(a=0, b=0):
             return a + b

        kwargs = fit([dict(a=5), dict(b=10), dict(a=5, b=10)])
        kwargs.map(lambda d: add(d.get("a", 0), d.get("b", 0)))
        kwargs.map(kw(add))  # no manual decomposition of the dict, use functions that weren't written for use with HOFs
        kwargs.map(kw(lambda a=0, b=0: a + b))  # use more readable lambdas
    """

    @functools.wraps(fn)
    def kwarged(kwargs):
        return fn(**kwargs)

    return kwarged


def fit(iterable):
    """Convert built in types to the corresponding fluent collection type. Unknown collection types are converted to Iterator."""
    if isinstance(iterable, tuple):
        return Tuple(iterable)
    elif isinstance(iterable, list):
        return List(iterable)
    elif isinstance(iterable, (set, frozenset)):
        return Set(iterable)
    elif isinstance(iterable, (dict, frozendict)):
        return Dict(iterable)
    elif isinstance(iterable, (range, Range)):
        return Range(iterable)
    else:
        return Iterator(iterable)


class Iterator(BaseIterator[T]):
    def __init__(self, it=()):
        self._it = iter(it)
        self._next = Unset  # in case we have to read an extra item from the underlying iterator without returning it

    def __next__(self):
        if self._next is Unset:
            return next(self._it)
        else:
            _next, self._next = self._next, Unset
            return _next

    def __iter__(self):
        if self._next is not Unset:
            _next, self._next = self._next, Unset
            yield _next
        yield from self._it

    def __contains__(self, item):
        for e in self:
            if e == item:
                return True
        return False

    def all(self, key=None):
        return all(self if key is None else self.map(key))

    def any(self, key=None):
        return any(self if key is None else self.map(key))

    def apply(self, fn):
        """
        Apply the given function to this iterator. Useful for bridging the gap between fluent and non-fluent operations
        by allowing functions which accept iterables to be used fluently.

        Example:
            # defined before introduction of fluent collections
            def sum(items):
                return reduce(lambda x, y: x + y, items, 0)

            Iterator((1, 2, 3)).apply(sum) == sum((1, 2, 3))

            fluent_iterator.filter(is_even).map(double).map(square).apply(sum)
        """
        return fn(self)

    def apply_and_fit(self, fn):
        return fit(fn(self))

    def batch(self, size, materialize=True):
        """
        :param size: max number of items in each batch. the last batch may have fewer items if there are not enough to
                     fill it
        :param materialize: whether to materialize each batch at a time. If True, `size` + 1 items from the underlying
                            iterator will be materialized at a time. This is required if you want to read multiple
                            batches before processing them
        """
        require(size > 0, "cannot create batches with fewer than 1 item, got {}", size)

        return (
            self.enumerate()
            .apply_and_fit(functools.partial(itertools.groupby, key=t(lambda i, _: i // size)))
            .map(itemgetter(1))
            .map(lambda b: map(itemgetter(1), b))
            .map(Tuple if materialize else Iterator)
        )

    def chain(self, *its):
        return Iterator(itertools.chain(self, *its))

    def combinations(self, r, with_replacement=False):
        combinations = itertools.combinations_with_replacement if with_replacement else itertools.combinations
        return Iterator(combinations(self, r))

    def combine_if(self, cond: bool, combinator: str, *a, **kw):
        if cond:
            return getattr(self, combinator)(*a, **kw)
        return self

    def contains(self, item):
        return item in self

    def count(self, key=None):
        counts = defaultdict(int)
        for k in self if key is None else self.map(key):
            counts[k] += 1
        return Dict(counts)

    def cycle(self):
        return Iterator(itertools.cycle(self))

    def debug(self, fn, every_n=1):
        """
        similar to self.do(fn), but allows skipping elements to avoid spam
        every_n = 0 will never call fn to allow things like:
            iter.debug(print, verbose and 10 or 0)...
        """
        require(every_n >= 0, "every_n must be greater than or equal to 0, but got {}", every_n)

        if every_n == 0:
            return self
        if every_n == 1:

            def gen():
                for item in self:
                    fn(item)
                    yield item

        else:

            def gen():
                i = 0
                for item in self:
                    i += 1
                    if i == every_n:
                        fn(item)
                        i = 0
                    yield item

        return Iterator(gen())

    def dict(self):
        """requires that items be 2-tuples"""
        return Dict(self)

    def distinct(self, key=None):
        if key is None:

            def gen():
                seen = set()
                for item in self:
                    if item not in seen:
                        seen.add(item)
                        yield item

        else:

            def gen():
                seen = set()
                for item in self:
                    item_key = key(item)
                    if item_key not in seen:
                        seen.add(item_key)
                        yield item

        return Iterator(gen())

    def do(self, fn=None, tween_fn=None):
        """
        equivalent to self.map(lambda e: fn(e); return e) if that were possible in python
        if tween_fn is present, it is called on sequential pairs of elements between when fn is called on each
        """

        def gen():
            if fn is None and tween_fn is None:
                for item in self:
                    yield item
            elif fn is None:
                for f, s in self.sliding(2):
                    tween_fn(f, s)
                    yield f
                try:
                    yield s
                except UnboundLocalError:
                    pass
            elif tween_fn is None:
                for item in self:
                    fn(item)
                    yield item
            else:
                for f, s in self.sliding(2):
                    fn(f)
                    yield f
                    tween_fn(f, s)
                try:
                    fn(s)
                    yield s
                except UnboundLocalError:
                    pass

        return Iterator(gen())

    def drop(self, n):
        """
        equivalent to self[n:]
        if n < 0, consumes the iterator and materializes up to -n elements in memory at a time
        """
        if n >= 0:
            for _ in range(n):
                try:
                    self.next()
                except StopIteration:
                    break
            return self
        else:
            # this logic is similar to sliding but we can't actually use sliding in case -n > self.size() since sliding
            # won't output windows unless they have the full number of elements
            window = self.take(-n).list()
            while self.has_next():
                window.pop(0)
                window.append(self.next())
            return Iterator(window)

    def drop_while(self, pred):
        return Iterator(itertools.dropwhile(pred, self))

    def enumerate(self, start=0):
        return Iterator(enumerate(self, start))

    def every_n(self, n, start=0):
        require(n > 0, n)
        return self.enumerate(start).filter(t(lambda i, _: i % n == 0)).map(itemgetter(1))

    def filter(self, pred=None, do_with_discarded=None):
        if pred is None and do_with_discarded is None:

            def gen():
                for item in self:
                    if item:
                        yield item

        elif do_with_discarded is None:

            def gen():
                for item in self:
                    if pred(item):
                        yield item

        elif pred is None:

            def gen():
                for item in self:
                    if item:
                        yield item
                    else:
                        do_with_discarded(item)

        else:

            def gen():
                for item in self:
                    if pred(item):
                        yield item
                    else:
                        do_with_discarded(item)

        return Iterator(gen())

    def first(self, pred=Unset, default=Unset):
        try:
            if pred is Unset:
                return self.next()
            else:
                return self.filter(pred).next()
        except StopIteration:
            if default is Unset:
                raise
            else:
                return default

    def flat_map(self, fn):
        if fn is None:

            def gen():
                for item in self:
                    yield from item

        else:

            def gen():
                for item in self:
                    yield from fn(item)

        return Iterator(gen())

    def flatten(self):
        """requires that items are iterable"""
        return self.flat_map(None)

    def fold(self, initial, fn):
        acc = initial
        for item in self:
            acc = fn(acc, item)
        return acc

    def for_each(self, fn=None, tween_fn=None):
        # shortcut for empty iterator so that later code can assume we have at least one element
        if not self.has_next():
            return

        if fn is None and tween_fn is None:
            for item in self:
                pass
        elif fn is None:
            for f, s in self.sliding(2):
                tween_fn(f, s)
        elif tween_fn is None:
            for item in self:
                fn(item)
        else:
            s = self.next()  # guaranteed safe because we checked has_next above
            for item in self:
                f, s = s, item
                fn(f)
                tween_fn(f, s)
            try:
                fn(item)
            except UnboundLocalError:
                # item is only unbound if self had exactly one element, in which case s is that element
                fn(s)

    def group_by(self, key=None):
        out = Dict()
        if key is None:
            for item in self:
                out.setdefault(item, List()).append(item)
        else:
            for item in self:
                out.setdefault(key(item), List()).append(item)
        return out

    def has_next(self):
        try:
            if self._next is Unset:
                self._next = next(self._it)
            return True
        except StopIteration:
            return False

    def intersperse(self, item):
        def gen():
            if self.has_next():
                yield self.next()
                for i in self:
                    yield item
                    yield i

        return Iterator(gen())

    def iter(self):
        # unlike the other collections, there's no need to create a copy here since the underlying iterator can only be
        # consumed once anyway
        return self

    def last(self, pred=Unset, default=Unset):
        if pred is not Unset:
            self = self.filter(pred)
        if self.has_next():
            for item in self:
                pass
            return item
        else:
            if default is Unset:
                raise StopIteration
            else:
                return default

    def list(self):
        return List(self)

    def map(self, fn):
        return Iterator(map(fn, self))

    def map_to_keys(self, fn):
        """Create a dictionary using the items in self as values and the given mapper applied to each as the corresponding key"""
        return self.map_to_pairs(fn).map(reversed).dict()

    def map_to_pairs(self, fn):
        """Map to pairs of (item, fn(item))"""
        return self.map(lambda item: (item, fn(item)))

    def map_to_values(self, fn):
        """Create a dictionary using the items in self as keys and the given mapper applied to each as the corresponding value"""
        return self.map_to_pairs(fn).dict()

    def max(self, key=None, default=Unset):
        if not self.has_next() and default is not Unset:
            return default
        return max(self) if key is None else max(self, key=key)

    def min(self, key=None, default=Unset):
        if not self.has_next() and default is not Unset:
            return default
        return min(self) if key is None else min(self, key=key)

    def mins(self, key=None):
        """
        Filters self to only values equal to the minimum value

        Consumes the entire iterator, materializing len(return) at a time.
        """
        if not self.has_next():
            return List()

        if key is None:
            mins = List([self.next()])
            mink = mins[0]
            for item in self:
                if item < mink:
                    mink = item
                    mins = List([item])
                elif item == mink:
                    mins.append(item)
        else:
            mins = List([self.next()])
            mink = key(mins[0])
            for item, itemk in self.map_to_pairs(key):
                if itemk < mink:
                    mink = itemk
                    mins = List([item])
                elif itemk == mink:
                    mins.append(item)
        return mins

    def min_max(self, key=None, default=Unset):
        if not self.has_next():
            if default is Unset:
                raise ValueError("min_max() arg is an empty sequence")
            else:
                return default
        if key is None:
            min = max = self.next()
            for item in self:
                if item < min:
                    min = item
                elif item > max:
                    max = item
            return min, max
        else:
            min = max = self.next()
            min_key = max_key = key(min)
            for item in self:
                item_key = key(item)
                if item_key < min_key:
                    min = item
                    min_key = item_key
                elif item_key > max_key:
                    max = item
                    max_key = item_key
            return min, max

    def next(self):
        return next(self)

    def only(self, pred=Unset):
        if pred is not Unset:
            self = self.filter(pred)
        require(self.has_next(), "no item found", _exc=ValueError)
        item = self.next()
        require(not self.has_next(), "too many items found", _exc=ValueError)
        return item

    def partition(self, pred):
        t, f = self.tee()
        # TODO: predicate is called twice for each item, see if we can avoid that
        return t.filter(pred), f.filter(lambda e: not pred(e))

    def peek(self, default=Unset):
        if self.has_next():
            return self._next
        elif default is not Unset:
            return default
        else:
            raise EmptyPeekException()

    def permutations(self, r=None):
        return Iterator(itertools.permutations(self, r))

    def powerset(self):
        items = self.tuple()
        return fit(range(len(items) + 1)).flat_map(items.combinations)

    def product(self, *its, repeat=1):
        return Iterator(itertools.product(self, *its, repeat=repeat))

    def reduce(self, fn, default=Unset):
        try:
            return self.fold(self.next(), fn)
        except StopIteration:
            if default is Unset:
                raise EmptyReduceException("reduce on empty iterator")
            return default

    def repeat(self, n=None):
        items = self.list()
        if n is None:
            return Iterator(itertools.repeat(items)).flatten()
        else:
            return Iterator(itertools.repeat(items, n)).flatten()

    def set(self):
        return Set(self)

    def size(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def sliding(self, size, step=1):
        """
        All windows are guaranteed to have exactly size items
        When step > 1 or size > len(self), may truncate the end of the iterator if a window cannot be filled
        """
        require(size > 0, "window size must be strictly positive, got {}", size)
        require(step > 0, "step size must be strictly positive, got {}", step)

        def gen():
            window = List(self.take(size))
            while window.size() == size:
                yield window
                # it's important to extend before dropping in case step > size
                window = window.extended(self.take(step)).drop(step)

        return Iterator(gen())

    def sliding_by_timestamp(self, size, step=1, stamp=timestamp(time.time)):
        """
        take a sliding window across time instead of index.

        - windows are not guaranteed to have the same number of elements (or even any elements)
        - timestamps are required to be monotonic, non-monotonic timestamps may cause an infinite iterator
        - does not truncate the end for lack of elements like index based sliding
        - may skip elements if abs(step) > size
        - step may be negative

        stamp argument is a function that maps items to (ts, item) pairs allowing timestamps to be extracted from
        elements rather than using the time at which they are pulled from the iterator.
        """
        require(size > 0, "window size must be strictly positive, got {}", size)
        require(step != 0, "step size must not be zero")
        if not self.has_next():
            return self
        it = self.map(stamp)
        if step < 0:
            # for negative steps, it's easiest to just flip the signs so that we can use the same comparison operations
            step *= -1
            it = it.map(t(lambda ts, item: (-ts, item)))

        def gen():
            start = it.peek()[0]  # safe because has_next has already returned True
            window = fit([])
            while True:
                # it's important to extend before dropping in case abs(step) > size
                window = window.extended(it.take_while(t(lambda ts, item: ts < start + size))).drop_while(
                    t(lambda ts, item: ts < start)
                )
                yield window.map(itemgetter(1))
                start += step
                if not it.has_next():
                    break

        return Iterator(gen())

    def take(self, n):
        """
        equivalent to self[:n]
        if n < 0, consumes the iterator and materializes up to n elements in memory at a time
        """
        if n >= 0:

            def gen():
                for _ in range(n):
                    try:
                        yield self.next()
                    except StopIteration:
                        break

        else:

            def gen():
                try:
                    windows = self.sliding(-n)
                    _next = windows.next()[0]
                    while windows.has_next():
                        yield _next
                        _next = windows.next()[0]
                except StopIteration:
                    pass

        return Iterator(gen())

    def take_while(self, pred=None):
        # not implemented using itertools.takewhile because it discards the first non-passing element
        if pred is None:

            def gen():
                for item in self:
                    if item:
                        yield item
                    else:
                        self._next = item
                        break

        else:

            def gen():
                for item in self:
                    if pred(item):
                        yield item
                    else:
                        self._next = item
                        break

        return Iterator(gen())

    def tee(self, n=2):
        return tuple(map(Iterator, itertools.tee(self, n)))

    def timestamp(self, clock=time.time):
        """
        like enumerate, but pairs each element with the timestamp at which it was yielded from self.
        peek (and any functions that use peeking behavior internally) will fix the timestamp for that item.
        """
        return self.map(timestamp(clock))

    def tqdm(self, *a, **kw):
        return Iterator(tqdm(self, *a, **kw))

    def transpose(self):
        """items must be iterables. If they have different lengths, the longer iterables will be truncated."""
        return fit(zip(*self)).map(Tuple)

    def tuple(self):
        return Tuple(self)

    unzip = transpose

    def zip(self, *others):
        return Iterator(zip(self, *others))

    def zip_append(self, *others):
        # like zip, but expects that items in self are iterable and adds the zipped items to those iterables
        # e.g.
        #   fit([(1, 2), (3, 4)].zip_append((5, 6)) == [(1, 2, 5), (3, 4, 6)]
        return Iterator(zip(*self.unzip(), *others))

    def zip_into(self, other):
        # like zip_append but expects that items in self are singular and items in others are iterable
        # e.g.
        #   fit([1, 2]).zip_into(fit([(3, 4), (5, 6)])) == [(1, 3, 4), (2, 5, 6)]
        return Iterator(zip(self, *other.unzip()))


class Tuple(tuple):
    def __add__(self, other):
        return Tuple(super().__add__(other))

    def __mul__(self, other):
        return Tuple(super().__mul__(other))

    def __getitem__(self, item):
        if isinstance(item, (int, np.integer)):
            return super().__getitem__(item)
        else:
            return Tuple(super().__getitem__(item))

    def __repr__(self):
        return "Tuple({})".format(super().__repr__())

    def all(self, key=None):
        return self.iter().all(key)

    def any(self, key=None):
        return self.iter().any(key)

    def apply(self, fn):
        return fn(self)

    def apply_and_fit(self, fn):
        return fit(fn(self))

    def batch(self, size):
        return self.iter().batch(size).map(Tuple).tuple()

    def combinations(self, r, with_replacement=False):
        return self.iter().combinations(r, with_replacement)

    def combine_if(self, cond: bool, combinator: str, *a, **kw):
        if cond:
            return getattr(self, combinator)(*a, **kw)
        return self

    def contains(self, item):
        return item in self

    def count(self, key=None):
        return self.iter().count(key)

    def debug(self, fn, every_n=1):
        self.iter().debug(fn, every_n).for_each()
        return self

    def dict(self):
        """requires that items be 2-tuples"""
        return Dict(self)

    def distinct(self, key=None):
        return self.iter().distinct(key).tuple()

    def do(self, fn=None, tween_fn=None):
        self.iter().for_each(fn, tween_fn)
        return self

    def drop(self, n):
        return Tuple(self[n:])

    def drop_while(self, pred):
        return self.iter().drop_while(pred).tuple()

    def enumerate(self, start=0):
        return Tuple(enumerate(self, start))

    def every_n(self, n, start=0):
        require(n > 0)
        return Range(start, self.size(), n).map(lambda i: self[i]).tuple()

    def filter(self, pred=None, do_with_discarded=None):
        return self.iter().filter(pred, do_with_discarded).tuple()

    def first(self, pred=Unset, default=Unset):
        return self.iter().first(pred, default)

    def flat_map(self, fn):
        return self.iter().flat_map(fn).tuple()

    def flatten(self):
        """requires that items are iterable"""
        return self.iter().flatten().tuple()

    def fold(self, initial, fn):
        return self.iter().fold(initial, fn)

    def for_each(self, fn=None, tween_fn=None):
        return self.iter().for_each(fn, tween_fn)

    def group_by(self, key=None):
        return self.iter().group_by(key)

    def intersperse(self, item):
        return self.iter().intersperse(item).tuple()

    def iter(self):
        return Iterator(self)

    def last(self, pred=Unset, default=Unset):
        return self.iter().last(pred, default)

    def list(self):
        return List(self)

    def map(self, fn):
        return self.iter().map(fn).tuple()

    def map_to_keys(self, fn):
        return self.iter().map_to_keys(fn)

    def map_to_pairs(self, fn):
        return self.iter().map_to_pairs(fn).tuple()

    def map_to_values(self, fn):
        return self.iter().map_to_values(fn)

    def max(self, key=None, default=Unset):
        return self.iter().max(key, default)

    def min(self, key=None, default=Unset):
        return self.iter().min(key, default)

    def min_max(self, key=None, default=Unset):
        return self.iter().min_max(key, default)

    def partition(self, pred):
        t, f = self.iter().partition(pred)
        return t.tuple(), f.tuple()

    def only(self, pred=Unset):
        return self.iter().only(pred)

    def permutations(self, r=None):
        return self.iter().permutations(r)

    def powerset(self):
        return self.iter().powerset()

    def product(self, *its, repeat=1):
        return self.iter().product(*its, repeat=repeat)

    def reduce(self, fn, default=Unset):
        return self.iter().reduce(fn, default)

    def repeat(self, n):
        if n is None:
            raise ValueError("cannot infinitely repeat materialized collections. try collection.iter().repeat().")
        return self.iter().repeat(n).tuple()

    def reversed(self):
        return Tuple(reversed(self))

    def set(self):
        return Set(self)

    def shuffled(self, random=None):
        out = self.list()
        insecure_random.shuffle(out, random=random)
        return out.tuple()

    def size(self):
        return len(self)

    def sliding(self, size, step=1):
        return fit(range(0, self.size() - size + 1, step)).map(lambda i: self[i : i + size]).tuple()

    def sorted(self, key=None, reverse=False):
        return Tuple(sorted(self, key=key, reverse=reverse))

    def take(self, n):
        return Tuple(self[:n])

    def take_while(self, pred):
        return self.iter().take_while(pred).tuple()

    def timestamp(self, clock=time.time):
        return self.iter().timestamp(clock)

    def tqdm(self, *a, **kw):
        return Iterator(tqdm(self, *a, **kw))

    def transpose(self):
        return self.iter().transpose().tuple()

    def tuple(self):
        return Tuple(self)

    unzip = transpose

    def zip(self, *others):
        return self.iter().zip(*others).tuple()

    def zip_append(self, *others):
        return self.iter().zip_append(*others).tuple()

    def zip_into(self, other):
        return self.iter().zip_into(other).tuple()

    def partition_slice(self, start: int, stop: int = None, length: int = None):
        require((stop is None) ^ (length is None), "must specify exactly one of stop or length")
        if length is not None:
            stop = start + length
        beginning = self[:start]
        middle = self[start:stop]
        end = self[stop:]
        return beginning + end, middle


class List(list):
    def __add__(self, other):
        return List(super().__add__(other))

    def __mul__(self, other):
        return List(super().__mul__(other))

    def __rmul__(self, other):
        return List(super().__rmul__(other))

    def __getitem__(self, item):
        if isinstance(item, (int, np.integer)):
            return super().__getitem__(item)
        else:
            return List(super().__getitem__(item))

    def __repr__(self):
        return "List({})".format(super().__repr__())

    def all(self, key=None):
        return self.iter().all(key)

    def any(self, key=None):
        return self.iter().any(key)

    def appended(self, item):
        ls = self.list()
        ls.append(item)
        return ls

    def apply(self, fn):
        return fn(self)

    def apply_and_fit(self, fn):
        return fit(fn(self))

    def batch(self, size):
        return self.iter().batch(size).map(List).list()

    def combinations(self, r, with_replacement=False):
        return self.iter().combinations(r, with_replacement)

    def combine_if(self, cond: bool, combinator: str, *a, **kw):
        if cond:
            return getattr(self, combinator)(*a, **kw)
        return self

    def contains(self, item):
        return item in self

    def copy(self):
        return List(self)

    def count(self, key=None):
        return self.iter().count(key)

    def debug(self, fn, every_n=1):
        self.iter().debug(fn, every_n).for_each()
        return self

    def dict(self):
        """requires that items be 2 element iterables"""
        return Dict(self)

    def discard(self, value):
        try:
            self.remove(value)
        except ValueError:
            return False
        return True

    def distinct(self, key=None):
        return self.iter().distinct(key).list()

    def do(self, fn=None, tween_fn=None):
        self.iter().for_each(fn, tween_fn)
        return self

    def drain(self):
        def gen():
            while self:
                yield self.pop()

        return Iterator(gen())

    def drop(self, n):
        return List(self[n:])

    def drop_while(self, pred):
        return self.iter().drop_while(pred).list()

    def enumerate(self, start=0):
        return List(enumerate(self, start))

    def every_n(self, n, start=0):
        require(n > 0)
        return Range(start, self.size(), n).map(lambda i: self[i]).list()

    def extended(self, iterable):
        ls = self.list()
        ls.extend(iterable)
        return ls

    def filter(self, pred=None, do_with_discarded=None):
        return self.iter().filter(pred, do_with_discarded).list()

    def first(self, pred=Unset, default=Unset):
        return self.iter().first(pred, default)

    def flat_map(self, fn):
        return self.iter().flat_map(fn).list()

    def flatten(self):
        """requires that items are iterable"""
        return self.iter().flatten().list()

    def fold(self, initial, fn):
        return self.iter().fold(initial, fn)

    def for_each(self, fn=None, tween_fn=None):
        return self.iter().for_each(fn, tween_fn)

    def group_by(self, key=None):
        return self.iter().group_by(key)

    def intersperse(self, item):
        return self.iter().intersperse(item).list()

    def iter(self):
        return Iterator(self)

    def last(self, pred=Unset, default=Unset):
        return self.iter().last(pred, default)

    def list(self):
        return List(self)

    def map(self, fn):
        return self.iter().map(fn).list()

    def map_to_keys(self, fn):
        return self.iter().map_to_keys(fn)

    def map_to_pairs(self, fn):
        return self.iter().map_to_pairs(fn).list()

    def map_to_values(self, fn):
        return self.iter().map_to_values(fn)

    def max(self, key=None, default=Unset):
        return self.iter().max(key, default)

    def min(self, key=None, default=Unset):
        return self.iter().min(key, default)

    def min_max(self, key=None, default=Unset):
        return self.iter().min_max(key, default)

    def partition(self, pred):
        t, f = self.iter().partition(pred)
        return t.list(), f.list()

    def permutations(self, r=None):
        return self.iter().permutations(r)

    def powerset(self):
        return self.iter().powerset()

    def product(self, *its, repeat=1):
        return self.iter().product(*its, repeat=repeat)

    def only(self, pred=Unset):
        return self.iter().only(pred)

    def reduce(self, fn, default=Unset):
        return self.iter().reduce(fn, default)

    def repeat(self, n):
        if n is None:
            raise ValueError("cannot infinitely repeat materialized collections. try collection.iter().repeat().")
        return self.iter().repeat(n).list()

    def reversed(self):
        return List(reversed(self))

    def set(self):
        return Set(self)

    def shuffled(self, random=None):
        out = self.list()
        insecure_random.shuffle(out, random=random)
        return out

    def size(self):
        return len(self)

    def sliding(self, size, step=1):
        return fit(range(0, self.size() - size + 1, step)).map(lambda i: self[i : i + size]).list()

    def sorted(self, key=None, reverse=False):
        return List(sorted(self, key=key, reverse=reverse))

    def take(self, n):
        return List(self[:n])

    def take_while(self, pred):
        return self.iter().take_while(pred).list()

    def timestamp(self, clock=time.time):
        return self.iter().timestamp(clock)

    def tqdm(self, *a, **kw):
        return Iterator(tqdm(self, *a, **kw))

    def transpose(self):
        return self.iter().transpose().list()

    def tuple(self):
        return Tuple(self)

    unzip = transpose

    def zip(self, *others):
        return self.iter().zip(*others).list()

    def zip_append(self, *others):
        return self.iter().zip_append(*others).list()

    def zip_into(self, other):
        return self.iter().zip_into(other).list()

    def partition_slice(self, start: int, stop: int = None, length: int = None):
        require((stop is None) ^ (length is None), "must specify exactly one of stop or length")
        if length is not None:
            stop = start + length
        beginning = self[:start]
        middle = self[start:stop]
        end = self[stop:]
        return beginning + end, middle


class Set(set):
    def __add__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def __or__(self, other):
        return self.union(other)

    def __ior__(self, other):
        for item in other:
            self.add(item)
        return self

    def __sub__(self, other):
        return self.difference(other)

    def __isub__(self, other):
        self.difference_update(other)
        return self

    def __xor__(self, other):
        return self.symmetric_difference(other)

    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self

    def add(self, item):
        new = item not in self
        super().add(item)
        return new

    def all(self, key=None):
        return self.iter().all(key)

    def any(self, key=None):
        return self.iter().any(key)

    def apply(self, fn):
        return fn(self)

    def apply_and_fit(self, fn):
        return fit(fn(self))

    def batch(self, size):
        return self.iter().batch(size).map(lambda b: b.set())

    def combinations(self, r, with_replacement=False):
        return self.iter().combinations(r, with_replacement)

    def combine_if(self, cond: bool, combinator: str, *a, **kw):
        if cond:
            return getattr(self, combinator)(*a, **kw)
        return self

    def contains(self, item):
        return item in self

    def copy(self):
        return Set(self)

    def count(self, key=None):
        return self.iter().count(key)

    def debug(self, fn, every_n=1):
        self.iter().debug(fn, every_n).for_each()
        return self

    def dict(self):
        """requires that items be 2-tuples"""
        return Dict(self)

    def difference(self, *s):
        return Set(super().difference(*s))

    def discard(self, item):
        removed = item in self
        super().discard(item)
        return removed

    def do(self, fn=None, tween_fn=None):
        self.iter().for_each(fn, tween_fn)
        return self

    def drain(self):
        def gen():
            while self:
                yield self.pop()

        return Iterator(gen())

    def enumerate(self, start=0):
        return self.iter().enumerate(start)

    def every_n(self, n, start=0):
        return self.iter().every_n(n, start).set()

    def filter(self, pred=None, do_with_discarded=None):
        return self.iter().filter(pred, do_with_discarded).set()

    def first(self, pred=Unset, default=Unset):
        return self.iter().first(pred, default)

    def flat_map(self, fn):
        return self.iter().flat_map(fn).set()

    def flatten(self):
        """requires that items are iterable"""
        return self.iter().flatten().set()

    def fold(self, initial, fn):
        return self.iter().fold(initial, fn)

    def for_each(self, fn=None, tween_fn=None):
        return self.iter().for_each(fn, tween_fn)

    def group_by(self, key=None):
        return self.iter().group_by(key)

    def intersection(self, *s):
        return Set(super().intersection(*s))

    def iter(self):
        return Iterator(self)

    def last(self, pred=Unset, default=Unset):
        return self.iter().last(pred, default)

    def list(self):
        return List(self)

    def map(self, fn):
        return self.iter().map(fn).set()

    def map_to_keys(self, fn):
        return self.iter().map_to_keys(fn)

    def map_to_pairs(self, fn):
        return self.iter().map_to_pairs(fn).set()

    def map_to_values(self, fn):
        return self.iter().map_to_values(fn)

    def max(self, key=None, default=Unset):
        return self.iter().max(key, default)

    def min(self, key=None, default=Unset):
        return self.iter().min(key, default)

    def min_max(self, key=None, default=Unset):
        return self.iter().min_max(key, default)

    def partition(self, pred):
        t, f = self.iter().partition(pred)
        return t.set(), f.set()

    def permutations(self, r=None):
        return self.iter().permutations(r)

    def powerset(self):
        return self.iter().powerset()

    def product(self, *its, repeat=1):
        return self.iter().product(*its, repeat=repeat)

    def only(self, pred=Unset):
        return self.iter().only(pred)

    def reduce(self, fn, default=Unset):
        return self.iter().reduce(fn, default)

    def set(self):
        return Set(self)

    def size(self):
        return len(self)

    def symmetric_difference(self, s):
        return Set(super().symmetric_difference(s))

    def timestamp(self, clock=time.time):
        return self.iter().timestamp(clock)

    def tqdm(self, *a, **kw):
        return Iterator(tqdm(self, *a, **kw))

    def tuple(self):
        return Tuple(self)

    def union(self, *s):
        return Set(super().union(*s))

    def zip(self, other=None, *others):
        return self.iter().zip(other, *others)

    def zip_append(self, *others):
        return self.iter().zip_append(*others)

    def zip_into(self, other):
        return self.iter().zip_into(other)


class Dict(dict):
    """
    For compatibility with default python dictionaries, `.iter()` iterates over keys only.
    However, other methods iterate over items
        e.g. `.map(t(lambda k, v: (k, v * 2)))`.
    If you wish to operate on only keys or only values use `.keys()` or `.values()` before your desired operation,
        e.g. `fluent_dict.values().count()`.
    """

    def __repr__(self):
        return "Dict({})".format(super().__repr__())

    def all(self, key=None):
        return self.items().all(key)

    def any(self, key=None):
        return self.items().any(key)

    def apply(self, fn):
        return fn(self)

    def apply_and_fit(self, fn):
        return fit(fn(self))

    def batch(self, size):
        return self.items().batch(size).map(lambda d: d.dict()).tuple()

    def combine_if(self, cond: bool, combinator: str, *a, **kw):
        if cond:
            return getattr(self, combinator)(*a, **kw)
        return self

    def contains(self, item):
        return item in self

    def copy(self):
        return Dict(self)

    def count(self, key=None):
        return self.iter().count(key)

    def debug(self, fn, every_n=1):
        self.items().debug(fn, every_n).for_each()
        return self

    def dict(self):
        return Dict(self)

    def discard(self, key):
        return self.pop(key, Unset) is Unset

    def do(self, fn=None, tween_fn=None):
        self.items().for_each(fn, tween_fn)
        return self

    def drain(self):
        def gen():
            while self:
                yield self.popitem()

        return Iterator(gen())

    def every_n(self, n, start=0):
        return self.iter().every_n(n, start).dict()

    def filter(self, pred=None, do_with_discarded=None):
        return self.items().filter(pred, do_with_discarded).dict()

    def filter_keys(self, pred=None, do_with_discarded=None):
        return (
            self.items()
            .filter(pred and t(lambda k, v: pred(k)), do_with_discarded and t(lambda k, v: do_with_discarded(k)))
            .dict()
        )

    def filter_values(self, pred=None, do_with_discarded=None):
        return (
            self.items()
            .filter(pred and t(lambda k, v: pred(v)), do_with_discarded and t(lambda k, v: do_with_discarded(v)))
            .dict()
        )

    def first(self, pred=Unset, default=Unset):
        return self.items().first(pred, default)

    def flat_map(self, fn):
        return self.items().flat_map(fn).dict()

    # TODO: consider adding flatten

    def fold(self, initial, fn):
        return self.items().fold(initial, fn)

    def for_each(self, fn=None, tween_fn=None):
        return self.items().for_each(fn, tween_fn)

    def group_by(self, key=None):
        return self.items().group_by(key).map_values(lambda d: d.dict())

    def invert(self):
        return Dict({v: k for k, v in self.items()})

    def invert_collect(self):
        """invert this dictionary and collect key collisions (multiple copies of the same value in the uninverted dictionary) into lists"""
        out = Dict()
        for k, v in self.items():
            out.setdefault(v, List()).append(k)
        return out

    def invert_flatten(self):
        """invert this dictionary and flatten values into multiple keys"""
        return Dict({v: k for k, vs in self.items() for v in vs})

    def items(self):
        return Iterator(super().items())

    def iter(self):
        return Iterator(self)

    def keys(self):
        return Iterator(super().keys())

    def last(self, pred=Unset, default=Unset):
        return self.iter().last(pred, default)

    def list(self):
        return List(self.items())

    def map(self, fn):
        return self.items().map(fn).dict()

    def map_keys(self, fn):
        return Dict({fn(k): v for k, v in self.items()})

    def map_values(self, fn):
        return Dict({k: fn(v) for k, v in self.items()})

    def max(self, key=None, default=Unset):
        return self.iter().max(key, default)

    def max_key(self, key=None, default=Unset):
        return self.iter().max(key and t(lambda k, v: key(k)), default)

    def max_value(self, key=None, default=Unset):
        return self.iter().max(key and t(lambda k, v: key(v)), default)

    def min(self, key=None, default=Unset):
        return self.iter().min(key, default)

    def min_key(self, key=None, default=Unset):
        return self.iter().min(key and t(lambda k, v: key(k)), default)

    def min_value(self, key=None, default=Unset):
        return self.iter().min(key and t(lambda k, v: key(v)), default)

    def min_max(self, key=None, default=Unset):
        return self.iter().min_max(key, default)

    def min_max_key(self, key=None, default=Unset):
        return self.iter().min_max(key and t(lambda k, v: key(k)), default)

    def min_max_value(self, key=None, default=Unset):
        return self.iter().min_max(key and t(lambda k, v: key(v)), default)

    def partition(self, pred):
        t, f = self.items().partition(pred)
        return t.dict(), f.dict()

    def partition_key(self, pred):
        _t, f = self.items().partition(t(lambda k, v: pred(k)))
        return _t.dict(), f.dict()

    def partition_value(self, pred):
        _t, f = self.items().partition(t(lambda k, v: pred(v)))
        return _t.dict(), f.dict()

    def powerset(self):
        return self.iter().powerset()

    def put(self, k, v):
        self[k] = v
        return self

    def only(self, pred=Unset):
        return self.iter().only(pred)

    def timestamp(self, clock=time.time):
        return self.items().timestamp(clock)

    def tqdm(self, *a, **kw):
        return Iterator(tqdm(self.items(), *a, **kw))

    def tuple(self):
        return Tuple(self.items())

    def updated(self, E=None, **F):
        d = self.dict()
        if E is None:
            d.update(**F)
        else:
            d.update(E, **F)
        return d

    def reduce(self, fn, default=Unset):
        return self.items().reduce(fn, default)

    def remove(self, k):
        self.pop(k, None)
        return self

    def size(self):
        return len(self)

    def values(self):
        return Iterator(super().values())


class Range:
    def __init__(self, *a):
        if len(a) == 0:
            raise TypeError("Range expected 1 arguments, got 0")
        elif len(a) > 3:
            raise TypeError(f"Range expected at most 3 arguments, got {len(a)}")
        if len(a) == 1 and isinstance(a[0], (range, Range)):
            self._range = a[0]
        else:
            require(all(isinstance(_, int) for _ in a), "All Range arguments should be ints but got {}", a)
            self._range = range(*a)
        self.start = self._range.start
        self.stop = self._range.stop
        self.step = self._range.step

    def __contains__(self, item):
        return item in self._range

    def __getitem__(self, item):
        r = self._range[item]
        if isinstance(item, (int, np.integer)):
            return r
        return Range(r)

    def __iter__(self):
        return iter(self._range)

    def __len__(self):
        return len(self._range)

    def __repr__(self):
        return "Range({}, {}, {})".format(self.start, self.stop, self.step)

    def all(self, key=None):
        return self.iter().all(key)

    def any(self, key=None):
        return self.iter().any(key)

    def apply(self, fn):
        return fn(self)

    def apply_and_fit(self, fn):
        return fit(fn(self))

    def batch(self, size):
        return self.iter().batch(size)

    def combinations(self, r, with_replacement=False):
        return self.iter().combinations(r, with_replacement)

    def combine_if(self, cond: bool, combinator: str, *a, **kw):
        if cond:
            return getattr(self, combinator)(*a, **kw)
        return self

    def contains(self, item):
        return item in self

    def count(self, key=None):
        return self.iter().count(key)

    def debug(self, fn, every_n=1):
        self.iter().debug(fn, every_n).for_each()
        return self

    def distinct(self, key=None):
        return self.iter().distinct(key)

    def do(self, fn=None, tween_fn=None):
        self.iter().for_each(fn, tween_fn)
        return self

    def drop(self, n):
        if n >= 0:
            return Range(self.start + self.step * n, self.stop, self.step)
        else:
            return Range(self.stop + self.step * n, self.stop, self.step)

    def drop_while(self, pred):
        return Range(self.first(lambda i: not pred(i), self.stop), self.stop, self.step)

    def enumerate(self, start=0):
        return Iterator(enumerate(self, start))

    def every_n(self, n, start=0):
        require(n > 0)
        return Range(self.start + start * self.step, self.stop, self.step * n)

    def filter(self, pred=None, do_with_discarded=None):
        return self.iter().filter(pred, do_with_discarded)

    def first(self, pred=Unset, default=Unset):
        return self.iter().first(pred, default)

    def flat_map(self, fn):
        return self.iter().flat_map(fn)

    def fold(self, initial, fn):
        return self.iter().fold(initial, fn)

    def for_each(self, fn=None, tween_fn=None):
        return self.iter().for_each(fn, tween_fn)

    def group_by(self, key=None):
        return self.iter().group_by(key)

    def intersperse(self, item):
        return self.iter().intersperse(item)

    def iter(self):
        return Iterator(self._range)

    def last(self, pred=Unset, default=Unset):
        return self.iter().last(pred, default)

    def list(self):
        return List(self)

    def map(self, fn):
        return self.iter().map(fn)

    def map_to_keys(self, fn):
        return self.iter().map_to_keys(fn)

    def map_to_pairs(self, fn):
        return self.iter().map_to_pairs(fn)

    def map_to_values(self, fn):
        return self.iter().map_to_values(fn)

    def max(self, key=None, default=Unset):
        return self.iter().max(key, default)

    def min(self, key=None, default=Unset):
        return self.iter().min(key, default)

    def min_max(self, key=None, default=Unset):
        return self.iter().min_max(key, default)

    def partition(self, pred):
        return self.iter().partition(pred)

    def permutations(self, r=None):
        return self.iter().permutations(r)

    def powerset(self):
        return self.iter().powerset()

    def product(self, *its, repeat=1):
        return self.iter().product(*its, repeat=repeat)

    def only(self, pred=Unset):
        return self.iter().only(pred)

    def reduce(self, fn, default=Unset):
        return self.iter().reduce(fn, default)

    def repeat(self, n=None):
        return self.iter().repeat(n)

    def reversed(self):
        r = self._range
        r = range(r.start + (len(r) - 1) * r.step, r.start - r.step, -r.step)
        return Range(r.start, r.stop, r.step)

    def set(self):
        return Set(self)

    def size(self):
        return len(self)

    def sliding(self, size, step=1):
        return fit(range(0, self.size() - size + 1, step)).map(lambda i: self[i : i + size])

    def sorted(self, key=None, reverse=False):
        return Iterator(sorted(self, key=key, reverse=reverse))

    def take(self, n):
        if n >= 0:
            return Range(self.start, min(self.stop, self.start + self.step * n), self.step)
        else:
            return Range(self.start, self.stop + self.step * n, self.step)

    def take_while(self, pred):
        return Range(self.start, self.first(lambda i: not pred(i), self.stop), self.step)

    def timestamp(self, clock=time.time):
        return self.iter().timestamp(clock)

    def tqdm(self, *a, **kw):
        return Iterator(tqdm(self, *a, **kw))

    def tuple(self):
        return Tuple(self)

    def zip(self, *others):
        return self.iter().zip(*others)

    def zip_append(self, *others):
        return self.iter().zip_append(*others)

    def zip_into(self, other):
        return self.iter().zip_into(other)

    def zip_append(self, other=None, *others):
        return self.iter().zip_append(other, *others)

    def zip_into(self, other):
        return self.iter().zip_into(other)


def split(s, *seps):
    def split_():
        match seps[0]:
            case None:
                return List(s.split())
            case "":
                return List(s)
            case sep:
                return List(s.split(sep))
    if not seps:
        return s
    return List([split(s, *seps[1:]) for s in split_()])


def rsub(a, b):
    return b - a


def read(filename):
    from os import path
    from inspect import stack
    with open(path.join(path.dirname(stack()[1][0].f_code.co_filename), filename)) as f:
        return f.read()


@contextmanager
def print_duration():
    start = time.time()
    yield
    print(f"took: {round(time.time() - start, 3)}s")


def hw(m):
    return len(m), len(m[0])


def inbounds(matrix):
    h, w = hw(matrix)
    def test(x, y):
        return 0 <= y < h and 0 <= x < w
    return test


def turn_left(d, symbols="NWSE"):
    return np.roll(tuple(symbols), -1, 0)[symbols.index(d)]


def turn_right(d, symbols="NWSE"):
    return np.roll(tuple(symbols), 1, 0)[symbols.index(d)]


def take_step(x, y, d, symbols="NWSE"):
    return [(x, y-1), (x-1, y), (x, y+1), (x+1, y)][symbols.index(d)]


def euclidean_distance(p1, p2):
    s = 0
    for i in range(len(p1)):
        d = p1[i] - p2[i]
        s += d * d
    return sqrt(s)


def clamp(value, limit):
    vmin, vmax = limit
    return vmin if value < vmin else vmax if value > vmax else value


def difference(x, y):
    return abs(x - y)


def true(*a, **kw):
    return True


def false(*a, **kw):
    return False


def neighbors(x, y=None):
    if y is None:
        x, y = x
    return Tuple(((x, y-1), (x, y+1), (x-1, y), (x+1, y)))


def ranges_intersect(a, b):
    # assumes step=1
    return a.start in b or b.start in a


def split_range(r, value):
    # assumes step=1
    start, stop = r.start, r.stop
    return range(start, min(value, stop)), range(value, stop)


def dataclass(
    cls=None,
    /,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    match_args=True,
    kw_only=False,
    slots=False,
):
    def wrap(cls):
        cls = basedataclass(
            cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            match_args=match_args,
            kw_only=kw_only,
            slots=slots,
        )

        def copy(self, **kw):
            new = deepcopy(self)
            for k, v in kw.items():
                setattr(new, k, v)
            return new
        cls.copy = copy
        return cls

    if cls is None:
        return wrap
    return wrap(cls)


class Primes:
    def __init__(self):
        self.list = List([2])
        self.set = Set([2])
        self.checked = 2

    def __iter__(self):
        return Iterator(count()).filter(self.is_prime)

    def check(self, n):
        self.checked = n
        stop = sqrt(n)
        for prime in self.list:
            if prime > stop:
                self.list.append(n)
                self.set.add(n)
                break
            if not n % prime:
                break

    def is_prime(self, n):
        for i in range(self.checked + 1, n + 1):
            self.check(i)
        return n in self.set

    @cache
    def factors(self, n):
        factors = List()
        if n == 1:
            return factors
        while True:
            if self.is_prime(n):
                return factors + [n]
            for prime in self.list:
                d, m = divmod(n, prime)
                if not m:
                    factors.append(prime)
                    n = d
                    break


primes = Primes()


def indices(m):
    h, w = hw(m)
    return Range(w).product(Range(h))