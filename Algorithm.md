# CZ4031-Query-Comparison-App

## Overview
The Query Comparison App takes in 2 different PosgreSQL Queries and lists the differences between the the resulting Query Execution Plans as well as the differences in the SQL queries.

## Algorithm

The algorithm works by identifying Clusters between the Query Execution Plan (QEP) Graphs of 2 queries. 

A Cluster is defined as the largest possible set of connected, common nodes between 2 queries. Hence, by identifying the Clusters between 2 QEPs, we can also identify the differences by finding the nodes which aren't in any Clusters. Then, we convert the nodes into plain text explanations and list the differences.
### QEP Processing
#### Cluster Definition

Clusters are the largest possible set of connected, common nodes between 2 queries.
For example, in the following graph, the Cluster is the set of all nodes except for the last node.

__INSERT CLUSTER GRAPH__

If the 2 queries are the same, the cluster should be the entire graph.

#### Creating Clusters
The algorithm finds clusters by checking 2 nodes and seeing if they are the same. Nodes are defined as similar if they have the same values for the following attributes:
* Node Type
* Relation Name
* Group Key
* Sort Key
* Join Type
* Index Name
* Hash Cond
* Table Filter
* Merge Cond
* Recheck Cond
* Join Filter
* Partial Mode

Then, if the nodes are the same, check that all the children nodes are the same and if they are, recursively add their children into the cluster.

#### Parsing the QEP
The algorithm starts at the root node of the 2 Query execution Graphs, say A and B. For every node in A not in a cluster, it checks if there is a corresponding cluster from all the nodes in B not already in a cluster, using the aforementioned method above. Everytime a cluster is found, the corresponding nodes are marked and will not be checked in subsequent iterations.

After the entire QEP has been parsed and the clusters generated, the algorithm creates a cluster dictionary with the key being the node and the value being the cluster it belongs. This allows for O(1) look up.

#### Generating the QEP differences
Once the clusters have been generated, the algorithm look through all the nodes in the 2 graphs individually and checks if they are in any cluster using the cluster dictionary. If they aren't, they will be stored as differences for the next step.
     
### Query Processing

#### Parsing the Query

#### Generating the SQL differences

### Printing the differences
Finally, the algorithm uses basic rule based formatting to print out different statements 

differences in the following format:
```
Plan 1 has 
  *list of graph differences*
While Plan 2 has
  *list of graph differences*
This is because of 
  *list of SQL differences*
```
