"""Unit tests for prefix-caching-affinity-dispatcher."""
import unittest
from prefix_caching_affinity_dispatcher.dispatcher import PrefixAffinityDispatcher


class TestPrefixAffinityDispatcher(unittest.TestCase):
    def setUp(self):
        self.disp = PrefixAffinityDispatcher()
        self.disp.add_worker("w1", "http://node1")
        self.disp.add_worker("w2", "http://node2")

    def test_identical_prefix_routes_to_same_worker(self):
        prefix = "SYSTEM_INSTRUCTIONS_HASH_12345"
        w_first = self.disp.dispatch(prefix)
        w_second = self.disp.dispatch(prefix)
        self.assertEqual(w_first.node_id, w_second.node_id)
