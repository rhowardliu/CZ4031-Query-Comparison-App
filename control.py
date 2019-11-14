import psycopg2
import tree_parsing as tp
import db_connect as db
import vocalizer as v

def add_explain_analyze(query):
  return 'EXPLAIN (ANALYZE true, FORMAT json) ' + query

def get_query_plan(cur,query):
  cur.execute(query)
  res = cur.fetchall()
  return res[0][0][0]

def generate_differences(query_1, query_2):
  conn = db.get_sql_cursor()
  cur = conn.cursor()
  p_1_json = get_query_plan(cur, add_explain_analyze(query_1))
  p_2_json = get_query_plan(cur, add_explain_analyze(query_2))
  p_1 = v.parse_json(p_1_json)
  p_2 = v.parse_json(p_2_json)
  clusters = tp.parse_tree(p_1, p_2)
  cluster_dict = tp.create_cluster_dict(clusters)
  diff_1 = tp.get_tree_differences(p_1,cluster_dict)
  diff_2 = tp.get_tree_differences(p_2,cluster_dict)
  print(tp.print_tree_difference(diff_1, diff_2))
  cur.close()
  conn.close()



# self.pushButton.clicked.connect(self.onClickButton)

# def onClickButton(self):
#     query = self.plainTextEdit.toPlainText()
#     tree = qp.query_to_tree(query)
#     self.textBrowser.setText(tree)
#     print(query)



if __name__ == '__main__':
  test_1 = '''select
  l_orderkey,
  sum(l_extendedprice * (1 - l_discount)) as revenue,
  o_orderdate,
  o_shippriority
from
  customer,
  orders,
  lineitem
where
  c_mktsegment = 'HOUSEHOLD'
  and c_custkey = o_custkey
  and l_orderkey = o_orderkey
  and o_orderdate < date '1995-03-21'
  and l_shipdate > date '1995-03-21'
group by
  l_orderkey,
  o_orderdate,
  o_shippriority
order by
  revenue desc,
  o_orderdate
limit 10;
'''

test_2 = '''select
  l_orderkey,
  sum(l_extendedprice * (1 - l_discount)) as revenue,
  o_orderdate,
  o_shippriority
from
  customer,
  orders,
  lineitem
where
  c_mktsegment = 'HOUSEHOLD'
  and c_custkey = o_custkey
  and l_orderkey = o_orderkey
group by
  l_orderkey,
  o_orderdate,
  o_shippriority
order by
  revenue desc,
  o_orderdate
limit 10;

'''
generate_differences(test_1, test_2)