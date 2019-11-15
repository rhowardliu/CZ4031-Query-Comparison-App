import src.controller.tree_parsing as tp
from src.database.db_connect import DB_Manager
import src.model.node_class as n


class Control(object):

    def __init__(self, ):
        super(Control, self).__init__()
        self.db = DB_Manager()

    def add_explain_analyze(self, query):
        return 'EXPLAIN (ANALYZE true, FORMAT json) ' + query

    def generate_differences(self, query_1, query_2):
        p_1_json = self.db.query(self.add_explain_analyze(query_1))
        p_2_json = self.db.query(self.add_explain_analyze(query_2))
        p_1 = n.parse_json(p_1_json)
        p_2 = n.parse_json(p_2_json)
        clusters = tp.parse_tree(p_1, p_2)
        cluster_dict = tp.create_cluster_dict(clusters)
        diff_1 = tp.get_tree_differences(p_1, cluster_dict)
        diff_2 = tp.get_tree_differences(p_2, cluster_dict)
        diff_statement = tp.print_tree_difference(diff_1, diff_2)
        print(diff_statement)
        return diff_statement