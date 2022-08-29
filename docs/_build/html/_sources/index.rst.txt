===============================================================
MapLapse: A python library to create animated timelapse of maps
===============================================================

.. image:: https://raw.githubusercontent.com/souravbhadra/maplapse/master/docs/images/logo.gif
        :alt: maplapse-logo

`MapLapse` is a Python-based library to create animated timelapse maps 
from given shapefiles. It is mainly built on top of `geopandas` and 
`matplotlib`, along with other open-source geospatial packages.

Key Features
============
* Animated **choropleth** maps
* Animated **proportional circle** maps
* Supports output in `.gif` and `.mp4`


Example
=======
The `Animator` object of `maplapse` can easily create the animations. Here is a code snippet:

.. code:: python

    from maplapse import Animator

    anim = Animator(shape='/county_shape.shp',
                value='/century_data.csv',
                time_column='Year',
                data_column='Value',
                shape_unique_column='ST_CNT',
                map_type='choropleth',
                out_path='/animation.gif')
   anim.animate()


Output:

.. image:: https://raw.githubusercontent.com/souravbhadra/maplapse/master/docs/images/corn_yield.gif
        :alt: maplapse-logo



.. toctree::
   :maxdepth: 2

   installation
   examples/index
   MapLapse API Reference <maplapse>

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
