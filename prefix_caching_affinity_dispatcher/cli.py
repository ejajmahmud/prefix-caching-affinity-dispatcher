"""CLI for prefix-caching-affinity-dispatcher."""
import sys
import argparse
from .dispatcher import PrefixAffinityDispatcher


def main():
    parser = argparse.ArgumentParser(description="Prefix Caching Affinity Dispatcher CLI")
    parser.add_argument("--demo", action="store_true", help="Run consistent prefix affinity routing demo")
    args = parser.parse_args()

    if args.demo:
        dispatcher = PrefixAffinityDispatcher()
        dispatcher.add_worker("gpu_node_1", "http://10.0.0.1:8000")
        dispatcher.add_worker("gpu_node_2", "http://10.0.0.2:8000")
        dispatcher.add_worker("gpu_node_3", "http://10.0.0.3:8000")

        prefix_system = "You are a specialized Python DevOps coding assistant v2.4..."
        for req_idx in range(5):
            w = dispatcher.dispatch(prefix_system)
            print(f"Request {req_idx+1} routed to: {w.node_id} (Warm cache guaranteed)")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
