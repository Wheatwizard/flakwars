from Stack import Stack

class Interpreter(object):
	def __init__(self,sourceA,sourceB,size):
		self.tape = list(sourceA.ljust(size," ")+sourceB.ljust(size," "))
		self.memory ={
			"A": [Stack(),Stack()],
			"B": [Stack(),Stack()],
		}
		self.scope ={
			"A": Stack(),
			"B": Stack(),
		}
		self.pointer ={
			"A":  0,
			"B": size,
		}
		self.lastcharacter = {"A":"","B":""}
		self.size = size
	def step(self):
		for program in "AB":
			scope = self.scope[program]
			character = self.tape[self.pointer[program]%(self.size*2)]
			if character in "([</":
				scope.append(0)
			elif character == ")":
				if self.lastcharacter[program] == "(":
					scope.pop()
					scope.append(scope.pop()+1)
				else:
					value = scope.pop()
					self.memory[program][0].append(value)
					scope.append(scope.pop()+value)
			elif character == ">":
				if self.lastcharacter[program] == "<":
					scope.pop()
					self.memory[program] = self.memory[program][::-1]
				else:
					scope.pop()
			elif character == "]":
				if self.lastcharacter[program] == "[":
					scope.pop()
					scope.append(scope.pop()+len(self.memory[program][0]))
				else:
					scope.append(-scope.pop()+scope.pop())
			elif character == "\\":
				if self.lastcharacter[program] == "/":
					scope.pop()
					scope.append(scope.pop()+"([<{/)]>}\\".index(self.tape[self.pointer[program]+self.memory[program][0].pop()]))
				else:
					value = scope.pop()
					offset = self.memory[program][0].pop()
					self.tape[(self.pointer[program]+offset)%(self.size*2)] = "([<{/)]>}\\"[value%10]
					scope.append(scope.pop()+value)
					print "".join(self.tape)
			elif character == "{":
				#TODO fix
				if self.tape[(self.pointer[program]+1)%(self.size*2)] != "}":
					if not self.memory[program][0][-1]:
						tempscope = 1
						start = self.pointer[program]
						while tempscope:
							self.pointer[program] += 1
							self.pointer[program] %= self.size * 2
							if self.tape[self.pointer[program]] == "{": tempscope += 1
							if self.tape[self.pointer[program]] == "}": tempscope -= 1
							if self.pointer[program] == start:
								print "%s Loses"%program
								return False
			elif character == "}":
				if self.lastcharacter[program] == "{":
					scope.append(scope.pop()+self.memory[program][0].pop())
				else:
					if self.memory[program][0][-1]:
						tempscope = 1
						start = self.pointer[program]
						while tempscope:
							self.pointer[program] -= 1
							self.pointer[program] %= self.size * 2
							if self.tape[self.pointer[program]] == "{": tempscope -= 1
							if self.tape[self.pointer[program]] == "}": tempscope += 1
							if self.pointer[program] == start:
								print "%s Loses"%program
								return False
			if character != " ":self.lastcharacter[program] = character
			self.pointer[program] += 1
			self.pointer[program] %= self.size * 2
		return True
	def __str__(self):
		return "".join(self.tape)

if __name__ == "__main__":
	import time
	a=Interpreter("()()()){}){}){}){}]){>{}()))/()()()\}            }","()()])){\\{}[()]))>()()]}",256)
	print a
	while a.step():time.sleep(.1)
