class Cluster(object):
    """docstring for Cluster"""

    def __init__(self, clusterSet):
        super(Cluster, self).__init__()
        self.clusterSet = clusterSet
        self.head = self.getHead()
        self.leaves = self.getLeaves()

    def getLeaves(self):
        leaves = []
        for node in self.clusterSet:
            isLeaf = True
            for child in node.children:
                if child in self.clusterSet:
                    isLeaf = False
            if isLeaf:
                leaves.append(node)
        return leaves

    def getHead(self):
        for node in self.clusterSet:
            if node.parent not in self.clusterSet:
                return node
        return None

    def __str__(self):
        return ','.join(map(str, self.clusterSet))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.clusterSet == other.clusterSet
        else:
            return False

    def __len__(self):
        return len(self.clusterSet)

    def __iter__(self):
        return iter(self.clusterSet)
