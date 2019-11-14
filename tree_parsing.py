import queue
import pdb
from cluster_class import Cluster

def level_traversal(root, level, all_nodes):
  if root is None:
    return
  if level >= len(all_nodes):
    new_level = []
    all_nodes.append(new_level)
  all_nodes[level].append(root)
  for child in root.children:
    level_traversal(child,level+1,all_nodes )


def get_cluster_set(a, b, cluster_grp):
  if a!=b:
    return cluster_grp
  if a.children and b.children:
    a_set = {x for x in a.children}
    b_set = {x for x in b.children}
    if a_set == b_set:
    # no banana so ok!
      if len(a_set) == 1:
        cluster_grp = cluster_grp.union(get_cluster_set(a.children[0], b.children[0], set()))
      else:
        if a.children[0] == b.children[0]:
          cluster_1 = get_cluster_set(a.children[0], b.children[0], set())
          cluster_2 = get_cluster_set(a.children[1], b.children[1], set())
        else:
          cluster_1 = get_cluster_set(a.children[0], b.children[1], set())
          cluster_2 = get_cluster_set(a.children[1], b.children[0], set())
        cluster_grp = cluster_grp.union(cluster_1, cluster_2)
  cluster_grp.add(a)  
  a.visited=True
  b.visited=True
  return cluster_grp

def parse_tree(A_root, B_root):
  clusters = []
  A_queue = queue.Queue()
  A_queue.put(A_root)
  while A_queue.qsize()!=0:
    a = A_queue.get()
    for child in a.children:
      if not child.parent:
        child.parent = a
      A_queue.put(child)
    if a.visited == True:
      continue
    B_queue = queue.Queue()
    B_queue.put(B_root)
    while B_queue.qsize()!=0:
      b = B_queue.get()
      for child in b.children:
        if not child.parent:
          child.parent = b
        B_queue.put(child)
      if b.visited == True:
        continue
      cluster_set = get_cluster_set(a, b, set())
      if cluster_set:
        clustered = Cluster(cluster_set)
        clusters.append(clustered)
  return clusters

def create_cluster_dict(clusters):
  cluster_dic = {}
  for i in range(len(clusters)):
    for node in clusters[i]:
      cluster_dic[node] = i
  return cluster_dic

def print_cluster_dict(cluster_dict):
  return_list = []
  for k,v in cluster_dict.items():
    return_list.append(f'{str(k)}: {v}')
  return ', '.join(return_list)

def get_tree_differences(root, cluster_dict):
  all_nodes = [] 
  diff_nodes = []
  level_traversal(root, 0, all_nodes)
  for i in range(len(all_nodes)):
    for node in all_nodes[i]:
      if node not in cluster_dict.keys():
        diff_nodes.append(node)
  return diff_nodes


def print_tree_difference(diff_a, diff_b):
  plan_1 = "Plan 1 has "
  plan_2 = "Plan 2 has "
  for node in diff_a:
    plan_1 += str(node) + ', '
  for node in diff_b:
    plan_2 += str(node) + ', '
  return plan_1 + plan_2       