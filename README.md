# Explanation Generation for Planning Problems

Code repository accompanying the JAIR paper:

> **A Logic-Based Explanation Generation Framework for Classical and Hybrid Planning Problems**
> Stylianos Loukas Vasileiou, William Yeoh, Tran Cao Son, Ashwin Kumar, Michael Cashmore, Daniele Magazzeni
>
> Journal of Artificial Intelligence Research, Vol. 73, pp. 1473–1534, 2022.
> [Paper](https://jair.org/index.php/jair/article/view/13431)

## Overview

This system generates logic-based explanations for classical planning problems. Given an agent's planning domain and a human's (possibly incomplete) model of that domain, it identifies the minimal information needed to explain why the agent's plan is correct.

The approach encodes PDDL planning domains into propositional logic using Z3 (SAT/SMT solver), then uses algorithms to compute explanations as minimal knowledge updates.

## Repository Structure

```
├── main.py              # Entry point — runs the blocks world example
├── encoder.py           # Encodes PDDL domains into Z3 propositional logic
├── pddl_adapter.py      # Adapts pddlpy output into grounded planning problems
├── algorithm.py         # Explanation generation algorithms (belief revision, entailment)
├── utils.py             # Z3 utilities and planning KB class
├── pddlpy/              # PDDL parser (bundled)
└── blocksworld/         # Example domain
    ├── domain.pddl          # Agent's domain (full model)
    ├── domain_human.pddl    # Human's domain (incomplete model)
    └── pb1.pddl             # Problem instance
```

## Installation

Requires Python 3.8+.

```bash
pip install -r requirements.txt
```

## Usage

Run the blocks world example:

```bash
python main.py
```

This encodes both the agent's and human's planning domains, solves for a plan, and prints it.

To use with your own domains, provide PDDL domain and problem files:

```python
import encoder

kb = encoder.EncodeKB("path/to/domain.pddl", "path/to/problem.pddl", length=2)
planning_kb = kb.knowledge_base()
print(planning_kb.plan())
```

## Citation

```bibtex
@article{Vasileiou2022,
  title={A Logic-Based Explanation Generation Framework for Classical and Hybrid Planning Problems},
  author={Vasileiou, Stylianos Loukas and Yeoh, William and Son, Tran Cao and Kumar, Ashwin and Cashmore, Michael and Magazzeni, Daniele},
  journal={Journal of Artificial Intelligence Research},
  volume={73},
  pages={1473--1534},
  year={2022}
}
```
