"""Core Prefix Caching Affinity Dispatcher implementation."""
import hashlib
from typing import Dict, List, Optional, Tuple, Any


class WorkerNode:
    def __init__(self, node_id: str, endpoint: str):
        self.node_id = node_id
        self.endpoint = endpoint
        self.active_connections = 0
        self.cached_prefixes: set = set()


class PrefixAffinityDispatcher:
    def __init__(self, replicas_per_worker: int = 10):
        self.replicas_per_worker = replicas_per_worker
        self.workers: Dict[str, WorkerNode] = {}
        self.ring: List[Tuple[int, str]] = []  # (hash, worker_id)

    def add_worker(self, worker_id: str, endpoint: str):
        self.workers[worker_id] = WorkerNode(worker_id, endpoint)
        for r in range(self.replicas_per_worker):
            v_key = f"{worker_id}#{r}"
            h = int(hashlib.md5(v_key.encode()).hexdigest(), 16)
            self.ring.append((h, worker_id))
        self.ring.sort(key=lambda x: x[0])

    def dispatch(self, prompt_prefix: str) -> WorkerNode:
        if not self.workers:
            raise RuntimeError("No workers registered in dispatcher")

        prefix_hash = int(hashlib.md5(prompt_prefix.encode()).hexdigest(), 16)
        # Find first ring node >= prefix_hash
        chosen_worker_id = None
        for h, w_id in self.ring:
            if h >= prefix_hash:
                chosen_worker_id = w_id
                break
        if chosen_worker_id is None:
            chosen_worker_id = self.ring[0][1]

        worker = self.workers[chosen_worker_id]
        worker.cached_prefixes.add(prefix_hash)
        return worker
