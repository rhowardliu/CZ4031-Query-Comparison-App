# CZ4031-Query-Comparison-App

## Overview
The Query Comparison App takes in 2 different PosgreSQL Queries and lists the differences between the the resulting Query Execution Plans as well as the differences in the SQL queries.

## Algorithm

The algorithm works by identifying Clusters between the Query Execution Plan (QEP) Graphs of 2 queries. 

A Cluster is defined as the largest possible set of connected, common nodes between 2 queries. Hence, by identifying the Clusters between 2 QEPs, we can also identify the differences by finding the nodes which aren't in any Clusters. Then, we convert the nodes into plain text explanations and list the differences.


### QEP Processing
##### Cluster Definition

Clusters are the largest possible set of connected, common nodes between 2 queries.
For example, in the following graph, the Cluster is the set of the blue nodes (without repetition).


<img src="https://raw.githubusercontent.com/rhowardliu/CZ4031-Query-Comparison-App/master/images/cluster1.png" width="500"/></a>

If the 2 queries are the same, the cluster should be the entire graph.

##### Creating Clusters
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

##### Rationale for Clusters
A naive way to identify differences between 2 QEPs is to check if, for every node in A, that same node exists in B. However, blindly checking for the existence of the node in the other graph is not an accurate way to determine differences. For example, 2 graphs can have the same node but in completely different places and hence these should not be identified as the same. Another example is if 2 graphs have the same few nodes but in a different order and hence should also not be identified as the same. Clusters are sensitive to the structure of the nodes and hence by using clusters, we can avoid this situation.

##### Parsing the QEP
The algorithm starts at the root node of the 2 Query Execution Graphs, say A and B. For every node in A not in a cluster, it checks if there is a corresponding cluster with all the nodes in B not already in a cluster, using the aforementioned method above. Everytime a cluster is found, the corresponding nodes are marked and will not be checked in subsequent iterations.

After the entire QEP has been parsed and the clusters generated, the algorithm creates a cluster dictionary with the key being the node and the value being the cluster number. This allows for O(1) look up.

##### Generating the QEP differences
Once the clusters have been generated, the algorithm look through all the nodes in the 2 graphs individually and checks if each node is in any cluster using the cluster dictionary. If not, the node will be identified as a difference node for that graph plan.


### Query Processing

##### Parsing the Query

##### Generating the SQL differences
---
### Printing the differences
Finally, the algorithm uses basic rule based formatting to print out different statements in the following format:
```
Plan 1 has 
  *list of graph differences*
  
While Plan 2 has
  *list of graph differences*
  
This can be explained by the differences in queries:
  *list of SQL differences*
```
An example output is:
```
Plan 1 has
    -Index Scan on relation "lineitem", with filter (l_shipdate > '1995-03-21'::date)

While Plan 2 has
    -Index Scan on relation "lineitem"

This can be explained by the differences in queries:

Query 1:
 - WHERE clause with parameters c_mktsegment = 'HOUSEHOLD' AND c_custkey = o_custkey AND l_orderkey = o_orderkey AND o_orderdate < date '1995-03-21' AND l_shipdate > date '1995-03-21' 
Query 2:
 - WHERE clause with parameters c_mktsegment = 'HOUSEHOLD' AND c_custkey = o_custkey AND l_orderkey = o_orderkey AND o_orderdate < date '1995-03-21'
```
