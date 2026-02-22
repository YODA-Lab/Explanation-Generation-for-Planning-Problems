from z3 import *
from utils import *
import encoder
from pddl_adapter import PlanningProblem

if __name__ == '__main__':
    domain_agent = "./blocksworld/domain.pddl"
    problem_agent = "./blocksworld/pb1.pddl"

    domain_human = "./blocksworld/domain_human.pddl"
    problem_human = "./blocksworld/pb1.pddl"

    # Encode agent KB:
    encoder_agent = encoder.EncodeKB(domain_agent, problem_agent, length=2)
    KBa = encoder_agent.knowledge_base()

    # Encode human KB:
    encoder_human = encoder.EncodeKB(domain_human, problem_human, length=2)
    KBh = encoder_human.knowledge_base()

    # Get KB model, and plan:
    # print(KBa.model())
    print(KBa.plan())




