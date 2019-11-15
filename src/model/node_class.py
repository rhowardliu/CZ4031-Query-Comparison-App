from __future__ import print_function
import argparse
import copy
import queue


class Node(object):
    def __init__(self, node_type, group_key, sort_key=None, relation_name=None, schema=None, alias=None, join_type=None, index_name=None, hash_cond=None, table_filter=None, index_cond=None, merge_cond=None, recheck_cond=None, join_filter=None, subplan_name=None, actual_rows=None, actual_time=None):
        self.node_type = node_type
        self.children = []
        self.relation_name = relation_name
        self.schema = schema
        self.alias = alias
        self.group_key = group_key
        self.sort_key = sort_key
        self.join_type = join_type
        self.index_name = index_name
        self.hash_cond = hash_cond
        self.table_filter = table_filter
        self.index_cond = index_cond
        self.merge_cond = merge_cond
        self.recheck_cond = recheck_cond
        self.join_filter = join_filter
        self.subplan_name = subplan_name
        self.actual_rows = actual_rows
        self.actual_time = actual_time
        # extra
        self.visited = False
        self.parent = None
        self.partial_mode = None

    def add_children(self, child):
        self.children.append(child)
    
    def set_output_name(self, output_name):
        if "T" == output_name[0] and output_name[1:].isdigit():
            self.output_name = int(output_name[1:])
        else:
            self.output_name = output_name

    def get_output_name(self):
        if str(self.output_name).isdigit():
            return "T" + str(self.output_name)
        else:
            return self.output_name

    def set_step(self, step):
        self.step = step

    # extra
    def __eq__(self, other):
        # checks
        attributes_to_compare = [
            'node_type', 'relation_name', 'group_key', 'sort_key', 'join_type', 'index_name',
            'hash_cond', 'table_filter', 'merge_cond', 'recheck_cond', 'join_filter', 'partial_mode'
        ]

        for attribute in attributes_to_compare:
            if getattr(self, attribute) != getattr(other, attribute):
                return False

        return True

    def __hash__(self):
        attributes = [
            'node_type', 'relation_name', 'group_key', 'sort_key', 'join_type', 'index_name',
            'hash_cond', 'table_filter', 'merge_cond', 'recheck_cond', 'join_filter', 'partial_mode'
        ]
        
        hash_list = []
        for attr in attributes:
            if attr == 'group_key' or attr == 'sort_key':
                # group and sort keys are lists. Change to tuple before append
                tmp = getattr(self, attr)
                if tmp:
                    hash_list.append(tuple(tmp))
                    continue
            hash_list.append(getattr(self, attr))

        return hash(tuple(hash_list))

    def __str__(self):
        s = ''
        # Index Scan, Seq Scan
        if 'Scan' in self.node_type:
            s += f'{self.node_type} on relation "{self.relation_name}"'
            if self.table_filter:
                s += f', with filter {self.table_filter}'
            return s

        # Hash Join, Merge Join
        if 'Join' in self.node_type:
            if 'Hash' in self.node_type:
                s += f'{self.node_type} (type: {self.join_type}) with Hash Condition {self.hash_cond}'
            elif 'Merge' in self.node_type:
                s += f'{self.node_type} (type: {self.join_type}) with Merge Condition {self.merge_cond}'

            if self.join_filter:
                s += f' and Join Filter {self.join_filter}'

            return s

        # Nested Loop Join
        if self.node_type == 'Nested Loop':
            s += f'{self.node_type} Join (type: {self.join_type})'

            if self.hash_cond:
                s += f' with Hash Condition {self.hash_cond}'

            s += f' on the results from a {self.children[0].node_type} and a {self.children[1].node_type}'

            return s

        # Sort
        if self.node_type == 'Sort':
            return f'Sort on sort keys {self.sort_key}'

        # Limit
        if self.node_type == 'Limit':
            return f'Limit results to {self.plan_rows} rows'


        # Bitmap Heap Scan
        if self.node_type == 'Bitmap Heap Scan':
            return 'Bitmap Heap Scan'

        # Bitmap Index Scan
        if 'Bitmap Index Scan' in self.node_type:
            return f'Bitmap Index Scan with index condition {self.recheck_cond}'

        # Unique
        if self.node_type == 'Unique':
            return 'Unique operation'

        # Aggregate
        if self.node_type == 'Aggregate':
            s += f'Aggregate'
            if self.partial_mode:
                s += f' ({self.partial_mode})'
            s += f' on results from a {self.children[0].node_type}'
            if len(self.children) > 1:
                s += f' and a {self.children[1].node_type}'

            return s

        # Base Case
        s += f"{str(self.node_type)}"
        if len(self.children) > 0:
            s += f' on results from a {self.children[0].node_type}'

        if len(self.children) > 1:
            s += f' and a {self.children[1].node_type}'

        return s
        

