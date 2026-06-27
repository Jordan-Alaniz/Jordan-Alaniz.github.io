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

One of my personal projects involved computing prime numbers as fast as possible. What started as a simple exercise turned into a deep dive on algorithm design and distributed computing. My current goal is finding a way to reach the billionth prime number and beyond with a realistic hardware setup.

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
def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i, v in enumerate(is_prime) if v]
```

This is dramatically faster for finding all primes up to a large limit, but requires much more processing power and still hits computational slow-downs.

## Taking It Further: A Cluster

For very large ranges, I am working to set up a small network of computers to split the work. Each machine will handle a segment of the number range, and results will be collected centrally.

Note: I have found that simply brute forcing primes can be significantly faster for smaller numbers. I may consider a dynamic approach depending on the goal.

## Future Research: GPU Acceleration

I know from being around computers that GPU processing for small numerical tasks is unlike anything I have tried so far. It does depend heavily on the type and manufacturer of the GPU though, and might require learning a new language. I do want to research in the future how I could leverage my GPU to accelerate my search even further.

_Additional topics:_ I did find a random pdf somewhere about a newer way to find prime numbers, so I will need to read up. I could also experiment with binary tricks to possibly skip numbers or more efficiently search through them. A segmented bitwise sieve distributed across a cluster would also be incredibly quick while RAM is not a limit.

## What I Took Away

- Algorithm choice matters more than raw hardware, up to a point
- Distributed computing has real overhead that has to be justified by the problem size
- Benchmarking with real numbers (not assumptions) is essential
