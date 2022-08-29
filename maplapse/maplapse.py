"""
The main module of `maplapse` library.

Author: Sourav Bhadra
Author Email: sbhadra019@gmail.com
"""


import os
import glob
import shutil
import tempfile
import collections
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
from tqdm import tqdm
import warnings


plt.rcParams.update({'figure.max_open_warning': 0})


class Animator():
    """The object that needs to initialized for timelapse parameters.

    To create a timelapse in either .gif or .mp4 format, the Animator
    object is needed to be specified, where key parameters should be 
    included.
    
    Args:
        shape (str): The path of the shapefile.
        value (str): The path of the csv file.
        time_column (str): The column in the csv file (`value`) 
            that represents the time or date.
        data_column (str): The column in the csv file (`value`) 
            that represents the value to map.
        shape_unique_column (str): The column in the shapefile 
            (`shape`) that can be uniquely mapped to the csv file.
        out_path (str): The path of the output animation file.
            `maplapse` currently supports output file as either 
            `.gif`or `. mp4`.
        map_type (str, optional): Type of output map. It can be 
            either `choropleth` or `proportional_circle`. If 
            `choropleth`, then the animation will include change 
            of a colormap. If type is `proportional_circle`, then 
            the values will be proportionally increased as the 
            radius of circles. By default 'choropleth'.
        value_unique_column (str, optional): The column in the csv 
            file (`value`) that can be uniquely mapped to the 
            shapfile. Only required when the unique column for 
            shapefile and value csv is different. If they 
            have the same column name, then the 
            value_unique_column will be automatically set as the 
            one as the shape_unique_column. By default None
        temporal_scaling (bool, optional): If `True`, then the 
            temporal values will be scaled to the maximum and 
            minimum values of the entire value csv file. 
            Otherwise, each timeframe plot of the animation will 
            be scaled to its own timefame. By default True.
        scale_factor (float, optional): A constant value to be 
            multiplied with the `proportional_circle` radius to 
            adjust its extent. If the circles are too large and 
            expand beyond the map boundary, then use 
            `scale_factor` values from 0 to 1 (e.g., 0.05). By 
            default None
            
    Keyword Args:
        dpi (int): The DPI (resolution) of the maps. By default 
            300.
        cmap (str): The colormap of the maps. Can be any cmap 
            from the matplotlib cmap library. By default 
            'rainbow'.
        map_title (str): Title of the map. Empty if none given.
        legend_title (str): Title of the legend. Shows 'Legend' 
            if none given.
        temporal_divisions (int): The temporal divisions for the 
            time scale in the bottom. 
        font (str): The font name for the map. Supports the font
            names supported in matplotlib.
        font_size (int): Size of all font elements. By default, 
            it is 7.
        poly_line_color (str):  The color of the plygon lines. By
            default, 'gray'
        poly_line_width (float): The width of the polygon lines. 
            By default, 0.7.
        circle_color (str): The color of the circles in the 
            `proportional_circle` map. By default 'red'.
        circle_alpha (float): The transparency level of the circles in
            the `proportional_circle` map. By default 0.5.
            
    Raises:
        ValueError: The `scale_factor` must be specified when 
            plotting `proportional_circle`.
    """
    
    def __init__(
        self,
        shape,
        value,
        time_column,
        data_column,
        shape_unique_column,
        out_path,
        map_type='choropleth',
        value_unique_column=None,
        temporal_scaling=True,
        scale_factor=None,
        **kwargs
    ):

        self.time_column = time_column
        self.shape_unique_column = shape_unique_column
        if value_unique_column is None:
            self.value_unique_column = shape_unique_column
        else:
            self.value_unique_column = value_unique_column
        self.data_column = data_column
        
        self.shape_path = shape 
        self.shape = gpd.read_file(shape)
        self.temporal = pd.read_csv(value, parse_dates=[time_column])
        
        # Get the unique timestamps from the time data
        self.times = np.unique(self.temporal[self.time_column].values)
        self.out_path = out_path
        self.temp_dir = None
        #self.temp_dir = self.create_temp_dir()
        self.map_type = map_type
        self.temporal_scaling = temporal_scaling
        self.counter = None # To be used for counting timeframes
        
        if map_type == 'proportional_circle' and scale_factor is None:
            raise ValueError('The `scale_factor` must be specified when plotting `proportional_circle`.')
        else:
            self.scale_factor = scale_factor
            
        if "dpi" not in kwargs.keys():
            kwargs["dpi"] = 300
        if "cmap" not in kwargs.keys():
            kwargs["cmap"] = 'rainbow'
        if "map_title" not in kwargs.keys():
            kwargs["map_title"] = None
        if "legend_title" not in kwargs.keys():
            kwargs["legend_title"] = "legend"
        if "temporal_divisions" not in kwargs.keys():
            kwargs["temporal_divisions"] = 10
        if "font" not in kwargs.keys():
            kwargs["font"] = 'Arial'
        if "font_size" not in kwargs.keys():
            kwargs["font_size"] = 10
        if "poly_line_color" not in kwargs.keys():
            kwargs["poly_line_color"] = 'gray'
        if "poly_line_width" not in kwargs.keys():
            kwargs["poly_line_width"] = 0.7
        if map_type == 'proportional_circle':
            if "circle_color" not in kwargs.keys():
                kwargs["circle_color"] = 'red'
        else:
            kwargs["circle_color"] = None
        if map_type == 'proportional_circle': 
            if "circle_alpha" not in kwargs.keys():
                kwargs["circle_alpha"] = 0.5
        else:
            kwargs["circle_alpha"] = None
            
        self.dpi = kwargs["dpi"]
        self.cmap = kwargs["cmap"]
        self.map_title = kwargs["map_title"]
        self.legend_title = kwargs["legend_title"]
        self.temporal_divisions = kwargs["temporal_divisions"]
        self.font = kwargs["font"]
        self.font_size = kwargs["font_size"]
        self.poly_line_color = kwargs["poly_line_color"]
        self.poly_line_width = kwargs["poly_line_width"]
        self.circle_color = kwargs["circle_color"]
        self.circle_alpha = kwargs["circle_alpha"]
        
        
        

    
    def create_temp_dir(
        self
    ):
        temp_dir = os.path.join(os.path.dirname(self.out_path),
                                f'temp')
        os.makedirs(temp_dir, exist_ok=True) 
        return temp_dir
    
    
    def sort_filenames(self, filenames):
        data = {}
        for filename in filenames:
            data[int(os.path.basename(filename).split('.')[0])] = filename
        # Sort the dictionary
        data_ord = collections.OrderedDict(sorted(data.items()))
        return list(data_ord.values())
        
    
    def save_animation(self, **kwargs):
        filenames = glob.glob(os.path.join(self.temp_dir, '*.png'))
        filenames = self.sort_filenames(filenames)
        with imageio.get_writer(self.out_path, mode='I', **kwargs) as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)
                
                
    def choropleth(
        self,
        gdf,
        ax
    ):
        self.shape.plot(
            ax=ax,
            facecolor="none",
            edgecolor='none',
            lw=1,
            zorder=1
        )
        
        if self.temporal_scaling:
            # Get the overall min and max values
            vmax = self.temporal[self.data_column].max()
            vmin = self.temporal[self.data_column].min()
        else:
            vmax = None
            vmin = None
        
        # Main ax
        gdf.plot(
            column=self.data_column,
            ax=ax,
            legend=True,
            cmap=self.cmap,
            legend_kwds={'label': self.legend_title,
                         'shrink': 0.6},
            vmin=vmin,
            vmax=vmax,
            zorder=2
        )
        
        
    def proportional_circle(
        self,
        gdf,
        ax
    ):
        warnings.filterwarnings("ignore")
    
        self.shape.plot(
            ax=ax,
            facecolor="none",
            edgecolor=self.poly_line_color,
            lw=self.poly_line_width,
            zorder=1
        )
        
        centroids = gdf.centroid
        centroids.plot(
            markersize=gdf[self.data_column]*self.scale_factor,
            ax=ax,
            color=self.circle_color,
            alpha=self.circle_alpha,
            zorder=2
        )
                
                
    def plot_frame(
        self,
        time,
        join,
        for_view=True
    ):
        font = {'family' : self.font,
                'weight' : 'normal',
                'size'   : self.font_size}
        plt.rc('font', **font)
        
        fig, ax = plt.subplots(2, 1,
                               dpi=self.dpi,
                               gridspec_kw={'height_ratios': [12, 1]})
            
        date = pd.to_datetime(time).strftime("%Y-%m-%d")
        
        if self.map_type == 'choropleth':
            self.choropleth(join, ax[0])
        elif self.map_type == 'proportional_circle':
            self.proportional_circle(join, ax[0])
        
        ax[0].set_axis_off()
        if self.map_title is not None:
            ax[0].set_title(self.map_title,
                            fontsize=self.font_size*1.5)
        
        # Temporal ax
        ax[1].axhline(y=0.5, color='darkgray', linestyle='-', zorder=1)
        
        years = pd.DatetimeIndex(self.times).year
        months = pd.DatetimeIndex(self.times).month
        days = pd.DatetimeIndex(self.times).day

        if np.unique(years).shape[0] <= 1:
            if np.unique(months).shape[0] <= 1:
                t1, t2 = days.min(), days.max()
                t = int(pd.to_datetime(time).strftime("%d"))
            else:
                t1, t2 = months.min(), months.max()
                t = int(pd.to_datetime(time).strftime("%m"))
        else:
            t1, t2 = years.min(), years.max()
            t = int(pd.to_datetime(time).strftime("%Y"))
            
        ax[1].scatter(x=int(t),
                        y=0.5,
                        zorder=2,
                        color='r',
                        s=30,
                        marker='>')
        
        #start_time = int(pd.to_datetime(self.times[0]).strftime(self.temporal_freq))
        #end_time = int(pd.to_datetime(self.times[-1]).strftime(self.temporal_freq))
        
        ax[1].set_xlim(left=t1, right=t2)
        ax[1].set_ylim(bottom=0.45, top=0.55)
        for k in np.linspace(t1, t2, self.temporal_divisions):
            ax[1].text(int(k), 0.56, f'{int(k)}',
                        ha='center', va='top',
                        fontsize=self.font_size)
        ax[1].set_axis_off()
        ax[1].set_title(f'{date}', fontsize=self.font_size)
        
        if for_view:
            pass
        else:
            plt.close()
            fig.savefig(os.path.join(self.temp_dir,
                                     f'{self.counter}.png'),
                        dpi=self.dpi,
                        bbox_inches='tight')
    
    
    def check_join_dtype(
        self
    ):
        shape_id_dtype = self.shape[self.shape_unique_column].dtype
        value_id_dtype = self.temporal[self.value_unique_column].dtype
        if shape_id_dtype != value_id_dtype:
            self.shape[self.shape_unique_column] = self.shape[self.shape_unique_column].astype(value_id_dtype)
        else:
            pass
        
    
    def view_frame(
        self,
        frame=0
    ):
        """
        View a selected frame.
        
        Useful to visualize one frame and then update the mapping
        parameters to adjust the visualization options in the
        `Animator` object.
        
        Args:
            frame (int): The frame to temporarily view, by default 0.
            
        Returns:
            matplotlib.Figure: A Figure object.
        """
        # Check if the join field dtype is same or not
        self.check_join_dtype()
        # Pick a time
        time = self.times[frame]
        # Get joined data
        join = self.join_shape_temporal(time)
        # Visualize one frame
        fig = self.plot_frame(time, join)
        return fig
        
    
    
    def join_shape_temporal(
        self,
        time
    ):
        # Get the data matching with the time
        time_data = self.temporal[self.temporal[self.time_column]==time]            
        # Merge with the shapefile
        join = pd.merge(
            left=self.shape,
            right=time_data,
            how='left',
            left_on=self.shape_unique_column,
            right_on=self.value_unique_column
        )
        return join
        
        
    def animate(
        self,
        **kwargs,
    ):
        """
        View a selected frame.
        
        Useful to visualize one frame and then update the mapping
        parameters to adjust the visualization options in the
        `Animator` object.
        
        Keyword Args:
            duration (float): The duration of each frame. It is to be
                used when the output format is `.gif`. By default 0.5.
            fps (int): Frames per second. It is to be used when the 
                output format is `.mp4`. By default 20.
        """
        # Check if the join field dtype is same or not
        self.check_join_dtype()
        # Loop through each unique time
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.temp_dir = tmpdirname
            for i, time in tqdm(enumerate(self.times), total=self.times.shape[0]):
                join = self.join_shape_temporal(time)
                self.counter = i
                # Matplotlib
                self.plot_frame(time, join, False)
            
            if "duration" not in kwargs.keys():
                kwargs["duration"] = 0.5
            if "fps" not in kwargs.keys():
                kwargs["fps"] = 20
            
            file_type = os.path.basename(self.out_path).split('.')[-1]
            if file_type == 'gif':
                self.save_animation(duration=kwargs["duration"])
            elif file_type == 'mp4':
                self.save_animation(fps=kwargs["fps"])
            
        #shutil.rmtree(self.temp_dir)