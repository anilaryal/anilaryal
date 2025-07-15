#!/usr/bin/env python3
"""
ERA5 Spatial Rainfall Visualization for Kathmandu Valley

This script downloads ERA5 reanalysis precipitation data and creates
spatial plots for the Kathmandu valley region in Nepal.

Requirements:
- CDS API key configured (~/.cdsapirc)
- Required Python packages (see requirements.txt)

Author: Generated for spatial rainfall analysis
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cdsapi
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Kathmandu Valley boundaries (approximate)
KATHMANDU_BOUNDS = {
    'north': 27.8,
    'south': 27.6,
    'east': 85.5,
    'west': 85.2
}

class KathmanduRainfallPlotter:
    """Class to handle ERA5 data download and rainfall plotting for Kathmandu valley."""
    
    def __init__(self):
        """Initialize the plotter with Kathmandu valley coordinates."""
        self.bounds = KATHMANDU_BOUNDS
        self.client = None
        
    def setup_cds_client(self):
        """Initialize CDS API client."""
        try:
            self.client = cdsapi.Client()
            print("✓ CDS API client initialized successfully")
        except Exception as e:
            print(f"Error initializing CDS client: {e}")
            print("Make sure you have configured your CDS API key in ~/.cdsapirc")
            raise
    
    def download_era5_data(self, year=2023, month=7, day=15, output_file='era5_rainfall_kathmandu.nc'):
        """
        Download ERA5 precipitation data for Kathmandu valley.
        
        Args:
            year (int): Year for data download
            month (int): Month for data download  
            day (int): Day for data download
            output_file (str): Output NetCDF filename
        """
        if self.client is None:
            self.setup_cds_client()
            
        # Expand bounds slightly for better visualization
        buffer = 0.1
        area = [
            self.bounds['north'] + buffer,  # North
            self.bounds['west'] - buffer,   # West  
            self.bounds['south'] - buffer,  # South
            self.bounds['east'] + buffer    # East
        ]
        
        request = {
            'product_type': 'reanalysis',
            'variable': 'total_precipitation',
            'year': str(year),
            'month': f'{month:02d}',
            'day': f'{day:02d}',
            'time': [
                '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
            ],
            'area': area,
            'format': 'netcdf',
        }
        
        print(f"Downloading ERA5 data for {year}-{month:02d}-{day:02d}...")
        print(f"Area: {area}")
        
        try:
            self.client.retrieve('reanalysis-era5-single-levels', request, output_file)
            print(f"✓ Data downloaded successfully: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error downloading data: {e}")
            raise
    
    def load_sample_data(self):
        """
        Create sample precipitation data for demonstration when ERA5 data is not available.
        """
        print("Creating sample precipitation data for demonstration...")
        
        # Create coordinate arrays
        lats = np.linspace(self.bounds['south']-0.1, self.bounds['north']+0.1, 50)
        lons = np.linspace(self.bounds['west']-0.1, self.bounds['east']+0.1, 50)
        
        # Create sample precipitation pattern (realistic for monsoon season)
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Create a realistic precipitation pattern with higher values in certain areas
        # Simulate orographic effects and typical monsoon patterns
        precip = (
            10 * np.exp(-((lat_grid - 27.7)**2 + (lon_grid - 85.35)**2) * 20) +  # Central peak
            8 * np.exp(-((lat_grid - 27.65)**2 + (lon_grid - 85.25)**2) * 30) +   # Southern peak
            5 * np.exp(-((lat_grid - 27.75)**2 + (lon_grid - 85.45)**2) * 25) +   # Eastern peak
            2 + 3 * np.random.random(lat_grid.shape)  # Base level + noise
        )
        
        # Create xarray dataset
        ds = xr.Dataset({
            'tp': ((['latitude', 'longitude'], precip * 1e-3)),  # Convert to meters (ERA5 units)
        }, coords={
            'latitude': lats,
            'longitude': lons,
        })
        
        return ds
    
    def plot_spatial_rainfall(self, data_file=None, title_date="Sample Data", save_plot=True):
        """
        Create spatial rainfall plot for Kathmandu valley.
        
        Args:
            data_file (str): Path to NetCDF file, if None uses sample data
            title_date (str): Date string for plot title
            save_plot (bool): Whether to save the plot
        """
        # Load data
        if data_file and os.path.exists(data_file):
            print(f"Loading data from {data_file}...")
            ds = xr.open_dataset(data_file)
            # Sum daily precipitation (convert from m/hour to mm/day)
            daily_precip = ds['tp'].sum('time') * 1000  # Convert to mm
        else:
            print("Using sample data for demonstration...")
            ds = self.load_sample_data()
            daily_precip = ds['tp'] * 1000  # Convert to mm
            
        # Create the plot
        fig = plt.figure(figsize=(12, 10))
        
        # Set up map projection
        ax = plt.axes(projection=ccrs.PlateCarree())
        
        # Set map extent for Kathmandu valley
        extent = [
            self.bounds['west'] - 0.1,
            self.bounds['east'] + 0.1,
            self.bounds['south'] - 0.1,
            self.bounds['north'] + 0.1
        ]
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.RIVERS, linewidth=0.3, alpha=0.7)
        ax.add_feature(cfeature.LAKES, alpha=0.3)
        
        # Plot precipitation data
        im = ax.contourf(
            ds.longitude, ds.latitude, daily_precip,
            levels=np.linspace(0, daily_precip.max(), 20),
            cmap='Blues',
            transform=ccrs.PlateCarree(),
            extend='max'
        )
        
        # Add contour lines
        contours = ax.contour(
            ds.longitude, ds.latitude, daily_precip,
            levels=10,
            colors='black',
            linewidths=0.5,
            alpha=0.6,
            transform=ccrs.PlateCarree()
        )
        ax.clabel(contours, inline=True, fontsize=8, fmt='%.1f')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('Daily Precipitation (mm)', fontsize=12)
        
        # Add gridlines
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                         linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xformatter = LongitudeFormatter()
        gl.yformatter = LatitudeFormatter()
        
        # Add title and labels
        plt.title(f'ERA5 Daily Precipitation - Kathmandu Valley\n{title_date}', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Add location markers for major cities
        cities = {
            'Kathmandu': (85.3240, 27.7172),
            'Lalitpur': (85.3206, 27.6683),
            'Bhaktapur': (85.4298, 27.6710)
        }
        
        for city, (lon, lat) in cities.items():
            ax.plot(lon, lat, 'ro', markersize=6, transform=ccrs.PlateCarree())
            ax.text(lon+0.02, lat+0.02, city, fontsize=10, fontweight='bold',
                   transform=ccrs.PlateCarree(), 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        if save_plot:
            output_file = f'kathmandu_rainfall_{title_date.replace("-", "")}.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved as: {output_file}")
        
        plt.show()
        
        return fig

    def plot_time_series(self, data_file=None):
        """
        Create time series plot of area-averaged precipitation.
        
        Args:
            data_file (str): Path to NetCDF file
        """
        if data_file and os.path.exists(data_file):
            ds = xr.open_dataset(data_file)
            # Calculate area-weighted mean over Kathmandu valley
            area_mean = ds['tp'].mean(['latitude', 'longitude']) * 1000  # Convert to mm/hour
            
            fig, ax = plt.subplots(figsize=(12, 6))
            area_mean.plot(ax=ax, linewidth=2, color='blue')
            ax.set_ylabel('Precipitation (mm/hour)')
            ax.set_xlabel('Time (Hours)')
            ax.set_title('Hourly Precipitation - Kathmandu Valley Average')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('kathmandu_rainfall_timeseries.png', dpi=300, bbox_inches='tight')
            print("✓ Time series plot saved as: kathmandu_rainfall_timeseries.png")
            plt.show()
        else:
            print("Time series requires actual ERA5 data file")

def main():
    """Main function to demonstrate rainfall plotting."""
    plotter = KathmanduRainfallPlotter()
    
    print("ERA5 Kathmandu Valley Rainfall Plotter")
    print("=" * 40)
    
    # Try to download real data (requires CDS API setup)
    try:
        print("\nAttempting to download ERA5 data...")
        data_file = plotter.download_era5_data(year=2023, month=7, day=15)
        
        # Plot spatial rainfall
        plotter.plot_spatial_rainfall(data_file, "2023-07-15")
        
        # Plot time series
        plotter.plot_time_series(data_file)
        
    except Exception as e:
        print(f"\nCould not download ERA5 data: {e}")
        print("Creating demonstration plot with sample data...")
        
        # Create demonstration plot with sample data
        plotter.plot_spatial_rainfall(None, "Sample Data")
    
    print("\n✓ Rainfall plotting completed!")

if __name__ == "__main__":
    main()