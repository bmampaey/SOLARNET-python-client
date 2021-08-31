import os
from urllib.request import urlopen, urlretrieve
from io import BytesIO

class Data:
	
	def __init__(self, metadata, data_location, tags):
		self.metadata = metadata
		self.data_location = data_location
		self.tags = tags
	
	def download(self, to='.'):
		if not os.path.isdir(to):
			raise ValueError('No directory %s' % to)
		
		to = os.path.join(to, self.data_location['file_path'])
		
		if not os.path.isdir(os.path.dirname(to)):
			os.makedirs(os.path.dirname(to))
		
		urlretrieve(self.data_location['file_url'], to)
	
	def data(self):
		return BytesIO(urlopen(self.data_location['file_url']).read())
	
	def HDUs(self):
		try:
			from astropy.io import fits
		except ImportError:
			raise ImportError('Module astropy is not installed')
		else:
			return fits.open(self.data())
