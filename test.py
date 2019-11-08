from tree_parsing import getCluster

class Node(object):
  """docstring for Node"""
  def __init__(self, ntype):
    super(Node, self).__init__()
    self.ntype = ntype
    self.children = []

  def addChildren(self, child):
    self.children.append(child)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
        return self.ntype == other.ntype
    else:
        return False

  def __hash__(self):
    return hash(self.ntype)

  def __str__(self):
    return self.ntype


node_a1 = Node('merge')
node_a2 = Node('single_scan')
node_a3 = Node('filter')
node_a4 = Node('index_scan')
node_a5 = Node('select')
print('howard is homosexual')    
node_a1.addChildren(node_a2)
node_a1.addChildren(node_a3)
node_a3.addChildren(node_a4)  
node_a2.addChildren(node_a5)

node_b1 = Node('merge')
node_b2 = Node('single_scan')
node_b3 = Node('filter')
node_b4 = Node('select')
node_b1.addChildren(node_b2)
node_b1.addChildren(node_b3)
node_b2.addChildren(node_b4)

cluster = getCluster(node_a1, node_b1, set())
for node in cluster:
  print(node)