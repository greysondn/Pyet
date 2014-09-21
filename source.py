from PIL import Image

# this is about the furthest extreme from neat code.

# constant colors
class pietColors(object):
	def __init__(self):
		# top row - lights
		self._lightRed     = (255, 192, 192)
		self._lightYellow  = (255, 255, 192)
		self._lightGreen   = (192, 255, 192)
		self._lightCyan    = (192, 255, 255)
		self._lightBlue    = (192, 192, 255)
		self._lightMagenta = (255, 192, 255)
		
		# second row - mediums
		self._red     = (255,   0,   0)
		self._yellow  = (255, 255,   0)
		self._green   = (  0, 255,   0)
		self._cyan    = (  0, 255, 255)
		self._blue    = (  0,   0, 255)
		self._magenta = (255,   0, 255)
		
		# third row - darks
		self._darkRed     = (192,   0,   0)
		self._darkYellow  = (192, 192,   0)
		self._darkGreen   = (  0, 192,   0)
		self._darkCyan    = (  0, 192, 192)
		self._darkBlue    = (  0,   0, 192)
		self._darkMagenta = (192,   0, 192)
		
		# fourth row - specials
		self._white = (255, 255, 255)
		self._black = (  0,   0,   0)
		
		# color table - per Piet normative spec
		self._colorTable = ( (self._lightRed, self._lightYellow, self._lightGreen, self._lightCyan, self._lightBlue, self._lightMagenta),
		                     (     self._red,      self._yellow,      self._green,      self._cyan,      self._blue,      self._magenta),
		                     ( self._darkRed,  self._darkYellow,  self._darkGreen,  self._darkCyan,  self._darkBlue,  self._darkMagenta) )
		
		# op table - again matching piet spec version
		self._opTable = (	(     "hold",        "push",          "pop"),
							(      "add",    "subtract",     "multiply"),
							(   "divide",         "mod",          "not"),
							(  "greater",     "pointer",       "switch"),
							("duplicate",        "roll",   "in(number)"),
							( "in(char)", "out(number)",    "out(char)")	) 
	# property forms of above variables
	@property
	def lightRed(self):
		return self._lightRed
	
	@property
	def lightYellow(self):
		return self._lightYellow
	
	@property
	def lightGreen(self):
		return self._lightGreen
	
	@property
	def lightCyan(self):
		return self._lightCyan
	
	@property
	def lightBlue(self):
		return self._lightBlue
	
	@property
	def lightMagenta(self):
		return self._lightMagenta

	@property
	def red(self):
		return self._red
	
	@property
	def yellow(self):
		return self._yellow
	
	@property
	def green(self):
		return self._green
	
	@property
	def cyan(self):
		return self._cyan
	
	@property
	def blue(self):
		return self._blue
	
	@property
	def magenta(self):
		return self._magenta
	
	@property
	def darkRed(self):
		return self._darkRed
	
	@property
	def darkYellow(self):
		return self._darkYellow
	
	@property
	def darkGreen(self):
		return self._darkGreen
	
	@property
	def darkCyan(self):
		return self._darkCyan
	
	@property
	def darkBlue(self):
		return self._darkBlue
	
	@property
	def darkMagenta(self):
		return self._darkMagenta

	@property
	def white(self):
		return self._white
	
	@property
	def black(self):
		return self._black
	
	@property
	def colorTable(self):
		return self._colorTable

	@property
	def opTable(self):
		return self._opTable

	# ---------------------------------------
	# other operations for piet colors
	# ---------------------------------------
	
	##
	# compares two colors given as 3 tuples
	#
	# @param   self    This object. Implicitly passed.
	# @param color1    3 tuple of a color as (R, G, B)
	# @param color2    3 tuple of a color as (R, G, B)
	#
	# @return  bool    whether the color tuples are the same
	#
	def compareColors(self, color1, color2):
	    # do they match? Default to true; we'll test negation out
		_match = True
		
		# test one at a time
		_match = _match and (color1[0] == color2[0])
		_match = _match and (color1[1] == color2[1])
		_match = _match and (color1[2] == color2[2])
		
		# return equivalence check
		return _match

	##
	# Finds color in the colorTable (plus white and black)
	#
	# @param   self    This object. Implicitly passed.
	# @param  color    3 tuple of a color as (R, G, B)
	#
	# @return tuple    2 tuple
	#                      First member: boolean
	#                          Was it found in the color table, or else actually white or black?
	#                      Second member: tuple
	#                          coordinates in colorTable
	#                              if found, just normal coordinates
	#                              if white, (-1, 1)
	#                              if black, (-1, 2)
	#                              if not found, (-1, 1)
	def findColor(self, color):
		# have we found a color?
		_found = False
		
		# coordinates in color table?
		_coordinates =( -1, -1)
		
		# go over the color table
		for x in range(6):
			for y in range(3):
				# compare this with the color we're currently at
				if (self.compareColors(color, pc.colorTable[y][x])):
					# found it! Store the coordinates, too.
					_found = True
					_coordinates = (x, y)
		
		# end of loop here
		#
		# let's see what happened there
		if (not _found):
			# there's still two colors it may be; we default to white.
			if (self.compareColors(color, self.white)):
				_found       = True
				_coordinates = (-1, 1)
			elif (self.compareColors(color, self.black)):
				_found       = True
				_coordinates = (-1, 2)
			else:
				_coordinates = (-1, 1)
		
		# after that, we just return a tuple.
		return (_found, _coordinates)

	def bufferString(self, string, length, char):
		while (len(string) < length):
			string = char + string
		return string
	
	def findOp(self, fromCoord, toCoord):
		# places to store the two shifts
		hueShift   = -1
		valueShift = -1
		
		# and the final operation.
		op = "noop"
		
		# so, let's first make sure it's not special case
		if (toCoord[0] >= 0 and fromCoord[0] >=0):
			# not special case. Okay. Let's handle hue.
			if (toCoord[0] > fromCoord[0]):
				# this transition is simple. We've not wrapped around.
				hueShift = toCoord[0] - fromCoord[0]
			elif (toCoord[0] == fromCoord[0]):
				# this is easy, too. We've not changed.
				hueShift = 0
			elif (toCoord[0] < fromCoord[0]):
				# this is the hard one, to me. We wrapped around.
				hueShift = ((6 - fromCoord[0]) + toCoord[0])
			else:
				# relax. Theoretically, this is impossible to reach. I'm just paranoid.
				raise ValueError("Invalid coordinate comparison for hue in findOp!")
			
			# and now value, pretty well the exact same way.
			if (toCoord[1] > fromCoord[1]):
				valueShift = toCoord[1] - fromCoord[1]
			elif (toCoord[1] == fromCoord[1]):
				valueShift = 0
			elif (toCoord[1] < fromCoord[1]):
				valueShift = ((3 - fromCoord[1]) + toCoord[1])
			else:
				raise ValueError("Invalid coordinate comparison for hue in findOp!")
				
			# and now we can find it in the table.
			op = self.opTable[hueShift][valueShift]
			
		else:
			op = "noop"
		
		return op
	
