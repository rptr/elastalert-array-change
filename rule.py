import dateutil.parser

from elastalert.ruletypes import RuleType
from elastalert.util import lookup_es_key

class ArrayChangeRule(RuleType):
    required_options = set(['tuplecheck', 'tuplefields'])

    def __init__(self, *args):
        super(ArrayChangeRule, self).__init__(*args)
        self.found_tuples = []

    def add_data(self, data):
        compare_keys    = self.rules['tuplefields']
        compare_values  = self.rules['tuplecheck']

        for event in data:
            key_tuple       = ''

            # Match the values of the defined keys
            # tuplefields:
            # - keyA
            # - keyB
            # - keyC
            # {"keyA" : "A", "keyB" : "B", "keyC" : "C"}
            # to a string in this format
            # A/B/C
            for key in compare_keys:
                es_key = lookup_es_key(event, key)
                if es_key:
                    key_tuple = (es_key if len(key_tuple) == 0
                                        else '%s/%s' % (key_tuple, es_key))

            if not key_tuple in self.found_tuples:
                self.found_tuples.append(key_tuple)

        missing = []

        # Check for expected documents
        for value in self.rules['tuplecheck']:
            if not value in self.found_tuples:
                missing.append(value)

        if len(missing):
            self.add_match({'direction' : 'configured_but_not_found',
                            'missing_values': missing})

        if ('allow_unconfigured' in self.rules and
                self.rules['allow_unconfigured'] == False):
            unexpected = []

            # Check for unexpected documents
            for value in self.found_tuples:
                if not value in self.rules['tuplecheck']:
                    unexpected.append(value)

            if len(unexpected):
                self.add_match({'direction' : 'found_but_not_configured',
                                'unexpected_values': unexpected})

    def get_match_str(self, match):
        if match['direction'] == 'configured_but_not_found':
            return ("Expected document(-s) %s not found in ElasticSearch" %
                    (match['missing_values']))
        elif match['direction'] == 'found_but_not_configured':
            return ("Document(-s) %s not found in rule configuration" %
                    (match['unexpected_values']))

    def garbage_collect(self, timestamp):
        if len(self.rules['tuplecheck']) > 0 and len(self.found_tuples) == 0:
            self.add_match({'direction' : 'configured_but_not_found',
                            'missing_values': self.rules['tuplecheck']})

        self.found_tuples.clear()
