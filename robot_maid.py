from random import randint
from time import clock

##===== TRANSITION =================

class Transition(object):
	def __init__(self, toState):
		self.toState = toState

	def Execute(self):
		print("Transitioning......")

##======= STATE ===================

class State(object):
	def __init__(self, FSM):
		self.FSM = FSM
		self.timer = 0
		self.startTime = 0

	def Enter(self):
		self.timer = randint(0, 5)

	def Execute(self):
		pass

	def Exit(self):
		pass

class CleanDishes(State):
	def __init__(self, FSM):
		super(CleanDishes, self).__init__(FSM)

	def Enter(self):
		print("Preparing to clean dishes")
		super(CleanDishes, self).Enter()

	def Execute(self):
		print("Cleaning dishes")
		if(self.startTime + self.timer <= clock()):
			if not(randint(1, 3) %2):
				self.FSM.ToTransition("toVacum")
			else:
				self.FSM.ToTransition("toSleep")

	def Exit(self):
		print("Finished cleaning dishes.")

class Vacum(State):
	def __init__(self, FSM):
		super(Vacum, self).__init__(FSM)

	def Enter(self):
		print("Starting to vacum")
		super(Vacum, self).Enter()

	def Execute(self):
		print("Vacuming")
		if(self.startTime + self.timer <= clock()):
			if not(randint(1, 3) %2):
				self.FSM.ToTransition("toSleep")
			else:
				self.FSM.ToTransition("toCleanDishes")

	def Exit(self):
		print("Finished Vacuming")

class Sleep(State):
	def __init__(self, FSM):
		super(Sleep, self).__init__(FSM)

	def Enter(self):
		print("Starting to sleep")
		super(Sleep, self).Enter()

	def Execute(self):
		print("sleeping")
		if(self.startTime + self.timer <= clock()):
			if not(randint(1, 3) %2):
				self.FSM.ToTransition("toVacum")
			else:
				self.FSM.ToTransition("toCleanDishes")

	def Exit(self):
		print("waking up from sleep")

##================================================
## FINTE STATE MACHINE

class FSM(object):
	def __init__(self, character):
		self.char = character
		self.state = {}
		self.transition = {}
		self.curState = None
		self.prevState = None
		self.trans = None

	def AddTransition(self, transName, transition):
		self.transition[transName] = transition

	def AddState(self, stateName, state):
		self.state[stateName] = state

	def SetState(self, stateName):
		self.prevState = self.curState
		self.curState = self.state[stateName]

	def ToTransition(self, toTrans):
		self.trans = self.transition[toTrans]

	def Execute(self):
		if(self.trans):
			self.curState.Exit()
			self.trans.Execute()
			self.SetState(self.trans.toState)
			self.curState.Enter()
			self.trans = None
		self.curState.Execute()

##=====================================================
## IMPLEMENTATION

Char = type("Char", (object,), {})

class RobotMaid(Char):
	def __init__(self):
		self.FSM = FSM(self)

		## STATES
		self.FSM.AddState("Sleep", Sleep(self.FSM))
		self.FSM.AddState("CleanDishes", CleanDishes(self.FSM))
		self.FSM.AddState("Vacum", Vacum(self.FSM))

		## TRANSMITION
		self.FSM.AddTransition("toSleep", Transition("Sleep"))
		self.FSM.AddTransition("toVacum", Transition("Vacum"))
		self.FSM.AddTransition("toCleanDishes", Transition("CleanDishes"))

		self.FSM.SetState("Sleep")

	def Execute(self):
		self.FSM.Execute()

if (__name__ == '__main__'):
	r = RobotMaid()
	
	for i in range(30):
		startTime = clock()
		timeInterval = 1
		while (startTime + timeInterval > clock()):
			pass

		r.Execute()
