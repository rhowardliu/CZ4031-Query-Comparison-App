import sql_results as sr
import vocalizer as v


def printNode(node):
  print('#### printNode')
  for key in node.__dict__:
    print("{key}='{value}'".format(key=key, value=node.__dict__[key]))
  
def printNodeType(node):
  print(node.node_type)


def printNLP(json):
  for line in v.get_text(json):
    print(line)

root = v.parse_json(sr.q3)
root = v.simplify_graph(root)
level_1 = list(root.children)
print(level_1)
level_2 = [y for x in level_1 for y in x.children ]
print(level_2)
level_3 = list(y for x in level_2 for y in x.children )
print(level_3)
level_4 = list(y for x in level_3 for y in x.children )
print(level_4)
level_5 = list(y for x in level_4 for y in x.children )
print(level_5)
level_6 = list(y for x in level_5 for y in x.children )
print(level_6)
level_7 = list(y for x in level_6 for y in x.children )
print(level_7)
printNLP(sr.q3)



# printNode(root)
[printNodeType(n) for n in level_1]
[printNodeType(n) for n in level_2]
[printNodeType(n) for n in level_3]
[printNodeType(n) for n in level_4]
[printNodeType(n) for n in level_5]
[printNodeType(n) for n in level_6]
[printNodeType(n) for n in level_7]




