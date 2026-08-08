---
title: "Prime Number Cluster"
excerpt: "Optimized algorithms for fast prime number computation and built a small computer cluster network for distributed calculations."
date: 2024-11-01
status: "In Progress"
tags:
  - Python
  - Networking
  - Distributed Computing
  - Algorithms
---

## Overview

I wanted to push the limits of prime number computation — not just with better algorithms, but by distributing the work across a small home cluster. The goal is to find primes deeper into the number line than a single machine can efficiently reach.

## Current milestone

Reached approximately the 100 millionth prime on a single machine (verification in progress). Multi-machine distribution is the next goal — the architecture is designed for it, but successfully coordinating nodes across the LAN is still in progress.

## Goals

- Implement and benchmark multiple prime-finding algorithms (trial division, Sieve of Eratosthenes, segmented sieve)
- Set up a small local network cluster to distribute computation across machines
- Measure real-world performance gains from parallelization vs. single-machine baseline
- Eventually target the billionth prime with a realistic hardware setup

## Tools & Skills Used

- **Python** — algorithm implementation, multiprocessing, chunk-based computation
- **Linux** — server configuration, SSH, network setup
- **Networking** — LAN configuration, process coordination across nodes

## What I've learned so far

For smaller ranges, a single well-optimized local process beats the overhead of coordination. The interesting tradeoffs only start to show at scale — which is exactly why the cluster is worth pursuing. Building this taught me that distributed systems design is really about managing overhead, not just adding machines.
