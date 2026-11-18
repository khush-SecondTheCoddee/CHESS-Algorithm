import unittest

from chess import Graph, chess_v1


class ChessV1Tests(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(directed=True)
        self.graph.add_edge("S", "G", travel_time=2, cost=10)
        self.graph.add_edge("S", "A", travel_time=3, cost=4)
        self.graph.add_edge("A", "G", travel_time=3, cost=4)

    def test_straight_line_identical_baselines(self):
        graph = Graph()
        graph.add_edge("A", "B", travel_time=2, cost=3)
        result = chess_v1(graph, "A", "B")
        self.assertEqual(result.path, ["A", "B"])
        self.assertFalse(result.switched)
        self.assertEqual((result.ttd, result.art, result.ctd, result.actd_s), (2, 2, 3, 3))

    def test_pst_boundaries_and_switching(self):
        self.assertTrue(chess_v1(self.graph, "S", "G", 0).switched)
        self.assertFalse(chess_v1(self.graph, "S", "G", 99).switched)
        for pst in range(0, 100):
            result = chess_v1(self.graph, "S", "G", float(pst))
            self.assertEqual(result.switched, pst <= 20)
        result = chess_v1(self.graph, "S", "G", 20)
        self.assertEqual(result.path, ["S", "A", "G"])
        self.assertEqual(result.savings_pct, 20.0)

    def test_invalid_pst(self):
        for pst in (-0.01, 99.01, float("nan"), "20"):
            with self.subTest(pst=pst), self.assertRaises(ValueError):
                chess_v1(self.graph, "S", "G", pst)

    def test_unreachable(self):
        result = chess_v1(self.graph, "G", "S")
        self.assertIsNone(result.path)
        self.assertFalse(result.switched)


if __name__ == "__main__":
    unittest.main()