class pietInterpreter(object):
	def __init__(self):
		# stack - A python list
		self.stack = []
		
		# hold register - where things are held. Can never be less than 1.
		self.hold = 1
		
		# direction pointer - seeds to right in spec
		self.dp = ">"
		
		# codel chooser - seeds to left in spec
		self.cc = "<"
		
		# whether we're in trace mode
		self.trace = False
		
		# out bit
		self.outstr = ""
	
	##
	# noop - because sometimes, there is none.
	def noop(self):
		pass

	##
	# hold is the mysterious upper left corner of the spec's op table.
	#
	# There's no formal docs for it.
	def _hold(self):
		self.hold = self.hold + 1
		
	##
	# design docs:
	# Pushes the value of the colour block just exited on to the stack.
	# Note that values of colour blocks are not automatically pushed on to the stack -
	# this push operation must be explicitly carried out.
	def push(self):
		self.stack.append(self.hold)
	
	##
	# design docs:
	# Pops the top value off the stack and discards it.
	def pop(self):
		raise NotImplementedError("pop!")
		
	##
	# design docs:
	# Pops the top two values off the stack, adds them, and pushes the result back on
	# the stack.
	def add(self):
		self.stack.append(self.stack.pop() + self.stack.pop())
		
	##
	# design docs:
	# Pops the top two values off the stack, calculates the second top value minus the
	# top value, and pushes the result back on the stack.
	def subtract(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		self.stack.append(val2 - val1)
		
	##
	# design docs:
	# Pops the top two values off the stack, multiplies them, and pushes the result
	# back on the stack.
	def multiply(self):
		self.stack.append(self.stack.pop() * self.stack.pop())
		
	##
	# design docs:
	# Pops the top two values off the stack, calculates the integer division of the
	# second top value by the top value, and pushes the result back on the stack.
	# If a divide by zero occurs, it is handled as an implementation-dependent error,
	# though simply ignoring the command is recommended.
	def divide(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		self.stack.append(int(val2 / val1))
	
	##
	# design docs:
	# Pops the top two values off the stack, calculates the second top value modulo
	# the top value, and pushes the result back on the stack. The result has the same
	# sign as the divisor (the top value). If the top value is zero, this is a divide
	# by zero error, which is handled as an implementation-dependent error, though
	# simply ignoring the command is recommended.
	def mod(self):
		raise NotImplementedError("mod!")
	
	##
	# design docs:
	# Replaces the top value of the stack with 0 if it is non-zero, and 1 if it is zero.
	def _not(self):
		raise NotImplementedError("not!")
	
	##
	# design docs:
	# Pops the top two values off the stack, and pushes 1 on to the stack if the second
	# top value is greater than the top value, and pushes 0 if it is not greater.
	def greater(self):
		raise NotImplementedError("greater!")
	
	##
	# design docs:
	# Pops the top value off the stack and rotates the DP clockwise that many steps
	# (anticlockwise if negative).
	def pointer(self):
		raise NotImplementedError("pointer!")
	
	##
	# design docs:
	# Pops the top value off the stack and toggles the CC that many times
	# (the absolute value of that many times if negative).
	def switch(self):
		raise NotImplementedError("switch!")
	
	##
	# design docs:
	# Pushes a copy of the top value on the stack on to the stack.
	def duplicate(self):
		# pop value off stack, push it twice
		val = self.stack.pop()
		self.stack.append(val)
		self.stack.append(val)
	
	##
	# design docs:
	# Pops the top two values off the stack and "rolls" the remaining stack entries to
	# a depth equal to the second value popped, by a number of rolls equal to the first
	# value popped. A single roll to depth n is defined as burying the top value on the
	# stack n deep and bringing all values above it up by 1 place. A negative number of
	# rolls rolls in the opposite direction. A negative depth is an error and the command
	# is ignored. If a roll is greater than an implementation-dependent maximum stack
	# depth, it is handled as an implementation-dependent error, though simply ignoring
	# the command is recommended.
	def roll(self):
		pass
		
		
	
	##
	# design docs:
	# Reads a value from STDIN as either a number or character, depending on the particular
	# incarnation of this command and pushes it on to the stack. If no input is waiting on
	# STDIN, this is an error and the command is ignored. If an integer read does not receive
	# an integer value, this is an error and the command is ignored.
	def in_num(self):
		raise NotImplementedError("in(number)!")
	
	##
	# design docs:
	# Reads a value from STDIN as either a number or character, depending on the particular
	# incarnation of this command and pushes it on to the stack. If no input is waiting on
	# STDIN, this is an error and the command is ignored. If an integer read does not receive
	# an integer value, this is an error and the command is ignored.
	def in_char(self):
		raise NotImplementedError("in(char)!")
	
	##
	# design docs:
	# Pops the top value off the stack and prints it to STDOUT as either
	# a number or character, depending on the particular incarnation of
	# this command.
	def out_num(self):
		raise NotImplementedError("out(number)!")
	
	##
	# design docs:
	# Pops the top value off the stack and prints it to STDOUT as either
	# a number or character, depending on the particular incarnation of
	# this command.
	def out_char(self):
		if (self.trace):
			# trace mode, it gets set aside.
			self.outstr = str(chr(self.stack.pop()))
		else:
			# normally, it's straight out.
			print(str(chr(self.stack.pop())))
		
	##
	# evaluate
	# based on the given string, perform given action.
	def evaluate(self, command):
		if ("noop" == command):
			self.noop()
		elif ("hold" == command):
			self._hold()
		elif ("push" == command):
			self.push()
		elif ("pop" == command):
			self.pop()
		elif ("add" == command):
			self.add()
		elif ("subtract" == command):
			self.subtract()
		elif ("multiply" == command):
			self.multiply()
		elif ("divide" == command):
			self.divide()
		elif ("mod" == command):
			self.mod()
		elif ("not" == command):
			self._not()
		elif ("greater" == command):
			self.greater()
		elif ("pointer" == command):
			self.pointer()
		elif ("switch" == command):
			self.switch()
		elif ("duplicate" == command):
			self.duplicate()
		elif ("roll" == command):
			self.roll()
		elif ("in(number)" == command):
			self.in_num()
		elif ("in(char)" == command):
			self.in_char()
		elif ("out(number)" == command):
			self.out_num()
		elif ("out(char)" == command):
			self.out_char()
		else:
			raise ValueError(command)
		
		# also, just to keep it simple
		if ("hold" != command):
			# reset hold
			self.hold = 1

# main function. This can also be imported as a toolkit.
if __name__ == "__main__":
	im = Image.open("debug.png")
	pc = pietColors()
	pi = pietInterpreter()
	
	opnum = 0
	
	pi.trace = True
	
	# print a header
	print("#### |   X |   Y |   Operation | OUT | DP | CC | Stack")
	print("-----+-----+-----+-------------+-----+----+----+------")
	print("0000 |   0 |   0 |        INIT |     |  > |  < | []")
	
	# like this?
	
	print(im.getpixel((0, 0)))
	
	previousColor = (pc.findColor(im.getpixel((0, 0))))[1]
	currentColor  = (0, 0)
	
	for x in range (1, im.size[0]):
		opnum = opnum + 1
		
		currentColor = (pc.findColor(im.getpixel((x, 0))))[1]
		
		command = (pc.findOp(previousColor, currentColor))
		
		# pi.evaluate(command)
		
		previousColor = currentColor
		
		# this will take a minute
		
		if (("hold" != command) and ("noop" != command)):
			outline = pc.bufferString(str(opnum), 4, "0") + " | "
			outline = outline + pc.bufferString(str(x), 3, " ") + " |   0 | "
			outline = outline + pc.bufferString(command, 11, " ") + " | "
			outline = outline + pc.bufferString(pi.outstr, 3, " ") + " |  "
			outline = outline + pi.dp + " |  " + pi.cc + " | " + str(pi.stack)
			
			pi.outstr = ""
			
			print(outline)