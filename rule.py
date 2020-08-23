import dateutil.parser

from elastalert.ruletypes import RuleType, CompareRule

# elastalert.util includes useful utility functions
# such as converting from timestamp to datetime obj
from elastalert.util import ts_to_dt, lookup_es_key

class ArrayChangeRule(CompareRule):
    required_options = set(['tuplecheck', 'tuplefields'])

    def __init__(self, *args):
        super(ArrayChangeRule, self).__init__(*args)
        self.key_tuples = []
        self.last_event = {}

    def add_data(self, data):
        compare_keys    = self.rules['tuplefields']
        compare_values  = self.rules['tuplecheck']

        for event in data:
            key_tuple       = ''

            for key in compare_keys:
                es_key = lookup_es_key(event, key)
                if es_key:
                    key_tuple = (es_key if len(key_tuple) == 0
                                        else '%s/%s' % (key_tuple, es_key))

            if key_tuple in compare_values and not key_tuple in self.key_tuples:
                self.key_tuples.append(key_tuple)
                self.last_event = event

    def garbage_collect(self, timestamp):
        for value in self.rules['tuplecheck']:
            if not value in self.key_tuples:
                self.add_match({'@timestamp' : timestamp})
                break

        self.key_tuples.clear()
        self.last_event = {}

