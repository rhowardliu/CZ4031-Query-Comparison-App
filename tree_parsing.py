A_group = []
B_group = []

def getCluster(a, b, cluster_grp):
  if a!=b:
    return cluster_grp
  if a.children and b.children:
    a_set = {x for x in a.children}
    b_set = {x for x in b.children}
    if a_set == b_set:
      if len(a_set) == 1:
        cluster_grp = cluster_grp.union(getCluster(a.children[0], b.children[0], set()))
      else:
        if a.children[0] == b.children[0]:
          cluster_1 = getCluster(a.children[0], b.children[0], set())
          cluster_2 = getCluster(a.children[1], b.children[1], set())
        else:
          cluster_1 = getCluster(a.children[0], b.children[1], set())
          cluster_2 = getCluster(a.children[1], b.children[0], set())
        cluster_grp = cluster_grp.union(cluster_1, cluster_2)
  cluster_grp.add(a)
  return cluster_grp


