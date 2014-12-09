import copy
from api import API
from Dataset import Dataset
from filters import StringFilter

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
		self.api = api.api.v1("dataset")
		# TODO get the list from a schema lookup
		self.field_names = ["name", "display_name", "instrument", "telescope", "description", "contact", "characteristics"]
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
				return next(dataset for dataset in self.Iterator(self.api.get(limit = 0, **self.__get_filters())["objects"]) if dataset.name == key or dataset.display_name == key)
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
			if keyword in self.field_names:
				try:
					filters[keyword] = StringFilter(value)
				except ValueError, why:
					raise ValueError("Bad filter value %s for keyword %s: %s" % (keyword, value, why))
			else:
				raise KeyError("Unknown keyword %s for dataset %s" % (keyword, self.display_name))
		
		dataset_copy = copy.deepcopy(self)
		dataset_copy.filters.update(filters)
		return dataset_copy

