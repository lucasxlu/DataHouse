from collections import defaultdict
from itertools import combinations
from sys import stdout


class cached_property(object):
    """A cached property only computed once
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class Base(object):
    """A base workflow for Apriori algorithm
    """

    def _before_generate_frequent_itemset(self):
        """Invoked before generate_frequent_itemset()
        """
        pass

    def _after_generate_frequent_itemset(self):
        """Invoked before generate_frequent_itemset()
        """
        pass

    def generate_frequent_itemset(self):
        """Generate and return frequent itemset
        """
        raise NotImplementedError("generate_frequent_itemset(self) need to be implemented.")

    def _before_generate_rule(self):
        """Invoked before generate_frequent_itemset()
        """
        pass

    def _after_generate_rule(self):
        """Invoked before generate_frequent_itemset()
        """
        pass

    def generate_rule(self):
        """Generate and return rule
        """
        raise NotImplementedError("generate_rule(self) need to be implemented.")

    def run(self):
        """Run Apriori algorithm and return rules
        """
        # generate frequent itemset
        self._before_generate_frequent_itemset()
        self.generate_frequent_itemset()
        self._after_generate_frequent_itemset()
        # generate rule
        self._before_generate_rule()
        self.generate_rule()
        self._after_generate_rule()


class Apriori(Base):
    def __init__(self, transaction_list, minsup, minconf, selected_items=None):
        """Initialization
        :param transaction_list: a list cantains transaction
        :param minsup: minimum support
        :param minconf: minimum confidence
        :param selected_items: selected items in frequent itemset, default `None`
        """
        self.transaction_list = transaction_list
        self.transaction_list_full_length = len(transaction_list)
        self.minsup = minsup
        self.minconf = minconf
        if selected_items is not None and selected_items is not []:
            self.selected_items = frozenset(selected_items)
        else:
            self.selected_items = None

        self.frequent_itemset = dict()
        # support for every frequent itemset
        self.frequent_itemset_support = defaultdict(float)
        # convert transaction_list
        self.transaction_list = list([frozenset(transaction) \
                                      for transaction in transaction_list])

        self.rule = []

    def set_selected_items(self, selected_items):
        """Set selected items
        """
        self.selected_items = frozenset(selected_items)

    @cached_property
    def items(self):
        """Return all items in the self.transaction_list
        """
        items = set()
        for transaction in self.transaction_list:
            for item in transaction:
                items.add(item)
        return items

    def filter_with_minsup(self, itemsets):
        """Return subset of itemsets which satisfies minsup
        and record their support
        """
        local_counter = defaultdict(int)
        for itemset in itemsets:
            for transaction in self.transaction_list:
                if itemset.issubset(transaction):
                    local_counter[itemset] += 1
        # filter with counter
        result = set()
        for itemset, count in local_counter.items():
            support = float(count) / self.transaction_list_full_length
            if support >= self.minsup:
                result.add(itemset)
                self.frequent_itemset_support[itemset] = support
        return result

    def _after_generate_frequent_itemset(self):
        """Filter frequent itemset with selected items
        """
        if self.selected_items is None:
            return
        local_remove = []
        for key, val in self.frequent_itemset.items():
            for itemset in val:
                if not self.selected_items.issubset(itemset):
                    local_remove.append((key, itemset))
        for (key, itemset) in local_remove:
            self.frequent_itemset[key].remove(itemset)

    def generate_frequent_itemset(self):
        """Generate and return frequent itemset
        """

        def _apriori_gen(itemset, length):
            """Return candidate itemset with given itemset and length
            """
            # simply use F(k-1) x F(k-1) (itemset + itemset)
            return set([x.union(y) for x in itemset for y in itemset \
                        if len(x.union(y)) == length])

        k = 1
        current_itemset = set()
        # generate 1-frequnt_itemset
        for item in self.items: current_itemset.add(frozenset([item]))
        self.frequent_itemset[k] = self.filter_with_minsup(current_itemset)
        # generate k-frequent_itemset
        while True:
            k += 1
            current_itemset = _apriori_gen(current_itemset, k)
            current_itemset = self.filter_with_minsup(current_itemset)
            if current_itemset != set([]):
                self.frequent_itemset[k] = current_itemset
            else:
                break
        return self.frequent_itemset

    def _generate_rule(self, itemset, frequent_itemset_k):
        """Generate rule with F(k) in DFS style
        """
        # make sure the itemset has at least two element to generate the rule
        if len(itemset) < 2:
            return
        for element in combinations(list(itemset), 1):
            rule_head = itemset - frozenset(element)
            confidence = self.frequent_itemset_support[frequent_itemset_k] / \
                         self.frequent_itemset_support[rule_head]
            if confidence >= self.minconf:
                rule = ((rule_head, itemset - rule_head), confidence)
                # if rule not in self.rule, add and recall _generate_rule() in DFS
                if rule not in self.rule:
                    self.rule.append(rule);
                    self._generate_rule(rule_head, frequent_itemset_k)

    def generate_rule(self):
        """Generate and return rule
        """
        # generate frequent itemset if not generated
        if len(self.frequent_itemset) == 0:
            self.generate_frequent_itemset()
        # generate in DFS style
        for key, val in self.frequent_itemset.items():
            if key == 1:
                continue
            for itemset in val:
                self._generate_rule(itemset, itemset)
        return self.rule

    def print_frequent_itemset(self):
        """Print out frequent itemset
        """
        stdout.write('======================================================\n')
        stdout.write('Frequent itemset:\n')
        for key, val in self.frequent_itemset.items():
            # stdout.write('frequent itemset size of {0}:\n'.format(key))
            for itemset in val:
                stdout.write('(')
                stdout.write(', '.join(itemset))
                stdout.write(')')
                stdout.write('  support = {0}\n'.format(round(self.frequent_itemset_support[itemset], 3)))
        stdout.write('======================================================\n')

    def print_rule(self):
        """Print out rules
        """
        stdout.write('======================================================\n')
        stdout.write('Rules:\n')
        for rule in self.rule:
            head = rule[0][0]
            tail = rule[0][1]
            confidence = rule[1]
            stdout.write('(')
            stdout.write(', '.join(head))
            stdout.write(')')
            stdout.write(' ==> ')
            stdout.write('(')
            stdout.write(', '.join(tail))
            stdout.write(')')
            stdout.write('  confidence = {0}\n'.format(round(confidence, 3)))
        stdout.write('======================================================\n')


class ImprovedApriori(Apriori):
    """Use Hash to filter frequent itemsets
    """

    def filter_with_minsup(self, itemsets):
        """Return subset of itemset which satisfies minsup
        and record their support
        """
        for itemset in itemsets:
            k = len(itemset)
            break
        local_counter = defaultdict(int)
        for transaction in self.transaction_list:
            for itemset in combinations(list(transaction), k):
                if frozenset(itemset) in itemsets:
                    local_counter[frozenset(itemset)] += 1
        # filter with counter
        result = set()
        for itemset, count in local_counter.items():
            support = float(count) / self.transaction_list_full_length
            if support >= self.minsup:
                result.add(itemset)
                self.frequent_itemset_support[itemset] = support
        return result


def read_json(json_filepath):
    import json
    json_str = open(json_filepath, mode='r', encoding='utf-8-sig').read()
    json_obj = json.loads(json_str)
    from pprint import pprint
    pprint(json_obj)


if __name__ == '__main__':
    read_json('movie.json')
    # dataset1 = [
    #     ['bread', 'milk'],
    #     ['bread', 'diaper', 'beer', 'egg'],
    #     ['milk', 'diaper', 'beer', 'cola'],
    #     ['bread', 'milk', 'diaper', 'beer'],
    #     ['bread', 'milk', 'diaper', 'cola'],
    # ]
    #
    # minsup = minconf = 0.5
    #
    # apriori = Apriori(dataset1, minsup, minconf)
    # apriori.run()
    # apriori.print_frequent_itemset()
    # apriori.print_rule()
