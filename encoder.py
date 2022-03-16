from pddl_adapter import PlanningProblem
from enum import Enum
from itertools import combinations
import z3
from utils import *
from collections import defaultdict


class EncodeKB(object):

    def __init__(self, dom_file: str, problem_file: str, length=1):
        self._problem = PlanningProblem(dom_file, problem_file)
        self._length = length
        self._KB = self._encode()

    def _encode(self):

        KB_ord = defaultdict(lambda: defaultdict(list))
        actions = self._problem.actions
        fluents = self._problem.fluents
        act_names = set()
        fluent_names = set()
        # opt_query = []



        # 1. encode initial state
        init_state = list(self._problem.initial_state)
        init_state_clauses = []

        for fluent in list(fluents):
            fluent = (fluent[0].upper(),) + fluent[1:]
            if fluent not in init_state:
                fluent = z3.Not(z3.Bool("_".join(fluent) + ('_0')))
            else:
                fluent = z3.Bool("_".join(fluent) + ('_0'))
            init_state_clauses.append(fluent)


        # 2. encode goal state
        goal_state = list(self._problem.goal_state)
        goal_state_clauses = []
        for goal in goal_state:
            goal = z3.Bool("_".join(goal) + '_'+(str(+self._length)))
            goal_state_clauses.append(goal)

        # for h in range(self._length - 1):
        #     for goal in goal_state:
        #         opt_query.append(makeName(goal, h))

        preconds = []
        add_effects = []
        del_effects = []
        frame_axioms = []
        exclusion_axioms = []

        for step in range(self._length):
            # 3. encode actions
            for act in actions:
                if act.effect_pos.issubset(act.precondition_pos):
                    continue

                name = makeName(act, step)
                act_names.add(str(name))

                # preconditions
                for p in act.precondition_pos:
                    # if 'adjacent' in p:
                    #     continue

                    p = "_".join(p) + '_' + (str(step))
                    p = z3.Bool(p.upper())
                    preconds.append(z3.Implies(name, p))
                    # KB_ord[act.operator_name]['preconds'].append(z3.Implies(name, p))
                # positive effects
                for e in act.effect_pos:
                    e = "_".join(e) + '_' + (str(step+1))
                    e = z3.Bool(e.upper())
                    add_effects.append(z3.Implies(name, e))
                    # KB_ord[act.operator_name]['add_eff'].append(z3.Implies(name, e))

                # negative effects
                for ne in act.effect_neg:
                    ne = "_".join(ne) + '_' + (str(step + 1))
                    ne = z3.Not(z3.Bool(ne.upper()))
                    del_effects.append(z3.Implies(name, ne))
                    # KB_ord[act.operator_name]['del_eff'].append(z3.Implies(name, ne))

            # 4. explanatory frame axioms
            for fluent in fluents:
                act_with_pos_effect = []
                act_with_neg_effect = []
                for act in actions:
                    if act.effect_pos.issubset(act.precondition_pos):
                        continue
                    if fluent in act.effect_pos:
                        act_with_pos_effect.append(act)
                    elif fluent in act.effect_neg:
                        act_with_neg_effect.append(act)


                if act_with_pos_effect:
                    a_pos = "_".join(fluent) + '_' + (str(step))
                    a_pos = z3.Not(z3.Bool(a_pos.upper()))
                    b_pos = "_".join(fluent) + '_' + (str(step + 1))
                    b_pos = z3.Bool(b_pos.upper())

                    frame_axioms.append(z3.Implies(z3.And(a_pos, b_pos),
                                   z3.Or([makeName(act, step) for act in act_with_pos_effect])))

                    # KB_ord[fluent[0]]['add_frames'].append(z3.Implies(z3.And(a_pos, b_pos),
                    #                z3.Or([makeName(act, step) for act in act_with_pos_effect])))

                else:
                    frame_axioms.append(z3.Or(makeName(fluent, step), z3.Not(makeName(fluent, step+1))))
                    # KB_ord[fluent[0]]['add_frames'].append(z3.Or(makeName(fluent, step), z3.Not(makeName(fluent, step+1))))



                if act_with_neg_effect:

                    a_neg = "_".join(fluent) + '_' + (str(step))
                    a_neg = z3.Bool(a_neg.upper())
                    b_neg = "_".join(fluent) + '_' + (str(step + 1))
                    b_neg = z3.Not(z3.Bool(b_neg.upper()))

                    frame_axioms.append(z3.Implies(z3.And(a_neg, b_neg),
                                                               z3.Or([makeName(act, step) for act in
                                                                 act_with_neg_effect])))

                    # KB_ord[fluent[0]]['del_frames'].append(z3.Implies(z3.And(a_neg, b_neg),
                    #                                            z3.Or([makeName(act, step) for act in
                    #                                              act_with_neg_effect])))

                else:
                    frame_axioms.append(z3.Or(z3.Not(makeName(fluent, step)), makeName(fluent, step + 1)))
                    # KB_ord[fluent[0]]['del_frames'].append(
                    #     z3.Or(z3.Not(makeName(fluent, step)), makeName(fluent, step + 1)))

            # 5. complete exclusion axiom
            for action_pair in combinations(actions, 2):
                if action_pair[0].effect_pos.issubset(
                        action_pair[0].precondition_pos):
                    continue
                if action_pair[1].effect_pos.issubset(
                        action_pair[1].precondition_pos):
                    continue


                exclusion_axioms.append(z3.Or(z3.Not(makeName(action_pair[0], step)), z3.Not(makeName(action_pair[1], step))))
                # KB_ord["action_excls"]['all'].append(z3.Or(z3.Not(makeName(action_pair[0], step)), z3.Not(makeName(action_pair[1], step))))

        # KB = init_state_clauses + goal_state_clauses + \
        #     preconds + add_effects + del_effects + explanatory_frame_axioms + \
        #     complete_exclusion_axiom

        KB = planningKB(fluent_names, act_names, init_state_clauses, goal_state_clauses, preconds, add_effects, del_effects, frame_axioms, exclusion_axioms)

        return KB


    def knowledge_base(self):
        return self._KB
