![maplapse-logo](https://raw.githubusercontent.com/souravbhadra/maplapse/master/docs/images/logo.gif)

## Key Use
`MapLapse` can create animated maps from a given shapefile and associated temporal data. The outputs can be either gif or mp4.

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





