import queue
import pdb

class Cluster(object):
  """docstring for Cluster"""
  def __init__(self, clusterSet):
    super(Cluster, self).__init__()
    self.cluster = []
    for node in clusterSet:
      if node.parent in self.cluster:
        parent_index = self.cluster.index(node.parent)
        self.cluster.insert(parent_index+1, node)
        continue
      if node.children:
        if len(node.children) == 2:
          if node.children[0] and node.children[1] in self.cluster:
            bigger_index = max(self.cluster.index(node.children[0]), self.cluster.index(node. children[1]))
            smaller_index = min(self.cluster.index(node.children[0]), self.cluster.index(node. children[1]))
            bigchild = self.cluster[bigger_index]
            self.cluster.remove(bigchild)
            self.cluster.insert(smaller_index, bigchild)
            self.cluster.insert(smaller_index, node)
            continue
          elif node.children[1] in self.cluster:
            child_index = self.cluster.index(node.children[0])
            self.cluster.insert(child_index, node)
            continue
        if node.children[0] in self.cluster:
          child_index = self.cluster.index(node.children[0])
          self.cluster.insert(child_index, node)
          continue
      self.cluster.append(node)

  def __str__(self):
    return ','.join(map(str, self.cluster))

  def __eq__(self, other):
    if isinstance(other, self.__class__):
        return self.cluster == other.cluster
    else:
      return False

  def __len__(self):
    return len(self.cluster)



def get_cluster(a, b, cluster_grp):
  if a!=b:
    return cluster_grp
  if a.children and b.children:
    a_set = {x for x in a.children}
    b_set = {x for x in b.children}
    if a_set == b_set:
      if len(a_set) == 1:
        cluster_grp = cluster_grp.union(get_cluster(a.children[0], b.children[0], set()))
      else:
        if a.children[0] == b.children[0]:
          cluster_1 = get_cluster(a.children[0], b.children[0], set())
          cluster_2 = get_cluster(a.children[1], b.children[1], set())
        else:
          cluster_1 = get_cluster(a.children[0], b.children[1], set())
          cluster_2 = get_cluster(a.children[1], b.children[0], set())
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
      cluster = get_cluster(a, b, set())
      if cluster:
        clusters.append(cluster)
        break
  return clusters

