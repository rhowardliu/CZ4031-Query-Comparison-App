import unittest
from tree_parsing import *
from cluster_class import Cluster
from vocalizer import Node
import vocalizer as v
import sql_results as sr


# class Node(v.Node):

#   def __init__(self, node_type, group_key, sort_key=None, relation_name=None, schema=None, alias=None,  join_type=None, index_name=None, 
#             hash_cond=None, table_filter=None, index_cond=None, merge_cond=None, recheck_cond=None, join_filter=None, subplan_name=None, actual_rows=None,
#             actual_time=None):
#       self.node_type = node_type
#       self.children = []
#       self.relation_name = relation_name
#       self.schema = schema
#       self.alias = alias
#       self.group_key = group_key
#       self.sort_key = sort_key
#       self.join_type = join_type
#       self.index_name = index_name
#       self.hash_cond = hash_cond
#       self.table_filter = table_filter
#       self.index_cond = index_cond
#       self.merge_cond = merge_cond
#       self.recheck_cond = recheck_cond
#       self.join_filter = join_filter
#       self.subplan_name = subplan_name
#       self.actual_rows = actual_rows
#       self.actual_time = actual_time
#       # extra
#       self.visited = False
#       self.parent = None


#   def add_children(self, child):
#       self.children.append(child)
  
#   def set_output_name(self, output_name):
#       if "T" == output_name[0] and output_name[1:].isdigit():
#           self.output_name = int(output_name[1:])
#       else:
#           self.output_name = output_name

#   def get_output_name(self):
#       if str(self.output_name).isdigit():
#           return "T" + str(self.output_name)
#       else:
#           return self.output_name

#   def set_step(self, step):
#       self.step = step

#   def __eq__(self, other):
#     if isinstance(other, self.__class__):
#         return self.node_type == other.node_type and self.group_key == other.group_key \
#           and self.sort_key == other.sort_key 
#     else:
#         return False

#   def __hash__(self):
#     return hash((self.node_type, self.group_key, self.sort_key))

#   def __str__(self):
#     return f"{str(self.node_type)} on {str(self.group_key)} and {str(self.sort_key)}"

def print_clusters(clusters):
  for i in range(len(clusters)):
    print(i)
    [print(node) for node in clusters[i]]


class TreeParseTest(unittest.TestCase):
  def test_get_cluster_set(self):
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
    # for n in my_cluster:
    #   print(n)
    self.assertEqual(correct_cluster, my_cluster)

  def test_parse_tree(self):
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
    node_a1 = v.parse_json(sr.q3)
    node_b1 = v.parse_json(sr.q3)
 
    my_cluster = Cluster(get_cluster_set(node_a1, node_b1, set()))
    # print(f'my cluster is {my_cluster}')
    # self.assertEqual(correct_cluster, my_cluster)
    self.assertTrue(node_a1==node_b1)
    self.assertTrue(node_a1.children[0]==node_b1.children[0])
    self.assertEqual(len(my_cluster), 10)
  
  def test_level_traversal(self):
    all_nodes = []
    node_a1 = v.parse_json(sr.q3)
    level_traversal(node_a1, 0, all_nodes)
    self.assertEqual(len(all_nodes),10)
    correct_node_num = [1,1,1,1,1,1,1,2,2,1]
    for i in range(10):
      self.assertEqual(len(all_nodes[i]),correct_node_num[i])

  def test_same_tree(self):
    # test if trees same is there diff
    root = v.parse_json(sr.q3)
    my_cluster = parse_tree(root, root)
    cluster_dict = create_cluster_dict(my_cluster)
    diffs = get_tree_differences(root,cluster_dict)
    self.assertEqual(len(diffs),0)

  def test_diff_tree(self):
    # test if trees diff is there diff
    root = v.parse_json(sr.q3)
    diff_root = v.parse_json(sr.q3_fake)
    my_cluster = parse_tree(root, diff_root)
    cluster_dict = create_cluster_dict(my_cluster)
    diffs = get_tree_differences(root,cluster_dict)
    self.assertEqual(len(diffs),1)

if __name__ == '__main__':
  unittest.main()


    