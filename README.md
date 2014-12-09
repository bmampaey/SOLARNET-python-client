SOLARNET API client
===================

Common usage
------------
```python
from SOLARNET import datasets

# See all available datasets
for dataset in datasets:
	print dataset

# Get a specific dataset
aia_lev1 = datasets["aia_lev1"]

# Filter the record in that dataset for February 2012 the 20th with a wavelength of 171A
filtered_aia_lev1 = aia_lev1.filter("DATE-OBS", "2012 Feb 20", WAVELNTH = 171)

# Display the date of observation and the wavelength in that filtered dataset
for record in filtered_aia_lev1:
	print record.meta_data["DATE-OBS"], record.meta_data["WAVELNTH"]

# Download the data from a record
record = filtered_aia_lev1[0]
redord.download("/tmp")

# Get the data as a [StringIO](https://docs.python.org/2/library/stringio.html) without saving to disk
data = record.data()

# Open the data as a fits file (see [pyfits open](https://pythonhosted.org/pyfits/api_docs/api_files.html#pyfits.open))
hdus = record.HDUs()


```
