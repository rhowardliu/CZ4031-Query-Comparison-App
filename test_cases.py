import unittest
from tree_parsing import *

class Node(object):
  def __init__(self, ntype, key):
    super(Node, self).__init__()
    self.ntype = ntype
    self.children = []
    self.key = key
    self.visited = False

  def addChildren(self, child):
    self.children.append(child)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
        return self.ntype == other.ntype and self.key == other.key
    else:
        return False

  def __hash__(self):
    return hash((self.ntype, self.key))

  def __str__(self):
    return self.ntype + ' on ' + self.key

def print_clusters(clusters):
  for i in range(len(clusters)):
    print(i)
    [print(node) for node in clusters[i]]


class TreeParseTest(unittest.TestCase):
  def test_get_cluster(self):
    node_a1 = Node('merge_join', 'id')
    node_a2 = Node('single_scan', 'id')
    node_a3 = Node('filter', 'id')
    node_a4 = Node('index_scan', 'id')
    node_a5 = Node('select', 'id')
    node_a1.addChildren(node_a2)
    node_a1.addChildren(node_a3)
    node_a3.addChildren(node_a4)  
    node_a2.addChildren(node_a5)

    node_b1 = Node('merge_join', 'id')
    node_b2 = Node('single_scan', 'id')
    node_b3 = Node('filter', 'id')
    node_b4 = Node('select', 'id')
    node_b1.addChildren(node_b2)
    node_b1.addChildren(node_b3)
    node_b2.addChildren(node_b4)

    correct_cluster = set([node_a1, node_a2, node_a3, node_a5])
    my_cluster = get_cluster(node_a1, node_b1, set())
    for n in my_cluster:
      print(n)
    self.assertEqual(correct_cluster, my_cluster)

  def test_parse_tree(self):
    node_a1 = Node('merge_join', 'id')
    node_a2 = Node('merge_join', 'age')
    node_a3 = Node('filter', 'age')
    node_a4 = Node('seq_scan', 'id')
    node_a5 = Node('seq_scan', '')
    node_a6 = Node('index_scan', '')
    node_a1.addChildren(node_a2)
    node_a1.addChildren(node_a3)
    node_a3.addChildren(node_a4)  
    node_a2.addChildren(node_a5)
    node_a2.addChildren(node_a6)


    node_b1 = Node('merge_join', 'id')
    node_b2 = Node('select', 'id')
    node_b3 = Node('filter', 'age')
    node_b4 = Node('seq_scan', 'id')
    node_b5 = Node('index_scan', '')
    node_b1.addChildren(node_b2)
    node_b1.addChildren(node_b3)
    node_b3.addChildren(node_b4)
    node_b4.addChildren(node_b5)

    cluster1 = set([node_a1])
    cluster2 = set([node_a3, node_a4])
    cluster3 = set([node_a6])
    correct_clusters = [cluster1, cluster2, cluster3]
    my_cluster = parse_tree(node_a1, node_b1)
    print_clusters(my_cluster)
    self.assertEqual(correct_clusters, my_cluster)


if __name__ == '__main__':
  unittest.main()


    