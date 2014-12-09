from datetime import datetime
import dateutil.parser

class Time:
	def __init__(self, *args, **kwargs):
		
		attrs = ["year", "month", "day", "hour", "minute", "second"]
		# First case, we get a string
		if len(args) == 1 and isinstance(args[0], basestring):
			time = Time.from_string(args[0])
			for attr in attrs:
				setattr(self, attr, getattr(time, attr)) 
		# Second case we get value for the fields indenpendently
		else:
			for attr, arg in zip(attrs, args):
				if arg is None:
					setattr(self, attr, None)
				elif isinstance(arg, int) or (attr == "second" and isinstance(arg, float)):
					setattr(self, attr, arg)
				else:
					raise TypeError("Wrong type of argument for attribute %s" % attr)
			
			for attr, arg in kwargs.iteritems():
				if hasattr(self, attr):
					raise ValueError("Duplicate value for attribute %s" % attr)
				elif arg is None:
					setattr(self, attr, None)
				elif isinstance(arg, int) or (attr == "second" and isinstance(arg, float)):
					setattr(self, attr, arg)
				else:
					raise TypeError("Wrong type of argument for attribute %s" % attr)
		
		# Set remaining attributes to None
		for attr in attrs:
			if not hasattr(self, attr):
				setattr(self, attr, None)
		
		# Make some verifications
		if self.year is not None and self.year <= 0:
			raise ValueError("Wrong value %s for attribute year" % self.year)
		if self.month is not None and not 1 <= self.month <= 12:
			raise ValueError("Wrong value %s for attribute month" % self.month)
		if self.day is not None and not 1 <= self.day <= 31:
			raise ValueError("Wrong value %s for attribute day" % self.day)
		if self.hour is not None and not 0 <= self.hour <= 23:
			raise ValueError("Wrong value %s for attribute hour" % self.hour)
		if self.minute is not None and not 0 <= self.minute <= 59:
			raise ValueError("Wrong value %s for attribute minute" % self.minute)
		if self.second is not None and not 0 <= self.second <= 59:
			raise ValueError("Wrong value %s for attribute second" % self.second)

	@classmethod
	def from_string(cls, time_string):
		# dateutil parser fills the unknow values from the default
		# We use this to know which field was set
		one = dateutil.parser.parse(time_string, default = datetime(1,1,1,1,1,1,1))
		two = dateutil.parser.parse(time_string, default = datetime(2,2,2,2,2,2,2))
		time = cls()
		for attr in ["year", "month", "day", "hour", "minute", "second", "microsecond"]:
			if getattr(one, attr) == 1:
				if getattr(two, attr) == 2:
					# The attribute was not set
					setattr(time, attr, None)
				else:
					setattr(time, attr, 1)
			else:
				setattr(time, attr, getattr(two, attr)) 
		
		# Add microseconds to seconds
		if time.microsecond is not None:
			if time.second is None:
				time.second = time.microsecond/1000000.0
			else:
				time.second += time.microsecond/1000000.0
			time.microsecond = None
		
		return time
	
	def __str__(self):
		
		return ", ".join(["%s: %s" % (attr,  getattr(self, attr)) for attr in ["year", "month", "day", "hour", "minute", "second"]])
	
	def __repr__(self):
		
		return "Time(%s)" % str(self)
