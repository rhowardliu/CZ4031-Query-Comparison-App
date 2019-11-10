
class Cluster(object):
  """docstring for Cluster"""
  def __init__(self, clusterSet):
    super(Cluster, self).__init__()
    self.cluster = self.sortClusterSet(clusterSet)
    self.head = self.cluster[0]
    self.leaves = self.getLeaves()


  def getLeaves(self):
    leaves = []
    for node in self.cluster:
      isLeaf = True
      for child in node.children:
        if child in self.cluster:
          isLeaf = False
      if isLeaf:
        leaves.append(node)
    return leaves


  def sortClusterSet(self, clusterSet):
    cluster = []
    for node in clusterSet:
      if node.parent in cluster:
        parent_index = cluster.index(node.parent)
        cluster.insert(parent_index+1, node)
        continue
      if node.children:
        if len(node.children) == 2:
          if node.children[0] and node.children[1] in cluster:
            bigger_index = max(cluster.index(node.children[0]), cluster.index(node. children[1]))
            smaller_index = min(cluster.index(node.children[0]), cluster.index(node. children[1]))
            bigchild = cluster[bigger_index]
            cluster.remove(bigchild)
            cluster.insert(smaller_index, bigchild)
            cluster.insert(smaller_index, node)
            continue
          elif node.children[1] in cluster:
            child_index = cluster.index(node.children[0])
            cluster.insert(child_index, node)
            continue
        if node.children[0] in cluster:
          child_index = cluster.index(node.children[0])
          cluster.insert(child_index, node)
          continue
      cluster.append(node)
    return cluster


  def __str__(self):
    return ','.join(map(str, self.cluster))

  def __eq__(self, other):
    if isinstance(other, self.__class__):
        return self.cluster == other.cluster
    else:
      return False

  def __len__(self):
    return len(self.cluster)


