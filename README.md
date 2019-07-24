SOLARNET API client
===================

Common usage
------------
```python
from __future__ import print_function
from SOLARNET import datasets

# See all available datasets
for dataset in datasets:
	print(dataset)

# Get a specific dataset
aia_lev1 = datasets["aia_lev1"]

# Filter the record in that dataset for June 2012 the 6th with a wavelength of 171A
filtered_aia_lev1 = aia_lev1.filter("DATE-OBS", "2012 June 6", WAVELNTH = 171)

# Display the date of observation and the wavelength in that filtered dataset
for record in filtered_aia_lev1:
	print(record.meta_data["DATE-OBS"], record.meta_data["WAVELNTH"])

# Download the data from a record
record = filtered_aia_lev1[0]
record.download("/tmp")

# Get the data as a BytesIO [1] without saving to disk
data = record.data()

# Open the data as a fits file (see astropy.io.fits [2])
hdus = record.HDUs()


```
[1] [BytesIO](https://docs.python.org/2/library/io.html#io.BytesIO)
[2] [astropy.io.fits](https://docs.astropy.org/en/stable/io/fits/)
