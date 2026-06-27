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

I wanted to push the limits of prime number computation — not just with better algorithms, but by building a small home cluster to split the work across multiple machines.

## Goals

- Implement and benchmark multiple prime-finding algorithms (trial division, Sieve of Eratosthenes, segmented sieve)
- Set up a small local network cluster to distribute computation
- Measure and compare real-world performance gains from parallelization

## Tools & Skills Used

- **Python** — algorithm implementation, multiprocessing, socket communication
- **Linux** — server configuration, SSH, network setup
- **Networking** — LAN configuration, process coordination across nodes

## What I Learned

The biggest bottleneck was network latency and coordination overhead — for smaller ranges, a single optimized local process beat the cluster. But for very large ranges, distributing segments across machines made a real difference. This taught me the real tradeoffs in distributed systems design.
