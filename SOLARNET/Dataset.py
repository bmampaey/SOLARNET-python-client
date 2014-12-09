import copy
from api import API
from filters import StringFilter, NumericFilter, TimeFilter
from Data import Data

class Dataset:
	
	class Iterator:
	
		def __init__(self, api, filters, keywords, offset = 0, limit = 20):
		
			self.api = api
			self.filters = filters
			self.keywords = keywords
			self.limit = limit
			self.offset = offset
			self.infos = []
		
		def __iter__(self):
			# Iterators are iterables too.
			return self
		
		def next(self):
			# Cache some info
			if not self.infos:
				self.infos = self.api.get(limit=self.limit, offset=self.offset, **self.filters)["objects"]
				self.offset += self.limit
			# Return the first one in cache
			if self.infos:
				info = self.infos.pop(0)
				# Parse the info into a Data
				meta_data = {self.keywords[field_name]: value for field_name, value in info.iteritems() if field_name in self.keywords}
				try:
					data_location = info["data_location"]["url"]
				except TypeError, KeyError:
					data_location = None
				tags = [tag["name"] for tag in info["tags"]]
				return Data(meta_data, data_location, tags)
			else:
				raise StopIteration()
	
	def __init__(self, info, api = API):
		self.name = info["name"]
		self.display_name = info["display_name"]
		self.description = info["description"]
		self.characteristics = info["characteristics"]
		
		self.keyword_api = api.api.v1(self.name + "_keyword")
		self.meta_data_api = api.api.v1(self.name + "_meta_data")
		self.data_location_api = api.api.v1(self.name + "_data_location")
		
		#Set up the keywords and the field names for easy reverse lookup
		# TODO get the fields by looking up the schema
		self.__keywords = dict()
		self.field_names = dict()
		
		for keyword in self.keyword_api.get(limit=0)["objects"]:
			self.field_names[keyword["name"]] = keyword["db_column"]
			self.__keywords[keyword["name"]] = {"description": keyword["description"], "unit": keyword["unit"], "type": keyword["python_type"] }
		
		# At first the filter is empty
		self.filters = dict()
	
	def __str__(self):
		if self.filters:
			return self.display_name + ": " + "; ".join([keyword+" = "+str(filter) for keyword,filter in self.filters.iteritems()])
		else:
			return self.display_name + ": all"
	
	def __repr__(self):
		return self.name
	
	def __get_filters(self):
		filters = dict()
		for keyword, filter in self.filters.iteritems():
			filters.update(filter(self.field_names[keyword]))
		return filters
	
	def __iter__(self):
		return self.Iterator(self.meta_data_api, self.__get_filters(), {field_name: keyword for keyword, field_name in self.field_names.iteritems()})
	
	def __getitem__(self, key):
		if isinstance(key, slice):
			# TODO if step is very large than cut down in smaller requests
			datas = list()
			i = 0
			for data in self.Iterator(self.meta_data_api, self.__get_filters(), {field_name: keyword for keyword, field_name in self.field_names.iteritems()}, offset = key.start, limit = key.stop):
				if i % key.step == 0:
					datas.append(data)
				i += 1
				if i + key.start >= key.stop:
					break
			return datas
		
		elif isinstance(key, int):
			if key < 0:
				raise IndexError("Negative indexes are not supported.")
			try:
				return next(self.Iterator(self.meta_data_api, self.__get_filters(), {field_name: keyword for keyword, field_name in self.field_names.iteritems()}, offset = key, limit = 1))
			except StopIteration:
				raise IndexError("The index (%d) is out of range" % key)
		
		else:
			raise TypeError("Invalid argument type.")
	
	@property
	def keywords(self):
		return self.__keywords
	
	
	def filter(self, *args, **kwargs):
		filters = dict()
		args = dict(zip(args[::2], args[1::2]))
		args.update(kwargs)
		for keyword, value in args.iteritems():
			if keyword in self.keywords:
				try:
					if self.keywords[keyword]["type"] == "str":
						filters[keyword] = StringFilter(value)
					elif self.keywords[keyword]["type"] == "int" or self.keywords[keyword]["type"] == "float":
						filters[keyword] = NumericFilter(value)
					elif self.keywords[keyword]["type"] == "datetime":
						filters[keyword] = TimeFilter(value)
					else:
						raise NotImplementedError("Filter for type %s has not been implemented" % self.keywords[keyword]["type"])
				except ValueError, why:
					raise ValueError("Bad filter value %s for keyword %s: %s" % (keyword, value, why))
			else:
				raise KeyError("Unknown keyword %s for dataset %s" % (keyword, self.display_name))
		
		dataset_copy = copy.deepcopy(self)
		dataset_copy.filters.update(filters)
		return dataset_copy
