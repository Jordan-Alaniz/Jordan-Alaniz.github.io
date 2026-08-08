---
title: "How I Sped Up Prime Number Computation"
date: 2026-06-26
categories:
  - Technical
tags:
  - Python
  - Algorithms
  - Distributed Computing
---

One of my personal projects involved computing prime numbers as fast as possible. What started as a simple exercise turned into a deep dive on algorithm design and distributed computing. I've reached approximately the 100 millionth prime on a single machine (verification pending), and my current goal is pushing further with a multi-machine cluster — eventually targeting the billionth prime with a realistic hardware setup.

## Starting Point: Trial Division

The most obvious approach: for every number `n`, check if any integer from `2` to `√n` divides it evenly.

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

Simple, but slow for large ranges. Every number gets its own full check.

## Chunk Computing

Instead of checking one number at a time, using parallel processing in chunks reduces time significantly:

```python
with multiprocessing.Pool(max_processes) as pool:
    while True:
        current_chunks = list(itertools.chain(*pool.map(work, [next(chunks) for i in range(max_processes)])))
        if len(current_chunks) + nums_found < calcTo:
            nums_found += len(current_chunks)
        else:
            current_chunks.sort()
            time2 = perf_counter()
            print(f'Your #: {current_chunks[calcTo-nums_found-1]}\nTime: {time2 - time1}sec')
            break
```

This is dramatically faster for finding all primes up to a large limit, but requires much more processing power and still hits computational slow-downs.

## Taking It Further: A Cluster

For very large ranges, I am working to set up a small network of computers to split the work. Each machine will handle a segment of the number range, and results will be collected centrally.

Note: I have found that simply brute forcing primes can be significantly faster for smaller numbers. I may consider a dynamic approach depending on the goal.

## Future Research: GPU Acceleration

I know from being around computers that GPU processing for small numerical tasks is unlike anything I have tried so far. It does depend heavily on the type and manufacturer of the GPU though, and might require learning a new language. I do want to research in the future how I could leverage my GPU to accelerate my search even further.

_Additional topics:_ I have a paper queued on a different algorithmic approach to prime generation that I want to work through. I could also experiment with binary tricks to skip numbers or search more efficiently. A segmented bitwise sieve distributed across a cluster would be incredibly fast while RAM is not a constraint.

## What I Took Away

- Algorithm choice matters more than raw hardware, up to a point
- Distributed computing has real overhead that has to be justified by the problem size
- Benchmarking with real numbers (not assumptions) is essential
