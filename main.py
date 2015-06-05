__author__ = 'orps'


import random

class EnviromentLocal:
	def __init__(self, beds):
		self.free_beds = beds
		self.watchers = 0
		self.changed = True

	def freeBed(self):
		self.free_beds += 1
		self.changed = True

	def takeBed(self):
		if self.free_beds > 0:
			self.free_beds -= 1
			self.changed = True
			return True
		return False

	def printState(self):
		if self.changed:
			print str(self)
			self.changed = False

	def __repr__(self):
		return 'enviroment : free bads is {0}, tv watchers is {1}'.format(self.free_beds, self.watchers)

class State:
	def __init__(self):
		self.money_minus = 40
		self.eat_minus = 0.02
		self.eat_plus = 0.06
		self.mind_minus = 0.03
		self.mind_plus = 0.06
		self.energy_minus = 0.05
		self.energy_plus = 0.08
		self.money_steal = 100

class WorkState:
	def __init__(self):
		self.name = 'work'
		self.s = State()

	def activate(self, human, env, humans):
		if env.watchers > 0:
			print '{0} is working and TV is messing '.format(human.name, self.name)
		else:
			print '{0} is working '.format(human.name, self.name)
		human.state = self

	def deactivate(self, human, env, humans):
		pass

	def calc(self, human, env):
		human.money += human.money_step
		human.eat -= self.s.eat_minus
		human.mind -= self.s.mind_minus
		if env.watchers > 0:
			tmp = 2
		else:
			tmp = 1

		human.energy -= self.s.energy_minus * tmp

	def isAvailiable(self, human, env, humans):
		return True

	def prioritie(self, human):
		if human.money <= human.money_t:
			return 4

		return 3

class EatState:
	def __init__(self):
		self.name = 'eat'
		self.s = State()

	def activate(self, human, env, humans):
		print '{0} is eating '.format(human.name)
		human.state = self

	def deactivate(self, human, env, humans):
		pass

	def calc(self, human, env):
		human.money -= self.s.money_minus
		human.eat += self.s.eat_plus
		human.mind -= self.s.mind_minus
		tmp = 1
		human.energy -= self.s.energy_minus * tmp

	def isAvailiable(self, human, env, humans):
		return human.money > self.s.money_minus

	def prioritie(self, human):
		if human.eat <= human.eat_l:
			return 5

		if human.money <= human.eat_t:
			return 4

		return 2

class WatchState:
	def __init__(self):
		self.name = 'watch'
		self.s = State()

	def activate(self, human, env, humans):
		print '{0} is watching tv '.format(human.name)
		human.state = self
		env.watchers += 1

	def deactivate(self, human, env, humans):
		env.watchers -= 1

	def calc(self, human, env):
		human.eat -= self.s.eat_minus
		if env.watchers > 0:
			tmp = 1.9
		else:
			tmp = 1
		human.mind += self.s.mind_plus * tmp
		human.energy -= self.s.energy_minus

	def isAvailiable(self, human, env, humans):
		return True

	def prioritie(self, human):
		if human.mind <= human.mind_l:
			return 5

		if human.money <= human.mind_t:
			return 4

		return 3

class SleepState:
	def __init__(self):
		self.name = 'sleep'
		self.s = State()

	def activate(self, human, env, humans):
		print '{0} is sleeping '.format(human.name, self.name)
		human.state = self
		env.takeBed()

	def deactivate(self, human, env, humans):
		env.freeBed()

	def calc(self, human, env):
		human.eat -= self.s.eat_minus
		human.mind -= self.s.mind_minus
		human.energy += self.s.energy_plus

	def isAvailiable(self, human, env, humans):
		return env.free_beds > 0

	def prioritie(self, human):
		if human.energy <= human.energy_l:
			return 5

		if human.energy <= human.energy_t:
			return 4

		return 3

