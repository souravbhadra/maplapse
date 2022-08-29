![check-status](https://img.shields.io/github/checks-status/souravbhadra/maplapse/main)
![license](https://img.shields.io/github/license/souravbhadra/maplapse)
![downloads](https://img.shields.io/github/downloads/souravbhadra/maplapse/total)


![maplapse-logo](https://raw.githubusercontent.com/souravbhadra/maplapse/master/docs/images/logo.gif)

`MapLapse` is a Python-based library to create animated timelapse maps from given shapefiles. It is mainly built on top of `geopandas` and `matplotlib`, along with other open-source geospatial packages.

## Key Features
- Animated **choropleth** maps
- Animated **proportional circle** maps
- Supports output in `.gif` and `.mp4`

## Example
The `Animator` object of `maplapse` can easily create the animations. Here is a code snippet:

```
anim = Animator(shape='/county_shape.shp',
                value='/century_data.csv',
                time_column='Year',
                data_column='Value',
                shape_unique_column='ST_CNT',
                map_type='choropleth',
                out_path='/animation.gif')
anim.animate()
```
Output:
![maplapse-ex1](https://raw.githubusercontent.com/souravbhadra/maplapse/master/docs/images/corn_yield.gif)

![maplapse-ex2](https://raw.githubusercontent.com/souravbhadra/maplapse/master/docs/images/covid.gif)

## Installation
Simply use `pip install maplapse`. The library has dependencies to 





