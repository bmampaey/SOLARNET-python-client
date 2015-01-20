import copy
from datetime import date, datetime
import dateutil.parser

from time import Time

class Filter:
	
	def __init__(self, value):
		self.value = value
		self.filters = {"%s__exact": value}

	def __call__(self, field_name):
		return {filter%field_name: value for filter, value in self.filters.iteritems()}
	
	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return repr(self.value)


class StringFilter(Filter):
	
	def __init__(self, value):
		self.value = value
		self.filters = dict()
		
		if not isinstance(value, (tuple, list)):
			self.filters["%s__iexact"] = value
		
		elif len(value) == 0 or len(value) > 3:
				raise ValueError("String filter must either be an exact value or a triplet (starts with, contains, end with)")
		
		else:
			if len(value) >= 1 and value[0] is not None:
				self.filters["%s__istartswith"] = value[0]
			if len(value) >= 2 and value[1] is not None:
				self.filters["%s__icontains"] = value[1]
			if len(value) >= 3 and value[2] is not None:
				self.filters["%s__iendswith"] = value[2]
	

class NumericFilter(Filter):
	
	def __init__(self, value):
		self.value = value
		self.filters = dict()
		if not isinstance(value, (tuple, list)):
			self.filters["%s__exact"] = value
		elif len(value) == 0 or len(value) > 2:
				raise ValueError("Numeric filter must either be an exact value or a doublet (min value, max value)")
		else:
			if len(value) >= 1 and value[0] is not None:
				self.filters["%s__gte"] = value[0]
			if len(value) >= 2 and value[1] is not None:
				self.filters["%s__lt"] = value[1]


class TimeFilter(Filter):
	
	def __init__(self, value):
		self.value = value
		self.filters = dict()
		
		if isinstance(self.value, basestring):
			self.value = Time(value)
		
		if isinstance(self.value, Time):
				for attr in ["year", "month", "day", "hour", "minute", "second"]:
					if getattr(self.value, attr) is not None:
						self.filters["%s__" + attr] = getattr(self.value, attr)
		
		elif isinstance(self.value, (tuple, list)) and 0 < len(self.value) <= 2 and (self.value[0] is None or isinstance(self.value[0], (basestring, datetime))) and (self.value[1] is None or isinstance(self.value[1], (basestring, datetime))):
			if isinstance(self.value[0] , basestring):
				self.value[0] = dateutil.parser.parse(self.value[0])
			self.filters["%s__gte"] = value[0].isoformat()
			if isinstance(self.value[1] , basestring):
				self.value[1] = dateutil.parser.parse(self.value[1])
			self.filters["%s__gte"] = value[1].isoformat()
		
		else:
			raise ValueError("Time filter must either be a Time value, a Time compatible string, or a doublet (first date, last date)")

class RelatedFilter(Filter):
	
	def __init__(self, value):
		self.value = value
		self.filters = dict()
		self.filters["%s__in"] = value
