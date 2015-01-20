import copy
from api import API
from Dataset import Dataset
from filters import StringFilter, NumericFilter, TimeFilter, RelatedFilter

class Datasets:
	
	class Iterator:
	
		def __init__(self, infos, offset = 0, limit = 0):
		
			self.infos = infos
		
		def __iter__(self):
			# Iterators are iterables too.
			return self
		
		def next(self):
			# Return the first one in cache
			if self.infos:
				return Dataset(self.infos.pop(0))
			else:
				raise StopIteration()
	
	def __init__(self, api = API):
		self.api = api.v1("dataset")
		# Get the list from a schema lookup
		self.fields = self.api.schema.get()['fields']
		self.filters = dict()
	
	def __iter__(self):
		return self.Iterator(self.api.get(limit = 0, **self.__get_filters())["objects"])
	
	def __str__(self):
		return ", ".join([str(dataset) for dataset in self])
	
	def __repr__(self):
		return ", ".join([repr(dataset) for dataset in self])
	
	def __getitem__(self, key):

		if isinstance(key, basestring):
			try:
				return next(dataset for dataset in self.Iterator(self.api.get(limit = 0, **self.__get_filters())["objects"]) if dataset.id == key or dataset.name == key)
			except StopIteration:
				raise IndexError("No such dataset")
		
		elif isinstance(key, int):
			if key < 0:
				raise IndexError("Negative indexes are not supported.")
			try:
				return next(self.Iterator(self.api.get(offset = key, limit = 1, **self.__get_filters())["objects"]))
			except StopIteration:
				raise IndexError("The index (%d) is out of range" % key)
		
		else:
			raise TypeError("Invalid argument type.")
	
	def __get_filters(self):
		filters = dict()
		for field_name, filter in self.filters.iteritems():
			filters.update(filter(field_name))
		return filters
		
	def filter(self, *args, **kwargs):
		filters = dict()
		args = dict(zip(args[::2], args[1::2]))
		args.update(kwargs)
		for keyword, value in args.iteritems():
			try:
				if self.fields[keyword]["type"] == "string":
					filters[keyword] = StringFilter(value)
				elif self.fields[keyword]["type"] == "int" or self.fields[keyword]["type"] == "float":
					filters[keyword] = NumericFilter(value)
				elif self.fields[keyword]["type"] == "datetime":
					filters[keyword] = TimeFilter(value)
				elif self.fields[keyword]["type"] == "related":
					filters[keyword] = RelatedFilter(value)
				else:
					raise NotImplementedError("Filter for type %s has not been implemented" % self.fields[keyword]["type"])
			except ValueError, why:
					raise ValueError("Bad filter value %s for keyword %s: %s" % (keyword, value, why))
			except KeyError:
				raise KeyError("Unknown datasets keyword %s" % keyword)
		
		dataset_copy = copy.deepcopy(self)
		dataset_copy.filters.update(filters)
		return dataset_copy