class StealState:
	def __init__(self):
		self.name = 'steal'
		self.s = State()

	def activate(self, human, env, humans):
		#print 'human {0} is stealing'.format(human.name)
		human.state = self
		for h in humans:
			if h.is_many_money() and h != human:
				print '{0} is stealing from {1}'.format(human.name, h.name)
				human.money += self.s.money_steal
				h.money -= self.s.money_steal
				break

	def deactivate(self, human, env, humans):
		pass

	def calc(self, human, env):
		human.eat -= self.s.eat_minus
		human.mind -= self.s.mind_minus
		human.energy -= self.s.energy_minus

	def isAvailiable(self, human, env, humans):
		for h in humans:
			if h.is_many_money() and human != h:
				return True

		return False

	def prioritie(self, human):
		if human.money <= human.money_l and human.eat <= human.eat_t:
			return 6

		return 1

class Freelancer:
	money_h = 4000
	money_t = 100
	money_l = 60

	eat_h = 1
	eat_t = 0.4
	eat_l = 0.2

	mind_h = 1
	mind_t = 0.45
	mind_l = 0.1

	energy_h = 1
	energy_t = 0.5
	energy_l = 0.12

	def __init__(self, name):
		self.money = 300
		self.name = name
		self.energy = random.uniform(0.5, 1)
		self.eat = random.uniform(0.5, 1)
		self.mind = random.uniform(0.5, 1)
		self.money_step = random.uniform(20, 30)
		self._is_normal = True
		self.state = None
		self._diagnosys = 'None'

	def __repr__(self):
		money_state = "normal"
		if self.money < self.money_t:
			money_state = 'low'
		if self.money < self.money_l:
			money_state = 'extremely low'

		eat_state = "normal"
		if self.eat < self.eat_t:
			eat_state = 'hungry'
		if self.eat < self.eat_l:
			eat_state = 'extremely hungry'

		mind_state = "normal"
		if self.mind < self.mind_t:
			mind_state = 'bad'
		if self.mind < self.mind_l:
			mind_state = 'extremely bad'

		energy_state = "normal"
		if self.energy < self.energy_t:
			energy_state = 'low'
		if self.energy < self.energy_l:
			mind_state = 'extremely low'

		return '{4} state: MONEY is {0}, ENERGY is {1}, HUNGRY state is {2}, MIND is {3}'.format(money_state,
																						energy_state,
																						eat_state,
																						mind_state, self.name)
	def is_normal(self):
		return self._is_normal

	def checkParams(self):
		self._is_normal = False

		if self.eat > 1:
			self.eat = 1

		if self.mind > 1:
			self.mind = 1

		if self.energy > 1:
			self.energy = 1

		if self.eat <= 0:
			self._diagnosys = 'died from hungry'
		elif self.mind <= 0:
			self._diagnosys = 'is psych'
		elif self.energy <= 0:
			self._diagnosys = 'died from heart'
		else:
			self._is_normal = True

	def step(self, env, states, humans):
		ss = {}
		prior = 0
		for state in states:
			if state.isAvailiable(self, env, humans):
				tmp = state.prioritie(self)
				if tmp > prior:
					prior = tmp
				ss[state] = state.prioritie(self)

		ss_list = []
		for state in ss.keys():
			if ss[state] == prior:
				ss_list.append(state)

		state = ss_list[random.randint(0, len(ss_list)-1)]
		if state.name == 'steal':
			if self.state is not None:
				self.state.deactivate(self, env, humans)
			state.activate(self, env, humans)
		else:
			if self.state != state:
				if self.state is not None:
					self.state.deactivate(self, env, humans)
				state.activate(self, env, humans)

	def is_many_money(self):
		return self.money > self.money_t

if __name__ == "__main__":
	freelancers = [Freelancer("DENIS"), Freelancer("MIKE"), Freelancer("DASHA"), Freelancer("LEM")]
	freelancers[1].money = 5000
	env = EnviromentLocal(2)
	states = [WorkState(), EatState(), WatchState(), SleepState(), StealState()]

	while len(freelancers) > 2:
		base_freelancers = freelancers
		freelancers = []
		for human in base_freelancers:
			human.step(env, states, base_freelancers)
		env.printState()

		for human in base_freelancers:
			human.state.calc(human, env)
			human.checkParams()
			print str(human)

		for human in base_freelancers:
			if human.is_normal():
				freelancers.append(human)
			else:
				print '{0} {1}'.format(human.name, human._diagnosys)

		print 