import re


class SQLParser:
    #"select room, title from talks.csv where time='09:00 AM'"
    #Project(['room', 'title'], ['room', 'title'], Filter(Eq(Field('time'), Value('09:00 AM')), Scan('talks.csv')))
    def __init__(self):
        self.patterns = {
            'select': r'select\s+(.*?)\s+from\s+(.*?)\s+where\s+(.*)',
            'filter': r'(\w+)\s*=\s*\'(.*?)\'',
        }

    def parse_sql(self, query):
        select_match = re.match(self.patterns['select'], query)
        if select_match:
            fields = [field.strip() for field in select_match.group(1).split(',')]
            table = select_match.group(2).strip()
            condition_match = re.match(self.patterns['filter'], select_match.group(3).strip())
            if condition_match:
                field_name = condition_match.group(1)
                value = condition_match.group(2)
                return Project(fields, fields, Filter(Eq(Field(field_name), Value(value)), Scan(table)))
            else:
                return Project(fields, fields, Scan(table))
        else:
            return "Invalid SQL query"


class Node:
    pass


class Project(Node):
    def __init__(self, fields, output_fields, child):
        self.fields = fields
        #self.output_fields = output_fields
        self.child = child


class Filter(Node):
    def __init__(self, condition, child):
        self.condition = condition
        self.child = child


class Eq(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Field(Node):
    def __init__(self, name):
        self.name = name


class Value(Node):
    def __init__(self, value):
        self.value = value


class Scan(Node):
    def __init__(self, table):
        self.table = table


parser = SQLParser()


def print_query(parsed_query):
    if isinstance(parsed_query, Project):
        return "Project({}, {})".format(parsed_query.fields,
                                            print_query(parsed_query.child))
    elif isinstance(parsed_query, Filter):
        return "Filter({}, {})".format(print_query(parsed_query.condition), print_query(parsed_query.child))
    elif isinstance(parsed_query, Eq):
        return "Eq({}, {})".format(print_query(parsed_query.left), print_query(parsed_query.right))
    elif isinstance(parsed_query, Field):
        return "Field('{}')".format(parsed_query.name)
    elif isinstance(parsed_query, Value):
        return "Value('{}')".format(parsed_query.value)
    elif isinstance(parsed_query, Scan):
        return "Scan('{}')".format(parsed_query.table)
    else:
        return parsed_query


# Example usage:
query = "select room, title from talks.csv where time='09:00 AM'"
parsed_query = parser.parse_sql(query)
print(print_query(parsed_query))
