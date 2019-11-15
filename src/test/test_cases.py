import unittest
from src.controller.tree_parsing import *
from src.model.cluster_class import Cluster
from src.model.node_class import Node
import src.model.node_class as n
import src.test.sql_results as sr
import src.test.edited_sql_results as esr

def print_clusters(clusters):
    for i in range(len(clusters)):
        print(i)
        [print(node) for node in clusters[i]]


class TreeParseTest(unittest.TestCase):
    def test_get_cluster_set(self):
        print('--- Get Cluster Set ---')
        node_a1 = Node('merge_join', 'id')
        node_a2 = Node('single_scan', 'id')
        node_a3 = Node('filter', 'id')
        node_a4 = Node('index_scan', 'id')
        node_a5 = Node('select', 'id')
        node_a1.add_children(node_a2)
        node_a1.add_children(node_a3)
        node_a3.add_children(node_a4)
        node_a2.add_children(node_a5)

        node_b1 = Node('merge_join', 'id')
        node_b2 = Node('single_scan', 'id')
        node_b3 = Node('filter', 'id')
        node_b4 = Node('select', 'id')
        node_b1.add_children(node_b2)
        node_b1.add_children(node_b3)
        node_b2.add_children(node_b4)

        correct_cluster = set([node_a1, node_a2, node_a3, node_a5])
        my_cluster = get_cluster_set(node_a1, node_b1, set())
        self.assertEqual(correct_cluster, my_cluster)

    def test_parse_tree(self):
        print('--- Parse Tree ---')
        node_a1 = Node('merge_join', 'id')
        node_a2 = Node('merge_join', 'age')
        node_a3 = Node('filter', 'age')
        node_a4 = Node('seq_scan', 'id')
        node_a5 = Node('seq_scan', '')
        node_a6 = Node('index_scan', '')
        node_a1.add_children(node_a2)
        node_a1.add_children(node_a3)
        node_a3.add_children(node_a4)
        node_a2.add_children(node_a5)
        node_a2.add_children(node_a6)

        node_b1 = Node('merge_join', 'id')
        node_b2 = Node('select', 'id')
        node_b3 = Node('filter', 'age')
        node_b4 = Node('seq_scan', 'id')
        node_b5 = Node('index_scan', '')
        node_b1.add_children(node_b2)
        node_b1.add_children(node_b3)
        node_b3.add_children(node_b4)
        node_b4.add_children(node_b5)

        cluster1 = set([node_a1])
        cluster2 = set([node_a3, node_a4])
        cluster3 = set([node_a6])
        correct_clusters = [cluster1, cluster2, cluster3]
        my_cluster = parse_tree(node_a1, node_b1)
        my_cluster_sets = [c.clusterSet for c in my_cluster]
        self.assertEqual(correct_clusters, my_cluster_sets)

    def test_cluster_object(self):
        print('--- Cluster Object ---')
        node_a1 = Node('merge_join', 'id')
        node_a2 = Node('single_scan', 'id')
        node_a3 = Node('filter', 'id')
        node_a4 = Node('index_scan', 'id')
        node_a5 = Node('select', 'id')
        node_a1.add_children(node_a2)
        node_a1.add_children(node_a3)
        node_a3.add_children(node_a4)
        node_a2.add_children(node_a5)

        node_b1 = Node('merge_join', 'id')
        node_b2 = Node('single_scan', 'id')
        node_b3 = Node('filter', 'id')
        node_b4 = Node('select', 'id')
        node_b1.add_children(node_b2)
        node_b1.add_children(node_b3)
        node_b2.add_children(node_b4)

        correct_cluster = Cluster(set([node_a3, node_a1, node_a5, node_a2]))
        my_cluster = Cluster(get_cluster_set(node_a1, node_b1, set()))
        self.assertEqual(correct_cluster, my_cluster)
        self.assertEqual(len(my_cluster), 4)

    def test_cluster_dict(self):
        print('--- Cluster Dictionary ---')
        node_a1 = Node('merge_join', 'id')
        node_a2 = Node('merge_join', 'age')
        node_a3 = Node('filter', 'age')
        node_a4 = Node('seq_scan', 'id')
        node_a5 = Node('seq_scan', '')
        node_a6 = Node('index_scan', '')
        node_a1.add_children(node_a2)
        node_a1.add_children(node_a3)
        node_a3.add_children(node_a4)
        node_a2.add_children(node_a5)
        node_a2.add_children(node_a6)

        node_b1 = Node('merge_join', 'id')
        node_b2 = Node('select', 'id')
        node_b3 = Node('filter', 'age')
        node_b4 = Node('seq_scan', 'id')
        node_b5 = Node('index_scan', '')
        node_b1.add_children(node_b2)
        node_b1.add_children(node_b3)
        node_b3.add_children(node_b4)
        node_b4.add_children(node_b5)

        cluster1 = Cluster(set([node_a1]))
        cluster2 = Cluster(set([node_a3, node_a4]))
        cluster3 = Cluster(set([node_a6]))
        correct_clusters = [cluster1, cluster2, cluster3]
        clusterdict = create_cluster_dict(correct_clusters)
        self.assertEqual(clusterdict[node_a1], 0)
        self.assertEqual(clusterdict[node_a3], 1)
        self.assertEqual(clusterdict[node_a4], 1)
        self.assertEqual(clusterdict[node_a6], 2)
        self.assertEqual(clusterdict[node_b1], 0)
        self.assertEqual(clusterdict[node_b3], 1)
        self.assertEqual(clusterdict[node_b4], 1)
        self.assertEqual(clusterdict[node_b5], 2)

    def test_cluster_json(self):
        print('--- Cluster JSON ---')
        node_a1 = n.parse_json(sr.q3)
        node_b1 = n.parse_json(sr.q3)

        my_cluster = Cluster(get_cluster_set(node_a1, node_b1, set()))
        all_nodes = []
        node_a1 = n.parse_json(sr.q3)
        level_traversal(node_a1, 0, all_nodes)
        i = 0
        print('Level | Node')
        for level in all_nodes:
            for node in level:
                print(f'{i} {str(node)}')
            i += 1
        self.assertTrue(node_a1 == node_b1)
        self.assertTrue(node_a1.children[0] == node_b1.children[0])
        self.assertEqual(len(my_cluster), 12)

    def test_level_traversal(self):
        print('--- Level Traversal ---')
        all_nodes = []
        node_a1 = n.parse_json(sr.q3)
        level_traversal(node_a1, 0, all_nodes)
        self.assertEqual(len(all_nodes), 10)
        correct_node_num = [1, 1, 1, 1, 1, 1, 1, 2, 2, 1]
        for i in range(10):
            self.assertEqual(len(all_nodes[i]), correct_node_num[i])

    def test_same_tree(self):
        print('--- Same Tree ---')
        root = n.parse_json(sr.q3)
        my_cluster = parse_tree(root, root)
        cluster_dict = create_cluster_dict(my_cluster)
        diffs = get_tree_differences(root, cluster_dict)
        self.assertEqual(len(diffs), 0)

    def test_diff_tree(self):
        print('--- Different Tree ---')
        root = n.parse_json(sr.q3)
        diff_root = n.parse_json(sr.q3_fake)
        my_cluster = parse_tree(root, diff_root)
        cluster_dict = create_cluster_dict(my_cluster)
        diffs = get_tree_differences(root, cluster_dict)
        self.assertEqual(len(diffs), 1)


if __name__ == '__main__':
    unittest.main()
