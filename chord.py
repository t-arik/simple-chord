import unittest
from typing import Optional
from random import shuffle

class Node:
    def __init__(
            self,
            key: int,
            successor: Optional['Node'] = None,
            predecessor: Optional['Node'] = None):
        self.key = key
        self.successor = successor or self
        self.predecessor = predecessor or self

    def find_successor(self, node: 'Node'):
        succ = self.successor
        pred = self.predecessor

        if self == succ == pred:
            return self
        elif self < node and node <= succ:
            return succ
        elif self > succ and (node > self or node <= succ):
            return succ
        else:
            return self.successor.find_successor(node)

    def find_successor_key(self, key: int):
        return self.find_successor(Node(key))

    def __lt__(self, other): return self.key < other.key
    def __le__(self, other): return self.key <= other.key
    def __gt__(self, other): return self.key > other.key
    def __ge__(self, other): return self.key >= other.key
    def __eq__(self, other): return self.key == other.key


class Chord:
    def __init__(self, node: Node):
        self.node = node

    def join(self, node: Node):
        entry = self.node.find_successor(node)
        node.successor = entry
        node.predecessor = entry.predecessor
        node.successor.predecessor = node
        node.predecessor.successor = node
        


class TestChord(unittest.TestCase):
    def test_join(self):
        node_count = 4
        nodes = [Node(i) for i in range(node_count)]
        shuffle(nodes)
        chord = Chord(nodes[0])
        for node in nodes[1:]:
            chord.join(node)

        nodes.sort(key=lambda node: node.key)
        for i, node in enumerate(nodes):
            self.assertEqual(node.successor, nodes[(i + 1) % node_count])
            self.assertEqual(node.predecessor, nodes[(i - 1) % node_count])

if __name__ == '__main__':  
    unittest.main()
