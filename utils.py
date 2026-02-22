import re
from z3 import *


def makeName(name, step):
    v = str(name)
    v = re.sub('[\(\)\{\}\[\]<>\'\,\(\)-]', ' ', v)
    v = v.strip()
    v = v.upper()
    v = '_'.join(v.split())
    return Bool(v + '_' + (str(step)))


def remove_steps(name):
    v = str(name).lower()
    v = re.sub('[\\{\}<>-_()]', ' ', v)
    v = v.replace('-', '')
    v = v.strip()
    v = v[:v.find(" ")]
    return str(v)


def getStep(var_name):
    [_, step] = var_name.split("_")
    return int(step)





def find(key, dictionary):
	for k, v in dictionary.items():
		if k == key:
			yield v
		elif isinstance(v, dict):
			for result in find(key, v):
				yield result
		elif isinstance(v, list):
			for d in v:
				if isinstance(d, dict):
					for result in find(key, d):
						yield result


def iterate_all(iterable, returned="key"):
	"""Returns an iterator that returns all keys or values
	   of a (nested) iterable.

	   Arguments:
		   - iterable: <list> or <dictionary>
		   - returned: <string> "key" or "value"

	   Returns:
		   - <iterator>
	"""

	if isinstance(iterable, dict):
		for key, value in iterable.items():
			if returned == "key":
				yield key
			elif returned == "value":
				if not (isinstance(value, dict) or isinstance(value, list)):
					yield value
			else:
				raise ValueError("'returned' keyword only accepts 'key' or 'value'.")
			for ret in iterate_all(value, returned=returned):
				yield ret
	elif isinstance(iterable, list):
		for el in iterable:
			for ret in iterate_all(el, returned=returned):
				yield ret






def NestedDictValues(d):
	for v in d.values():
		if isinstance(v, dict):
			yield from NestedDictValues(v)
		else:
			yield v


class AstRefKey:
    def __init__(self, n):
        self.n = n
    def __hash__(self):
        return self.n.hash()
    def __eq__(self, other):
        return self.n.eq(other.n)
    def __repr__(self):
        return str(self.n)

def askey(n):
    assert isinstance(n, AstRef)
    return AstRefKey(n)

def get_vars(f):
	r = set()
	def collect(f):
		if is_const(f):
			if f.decl().kind() == Z3_OP_UNINTERPRETED and not askey(f) in r:
				r.add(askey(f))
		else:
			for c in f.children():
				collect(c)
	collect(f)
	return list(r)


def get_models(F, M):
	result = []
	s = Solver()
	s.add(F)
	while len(result) < M and s.check() == sat:
		m = s.model()
		result.append(m)
		# Create a new constraint the blocks the current model
		block = []
		for d in m:
			# d is a declaration
			if d.arity() > 0:
				raise Z3Exception("uninterpreted functions are not supported")
			# create a constant from declaration
			c = d()
			if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
				raise Z3Exception("arrays and uninterpreted sorts are not supported")
			block.append(c != m[d])
		s.add(Or(block))

	return result



class planningKB():

	def __init__(self, fluents, actions, inits, goals, preconds, add_effects, del_effects, frame_axioms, excls):

		self.fluent = fluents
		self.actions = actions
		self.inits = inits
		self.goals = goals
		self.preconditions = preconds
		self.add_effects = add_effects
		self.del_effects = del_effects
		self.excls = excls
		self.frame_axioms = frame_axioms

	def all_formulae(self):
		return self.inits + self.goals + self.preconditions +self.add_effects +self.del_effects + self.frame_axioms + self.excls

	def model(self):
		s = Solver()
		for k in self.all_formulae():
			s.add(k)
		if s.check():
			return s.model()
		else:
			return None

	def plan(self):
		def atoi(text):
			return int(text) if text.isdigit() else text

		def natural_keys(text):
			return [atoi(c) for c in re.split('(\d+)', text)]
		model = self.model()

		# for m in model:
		# 	if model[m]

		plan = [str(d) for d in model if str(model[d]) == str(True) and str(d) in self.actions]
		plan = sorted(plan, key=lambda x: natural_keys(x)[1])

		return plan