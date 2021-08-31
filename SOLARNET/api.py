from slumber import API

class SvoApi(API):
	def __call__(self, resource_uri):
			"""
			Returns a ressource by it's ressource URI
			"""
			return getattr(self, resource_uri)

svo_api = SvoApi('https://solarnet2.oma.be/service/api/svo/', auth = None)
