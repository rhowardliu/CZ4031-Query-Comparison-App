# CZ4031-Query-Comparison-App

The algorithm works by creating Clusters between the Query Execution Plan Graphs of 2 queries. 

A Cluster is defined as the largest possible set of connected, common nodes between 2 queries. For example,
in the following graph, the Cluster is the set of all nodes except for the last node. If the 2 queries are the same, the cluster should be the entire 
