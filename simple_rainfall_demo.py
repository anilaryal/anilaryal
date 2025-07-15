#!/usr/bin/env python3
"""
Simple ERA5 Rainfall Demo for Kathmandu Valley (without cartopy)

This is a simplified version that demonstrates the core rainfall plotting
functionality using only matplotlib, without requiring cartopy.
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import os

# Kathmandu Valley boundaries (approximate)
KATHMANDU_BOUNDS = {
    'north': 27.8,
    'south': 27.6,
    'east': 85.5,
    'west': 85.2
}

class SimpleKathmanduRainfallPlotter:
    """Simplified class for rainfall plotting without cartopy dependencies."""
    
    def __init__(self):
        """Initialize the plotter with Kathmandu valley coordinates."""
        self.bounds = KATHMANDU_BOUNDS
    
    def load_sample_data(self):
        """Create sample precipitation data for demonstration."""
        print("Creating sample precipitation data for Kathmandu Valley...")
        
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
            'tp': ((['latitude', 'longitude'], precip)),  # Already in mm
        }, coords={
            'latitude': lats,
            'longitude': lons,
        })
        
        return ds
    
    def plot_spatial_rainfall(self, title_date="Sample Data", save_plot=True):
        """
        Create spatial rainfall plot for Kathmandu valley using simple matplotlib.
        
        Args:
            title_date (str): Date string for plot title
            save_plot (bool): Whether to save the plot
        """
        # Load sample data
        print("Using sample data for demonstration...")
        ds = self.load_sample_data()
        daily_precip = ds['tp']  # Already in mm
            
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Extract values to avoid xarray compatibility issues
        lons = ds.longitude.values
        lats = ds.latitude.values
        precip_values = daily_precip.values
        
        # Plot precipitation data using contourf
        im = ax.contourf(
            lons, lats, precip_values,
            levels=np.linspace(0, np.max(precip_values), 20),
            cmap='Blues',
            extend='max'
        )
        
        # Add contour lines
        contours = ax.contour(
            lons, lats, precip_values,
            levels=10,
            colors='black',
            linewidths=0.5,
            alpha=0.6
        )
        ax.clabel(contours, inline=True, fontsize=8, fmt='%.1f')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('Daily Precipitation (mm)', fontsize=12)
        
        # Set labels and formatting
        ax.set_xlabel('Longitude (°E)', fontsize=12)
        ax.set_ylabel('Latitude (°N)', fontsize=12)
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Set aspect ratio to be roughly equal
        ax.set_aspect('equal', adjustable='box')
        
        # Add title
        plt.title(f'ERA5 Daily Precipitation - Kathmandu Valley\n{title_date}', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Add location markers for major cities
        cities = {
            'Kathmandu': (85.3240, 27.7172),
            'Lalitpur': (85.3206, 27.6683),
            'Bhaktapur': (85.4298, 27.6710)
        }
        
        for city, (lon, lat) in cities.items():
            ax.plot(lon, lat, 'ro', markersize=8, markeredgecolor='white', markeredgewidth=1)
            ax.text(lon+0.01, lat+0.01, city, fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Set map bounds
        ax.set_xlim(self.bounds['west'] - 0.05, self.bounds['east'] + 0.05)
        ax.set_ylim(self.bounds['south'] - 0.05, self.bounds['north'] + 0.05)
        
        plt.tight_layout()
        
        if save_plot:
            output_file = f'kathmandu_rainfall_simple_{title_date.replace("-", "").replace(" ", "_")}.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved as: {output_file}")
        
        # Show plot (won't work in headless environment but good for demo)
        try:
            plt.show()
        except:
            print("✓ Plot created successfully (display not available in headless mode)")
        
        return fig

    def create_summary_statistics(self):
        """Create summary statistics for the sample data."""
        ds = self.load_sample_data()
        daily_precip = ds['tp']
        
        # Extract values for calculations
        precip_values = daily_precip.values
        
        stats = {
            'mean': float(np.mean(precip_values)),
            'max': float(np.max(precip_values)),
            'min': float(np.min(precip_values)),
            'std': float(np.std(precip_values))
        }
        
        print("\nKathmandu Valley Rainfall Statistics:")
        print("-" * 40)
        print(f"Mean precipitation: {stats['mean']:.2f} mm")
        print(f"Maximum precipitation: {stats['max']:.2f} mm")
        print(f"Minimum precipitation: {stats['min']:.2f} mm")
        print(f"Standard deviation: {stats['std']:.2f} mm")
        
        return stats

def main():
    """Main function to demonstrate simplified rainfall plotting."""
    print("Simple ERA5 Kathmandu Valley Rainfall Plotter")
    print("=" * 50)
    
    # Set matplotlib to use non-interactive backend
    import matplotlib
    matplotlib.use('Agg')
    
    plotter = SimpleKathmanduRainfallPlotter()
    
    print("\nGenerating sample rainfall plot...")
    
    # Create demonstration plot with sample data
    fig = plotter.plot_spatial_rainfall("Sample Monsoon Data")
    
    # Generate summary statistics
    stats = plotter.create_summary_statistics()
    
    print("\n✓ Simple rainfall plotting demonstration completed!")
    print("\nNote: This is a simplified version using sample data.")
    print("For real ERA5 data download and advanced mapping features,")
    print("use the full era5_kathmandu_rainfall.py script with cartopy.")

if __name__ == "__main__":
    main()