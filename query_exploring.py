import sql_results as sr
import vocalizer as v


def printNodeAttributes(node):
  for key in node.__dict__:
    print("{key}='{value}'".format(key=key, value=node.__dict__[key]))


def printNLP(json):
  for line in v.get_text(json):
    print(line)

root = v.parse_json(sr.q4)
root = v.simplify_graph(root)
level_1 = root.children
level_2 = level_1[0].children
level_3 = level_2[0].children
level_4 = level_3[0].children
level_5 = level_4[0].children

printNLP(sr.q18)



# printNodeAttributes(root)
[printNodeAttributes(n) for n in level_4]




