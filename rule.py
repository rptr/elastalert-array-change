import dateutil.parser

from elastalert.ruletypes import RuleType
from elastalert.util import lookup_es_key

class ArrayChangeRule(RuleType):
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

            if not key_tuple in self.key_tuples:
#               print("Adding tuple " + key_tuple)
                self.key_tuples.append(key_tuple)
                self.last_event = event

        for value in self.rules['tuplecheck']:
#           print("Checking for configured tuple " + value)
            if not value in self.key_tuples:
#               print("MATCH! could not find configured tuple " + value)
                self.add_match({'direction' : 'configured_but_not_found', 'configured_value': value})
                break

        for value in self.key_tuples:
#           print("Checking for Elastic tuple " + value)
            if not value in self.rules['tuplecheck']:
#               print("MATCH! could not find Elastic tuple " + value)
                self.add_match({'direction' : 'elastic_but_not_configured', 'elastic_value': value})
                break


    def get_match_str(self, match):
        if (match['direction'] == 'configured_but_not_found'):
            return "Configured value %s not found in Elastic" % (match['configured_value'])
        else:
            return "Elastic document %s not found in configuration" % (match['elastic_value'])

    def garbage_collect(self, timestamp):
        self.key_tuples.clear()
        self.last_event = {}
