SOLARNET Virtual Observatory (SVO)
==================================
The SVO is a service first supported by the [SOLARNET](http://solarnet-east.eu/) project, funded by the European Commission’s FP7 Capacities Programme under the Grant Agreement 312495. Then made operational thanks to the [SOLARNET2](https://solarnet-project.eu) project, funded by the the European Union's Horizon 2020 Research and Innovation Programme under Grant Agreement 824135.

It's purpose is to collect metadata from as many solar observations as possible, especially those made thanks to the SOLARNET projects, in a common catalog and make them available to the scientific community.

A first prototype version was released in February 2016, and the operational version is available now at https://solarnet2.oma.be

The SVO code is split in several parts:
- A [web server](https://github.com/bmampaey/SOLARNET-server)
- A [web client](https://github.com/bmampaey/SOLARNET-web-client)
- A [python client](https://github.com/bmampaey/SOLARNET-python-client)
- An [IDL client](https://github.com/bmampaey/SOLARNET-IDL-client)
- [Data provider tools](https://github.com/bmampaey/SOLARNET-provider-tools)

SOLARNET API python client
==========================

This package can be used as a client or as an example how to work with the API using Python 3

Example usage
-------------

```python

from SOLARNET import datasets

# See all available datasets
for dataset in datasets:
	print(dataset)

# Get a specific dataset
aia_lev1 = datasets['AIA level 1']

# Filter the record in that dataset for June 2012 the 6th with a wavelength of 171A
filtered_aia_lev1 = aia_lev1.filter('DATE-OBS', '2012 June 6', WAVELNTH = 171)

# Display the date of observation and the wavelength in that filtered dataset
for record in filtered_aia_lev1:
	print(record.metadata['DATE-OBS'], record.metadata['WAVELNTH'])

# Download the data from a record
record = filtered_aia_lev1[0]
record.download('/tmp')

# Get the data as a BytesIO [1] without saving to disk
data = record.data()

# Open the data as a fits file (see astropy.io.fits [2])
hdus = record.HDUs()


```
[1] [BytesIO](https://docs.python.org/3/library/io.html#io.BytesIO)
[2] [astropy.io.fits](https://docs.astropy.org/en/stable/io/fits/)
