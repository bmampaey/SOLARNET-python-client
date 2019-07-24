from distutils.core import setup
setup(
	name = 'SOLARNET',
	packages = ['SOLARNET'],
	version = '2.1',
	description = 'A python client to access the RESTfull interface of the SOLARNET Data Archive',
	author = 'Benjamin Mampaey',
	author_email = 'bmampaey@gmail.com',
	url = 'https://github.com/bmampaey/SOLARNET-python-client',
	download_url = 'https://github.com/bmampaey/SOLARNET-python-client/tarball/2.1',
	install_requires=[
		'python-dateutil',
		'slumber',
		'astropy',
		'numpy',
		'future'
	],
	keywords = [
		'sun',
		'astronomy',
		'SOLARNET',
		'RESTfull'
	],
	classifiers = [
		'Intended Audience :: Science/Research',
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License','Natural Language :: English',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: Astronomy'
	],
	package_data = {'': ['*.txt', '*.rst', '*.md']}
)