# Phase 1
def parse_json(json_obj):
    q = queue.Queue()
    q_node = queue.Queue()
    # json_obj = json.load(open(json_file, 'r'))
    plan = json_obj['Plan']
    q.put(plan)
    q_node.put(None)

    while not q.empty():
        current_plan = q.get()
        parent_node = q_node.get()

        relation_name = schema = alias = group_key = sort_key = join_type = index_name = hash_cond = table_filter \
            = index_cond = merge_cond = recheck_cond = join_filter = subplan_name = actual_rows = actual_time = None
        if 'Relation Name' in current_plan:
            relation_name = current_plan['Relation Name']
        if 'Schema' in current_plan:
            schema = current_plan['Schema']
        if 'Alias' in current_plan:
            alias = current_plan['Alias']
        if 'Group Key' in current_plan:
            group_key = current_plan['Group Key']
        if 'Sort Key' in current_plan:
            sort_key = current_plan['Sort Key']
        if 'Join Type' in current_plan:
            join_type = current_plan['Join Type']
        if 'Index Name' in current_plan:
            index_name = current_plan['Index Name']
        if 'Hash Cond' in current_plan:
            hash_cond = current_plan['Hash Cond']
        if 'Filter' in current_plan:
            table_filter = current_plan['Filter']
        if 'Index Cond' in current_plan:
            index_cond = current_plan['Index Cond']
        if 'Merge Cond' in current_plan:
            merge_cond = current_plan['Merge Cond']
        if 'Recheck Cond' in current_plan:
            recheck_cond = current_plan['Recheck Cond']
        if 'Join Filter' in current_plan:
            join_filter = current_plan['Join Filter']
        if 'Actual Rows' in current_plan:
            actual_rows = current_plan['Actual Rows']
        if 'Actual Total Time' in current_plan:
            actual_time = current_plan['Actual Total Time']
        if 'Subplan Name' in current_plan:
            if "returns" in current_plan['Subplan Name']:
                name = current_plan['Subplan Name']
                subplan_name = name[name.index("$"):-1]
            else:
                subplan_name = current_plan['Subplan Name']

        current_node = Node(
            current_plan['Node Type'], group_key, sort_key, relation_name, schema, alias, join_type,
            index_name, hash_cond, table_filter, index_cond, merge_cond, recheck_cond, join_filter,
            subplan_name, actual_rows, actual_time
        )

        if "Limit" == current_node.node_type:
            current_node.plan_rows = current_plan['Plan Rows']
           
        if "Scan" in current_node.node_type:
            if "Index" in current_node.node_type:
                if relation_name:
                    current_node.set_output_name(relation_name + " with index " + index_name)
            elif "Subquery" in current_node.node_type:
                current_node.set_output_name(alias)
            else:
                current_node.set_output_name(relation_name)

        if "Aggregate" in current_node.node_type:
            current_node.partial_mode = current_plan['Partial Mode']

        if parent_node is not None:
            parent_node.add_children(current_node)
        else:
            head_node = current_node

        if 'Plans' in current_plan:
            for item in current_plan['Plans']:
                # push child plans into queue
                q.put(item)
                # push parent for each child into queue
                q_node.put(current_node)

    return head_node


if __name__ == '__main__':
    args = parser.parse_args()
    steps = get_text(args.json_file)
    # vocalize(steps)
