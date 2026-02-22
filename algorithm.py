from z3 import *
import itertools


def skeptically_entail(a, b):
    s = Solver()
    for i in range(len(a)):
        s.reset()
        s.add(Implies(a[i], b))
        output = str(s.check())
        if output != "sat":
            return False
    return True


def credulously_entail(a, b):
    s = Solver()
    for i in range(len(a)):
        s.reset()
        s.add(Implies(a[i], b))
        output = str(s.check())
        if output == "sat":
            return True
    return False


def update(kb, exp):
    subsets = []
    for length in range(0, len(kb)):
        for subset in itertools.combinations(kb, length):
            possible_kb = list(set().union(subset, exp))
            subsets.append(possible_kb)
    subsets = sort(subsets)
    s = Solver()
    for subset in subsets:
        s.reset()
        s.add(And(sub for sub in subset))
        output = String(s.check())
        if output == "sat":
            return subset
    return kb


def sort(q):
    costs = []
    for i in q:
        costs.append(len(i))
    sorted_q = [x for _, x in sorted(zip(costs, q))]
    return sorted_q


def most_preferred(kba, kbh, phi_s, phi_c):
    if credulously_entail(kbh, phi_c) and skeptically_entail(kbh, phi_s):
        return []
    else:
        q = PriorityQueue()
        checked = []
        condition = True
        while condition:
            epi = q.dequeue()
            checked.append(epi)
            new_kbh = update(kbh, epi)
            if credulously_entail(new_kbh, phi_c) and skeptically_entail(new_kbh, phi_s):
                return epi
            else:
                for a in kba:
                    union = list(set().union(epi, a))
                    if a not in kbh and union not in checked:
                        v = cost_function(union)
                        q = q.enqueue(union)
            if len(q) == 0:
                condition = False


def get_SAT_model(kb):
    expressions = [expression for expression in kb]
    return And(expressions)


def extract_relevant_literals(kb, plan):
    result = []
    for i in kb:
        if i in plan:
            result.append(i)
    return result


def extract_partial_model(kba, plan):
    mu = []
    m = get_SAT_model(kba)
    lambda_new = extract_relevant_literals(kba, plan)
    for (l, t) in m:
        if l in lambda_new:
            mu = list(set().union(mu, [(l, t)]))
    return mu


def cost_function(a):
    return len(a)


class PriorityQueue:

    def __init__(self):
        self.queue = [[]]

    def enqueue(self, exp):
        self.queue.append(exp)
        self.queue = sort(self.queue)
        return self

    def dequeue(self):
        element = self.queue[0]
        self.queue.remove(element)
        return element

    def get_queue(self):
        return self.queue


def main():
    print("hi")


if __name__ == '__main__':
    main()
