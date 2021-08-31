from copy import deepcopy
from .api import svo_api
from .filters import StringFilter, NumericFilter, TimeFilter, RelatedFilter
from .Data import Data


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
		
		def __next__(self):
			# Cache some info
			if not self.infos:
				self.infos = self.api.get(limit=self.limit, offset=self.offset, **self.filters)['objects']
				self.offset += self.limit
			# Return the first one in cache
			if self.infos:
				info = self.infos.pop(0)
				# Parse the info into a Data
				metadata = {self.keywords[field_name]: value for field_name, value in info.items() if field_name in self.keywords}
				try:
					data_location = info['data_location']
				except (TypeError, KeyError):
					data_location = None
				tags = [tag['name'] for tag in info['tags']]
				return Data(metadata, data_location, tags)
			else:
				raise StopIteration()
	
	def __init__(self, info, api = svo_api):
		self.name = info['name']
		self.description = info['description']
		self.characteristics = info['characteristics']
		self.metadata_api = api(info['metadata']['resource_uri'])
		
		# Get the fields by looking up the schema
		self.fields = self.metadata_api.schema.get()['fields']
		
		#Set up the keywords and the field names for easy reverse lookup
		self.__keywords = dict()
		self.field_names = dict(tags='tags')
		
		for keyword in api.keyword.get(limit=0, dataset__name=self.name)['objects']:
			self.field_names[keyword['verbose_name']] = keyword['name']
			self.__keywords[keyword['verbose_name']] = {'description': keyword['description'], 'unit': keyword['unit'], 'type': keyword['type'] }
		
		# At first the filter is empty
		self.filters = dict()
	
	def __str__(self):
		if self.filters:
			return self.name + ': ' + '; '.join([keyword+' = '+str(filter) for keyword,filter in self.filters.items()])
		else:
			return self.name + ': all'
	
	def __repr__(self):
		return str(self)
	
	def __get_filters(self):
		filters = dict()
		for keyword, filter in self.filters.items():
			field_name = self.field_names[keyword]
			for key, value in filter.filters.items():
				filters[key % field_name] = value
		return filters
	
	def __iter__(self):
		return self.Iterator(self.metadata_api, self.__get_filters(), {field_name: keyword for keyword, field_name in self.field_names.items()})
	
	def __getitem__(self, key):
		if isinstance(key, slice):
			datas = list()
			i = 0
			for data in self.Iterator(self.metadata_api, self.__get_filters(), {field_name: keyword for keyword, field_name in self.field_names.items()}, offset = key.start, limit = key.stop):
				if not key.step or i % key.step == 0:
					datas.append(data)
				i += 1
				if i + key.start >= key.stop:
					break
			return datas
		
		elif isinstance(key, int):
			if key < 0:
				raise IndexError('Negative indexes are not supported.')
			try:
				return next(self.Iterator(self.metadata_api, self.__get_filters(), {field_name: keyword for keyword, field_name in self.field_names.items()}, offset = key, limit = 1))
			except StopIteration:
				raise IndexError('The index (%d) is out of range' % key)
		
		else:
			raise TypeError('Invalid argument type.')
	
	@property
	def keywords(self):
		return self.__keywords
	
	
	def filter(self, *args, **kwargs):
		filters = dict()
		args = dict(zip(args[::2], args[1::2]))
		args.update(kwargs)
		
		for keyword, value in args.items():
			try:
				field_name = self.field_names[keyword]
			except KeyError:
				raise KeyError('Unknown keyword %s for dataset %s' % (keyword, self.name))
			else:
				field_type = self.fields[field_name]['type']
			try:
				if field_type == 'string':
					filters[keyword] = StringFilter(value)
				elif field_type == 'integer' or field_type == 'float':
					filters[keyword] = NumericFilter(value)
				elif field_type == 'datetime':
					filters[keyword] = TimeFilter(value)
				elif field_type == 'related':
					filters[keyword] = RelatedFilter(value)
				else:
					raise NotImplementedError('Filter for type %s has not been implemented' % field_type)
			except ValueError as why:
					raise ValueError('Bad filter value %s for keyword %s: %s' % (keyword, value, why))
		
		dataset_copy = deepcopy(self)
		dataset_copy.filters.update(filters)
		return dataset_copy
