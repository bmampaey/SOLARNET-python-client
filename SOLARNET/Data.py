import os
import urllib, urlparse
import StringIO

class Data:
	
	def __init__(self, meta_data, data_location, tags):
		self.meta_data = meta_data
		self.data_location = data_location
		self.tags = tags
	
	def download(self, to="."):
		if os.path.isdir(to):
			to = os.path.join(to, os.path.basename(urlparse.urlparse(self.data_location).path))
		elif not os.path.isdir(os.path.dirname(to)):
			raise ValueError("No directory %s" % os.path.dirname(to))
		
		urllib.urlretrieve(self.data_location, to)
	
	def data(self):
		return StringIO.StringIO(urllib.urlopen(self.data_location).read())
	
	def HDUs(self):
		try:
			import pyfits
		except ImportError:
			raise ImportError("Module pyfits is not installed")
		else:
			return pyfits.open(self.data())
