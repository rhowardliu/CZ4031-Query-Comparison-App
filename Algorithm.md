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
A naive way to identify differences between 2 QEPs is to check if, for every node in A, that same node exists in B. However, blindly checking for the existence of the node in the other graph is not the best way to determine differences as it does not allow us compare differences that are related. As seen in the diagram, graph A has the orange node in between clusters 1 and 2 whereas Graph B has the purple and green nodes in between clusters 1 and 2. Using clusters allow us to identify and compare the transformation between different nodes, which would not have otherwise been possible in the naive implementation.

<img src="https://raw.githubusercontent.com/rhowardliu/CZ4031-Query-Comparison-App/master/images/cluster2.png" width="500"/></a>

Although not fully implemented in this project, the clustering algorithm provides the foundation for future work in this regard.

##### Parsing the QEP
The algorithm starts at the root node of the 2 Query Execution Graphs, say A and B. For every node in A not in a cluster, it checks if there is a corresponding cluster with all the nodes in B not already in a cluster, using the aforementioned method above. Everytime a cluster is found, the corresponding nodes are marked and will not be checked in subsequent iterations.

After the entire QEP has been parsed and the clusters generated, the algorithm creates a cluster dictionary with the key being the node and the value being the cluster number. This allows for O(1) look up.

##### Generating the QEP differences
Once the clusters have been generated, the algorithm look through all the nodes in the 2 graphs individually and checks if each node is in any cluster using the cluster dictionary. If not, the node will be identified as a difference node for that graph plan. 


### Query Processing

##### Parsing the Query
We make use of the `sqlparse` library to parse the SQL queries. We parse out the top level keywords such as `SELECT` and `WHERE`, and partition the query into dictionaries.

A sample parsed query looks like this:
```
{'SELECT': 'sum(l_extendedprice * l_discount) AS revenue',
 'FROM': 'lineitem',
 'WHERE': "l_shipdate >= date '1995-01-01' AND l_shipdate < date '1995-01-01' + interval '1' YEAR AND l_discount BETWEEN 0.09 - 0.01 AND 0.09 + 0.01 AND l_quantity < 24 ",
 'LIMIT': '1'}
```

##### Generating the Query differences
By parsing each query dictionary, we identify the differences in key/value pairs and print out all the differences between the 2 SQL queries

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
