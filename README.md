# Encoder Library for IVT-S Current Sensor

This is a library for encoding CAN messages for the IVT-S current sensor.
It provides a set of functions to let you specify teh message contents as
function parameters, and it returns the data needed to create a CAN message.

For an example see the `example` directory.

## Installation

This package __is not__ on pypi.

You should always use a python virtual environment.

You can:

* install from github: `pip install git+https://github.com/sectioncritical/ivts.git`
* clone or download the repo and install from file system: `pip install path/to/ivts`

## TODO

This package is not really complete. It needs more work. Here is a partial
list:

* fill out missing encoder functions (log data for example)
* docs, docs, docs
* better example
* better tests
* decoder
