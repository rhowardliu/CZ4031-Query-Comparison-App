import sqlparse
from collections import OrderedDict


def print_query_difference(query1, query2):
    dict_a = parse_query(query1)
    dict_b = parse_query(query2)
    a_diff, b_diff = compare_differences(dict_a, dict_b)
    if len(a_diff) == len(b_diff) == 0:
        return 'There were no differences in the queries'

    s = ''
    if len(a_diff) > 0:
        s += '\nQuery 1:'
        for item in a_diff:
            s += f'\n\t- {item}'

    if len(b_diff) > 0:
        s += '\nQuery 2:'
        for item in b_diff:
            s += f'\n\t- {item}'

    return s


def parse_query(query):
    query = ' '.join(query.split('\n'))
    query = ''.join(query.split('\t'))

    parsed = sqlparse.parse(sqlparse.format(query, keyword_case='upper'))[0]
    token_list = parsed.tokens
    token_list = remove_whitespaces(token_list)
    return tokens_to_dict(token_list)


def print_token_list(token_list):
    for t in token_list:
        print(repr(str(t)))


def remove_whitespaces(token_list):
    for i, s in enumerate(token_list):
        if s.is_whitespace:
            token_list.pop(i)
    return token_list


def tokens_to_dict(tokens):
    d = OrderedDict()
    for idx, item in enumerate(tokens):
        if item.value == 'SELECT':
            d['SELECT'] = tokens[idx + 1].value
            continue
        
        if item.is_keyword:
            d[item.value] = tokens[idx + 1].value
            continue
            
        if isinstance(item, sqlparse.sql.Where):
            tmp = item.value[6:]  # delete "WHERE " from the value
            d['WHERE'] = tmp  # parse for the "AND"s?
            continue
    return d


def compare_differences(dict_a, dict_b):
    a_diff = []
    b_diff = []

    for key, a_value in dict_a.items():
        if key in dict_b:
            if a_value != dict_b[key]:
                a_diff.append(f'{key} clause with parameters {a_value}')
                b_diff.append(f'{key} clause with parameters {dict_b[key]}')
        else:
            a_diff.append(f'{key} clause with parameters: {a_value}')

    for key, b_value in dict_b.items():
        if key not in dict_a:
            b_diff.append(f'{key} clause with parameters: {b_value}')

    return a_diff, b_diff
