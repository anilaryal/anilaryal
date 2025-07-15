#!/usr/bin/env python3
"""
Example usage of the ERA5 Kathmandu Valley Rainfall Plotter

This script demonstrates different ways to use the rainfall plotting functionality.
"""

from era5_kathmandu_rainfall import KathmanduRainfallPlotter
import matplotlib.pyplot as plt

def example_basic_usage():
    """Example 1: Basic usage with sample data."""
    print("Example 1: Basic spatial rainfall plot with sample data")
    print("-" * 50)
    
    plotter = KathmanduRainfallPlotter()
    
    # Create a plot with sample data (no ERA5 download needed)
    fig = plotter.plot_spatial_rainfall(
        data_file=None, 
        title_date="Sample Monsoon Data", 
        save_plot=True
    )
    
    print("✓ Basic plot created successfully!\n")

def example_custom_date():
    """Example 2: Download and plot data for a specific date."""
    print("Example 2: Download ERA5 data for specific date")
    print("-" * 50)
    
    plotter = KathmanduRainfallPlotter()
    
    try:
        # Download data for monsoon season (July 2023)
        data_file = plotter.download_era5_data(
            year=2023, 
            month=7, 
            day=20
        )
        
        # Plot the downloaded data
        plotter.plot_spatial_rainfall(
            data_file=data_file,
            title_date="2023-07-20",
            save_plot=True
        )
        
        # Also create time series plot
        plotter.plot_time_series(data_file)
        
        print("✓ Real ERA5 data plot created successfully!\n")
        
    except Exception as e:
        print(f"Could not download ERA5 data: {e}")
        print("Make sure you have CDS API configured")
        print("Falling back to sample data...")
        
        # Fallback to sample data
        plotter.plot_spatial_rainfall(
            data_file=None,
            title_date="Sample Data (ERA5 unavailable)",
            save_plot=True
        )

def example_multiple_plots():
    """Example 3: Create multiple plots for comparison."""
    print("Example 3: Multiple plots with different parameters")
    print("-" * 50)
    
    plotter = KathmanduRainfallPlotter()
    
    # Create plots for different scenarios
    scenarios = [
        ("Light Rain", "Sample Data - Light"),
        ("Heavy Rain", "Sample Data - Heavy"),
        ("Monsoon Peak", "Sample Data - Monsoon")
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), 
                           subplot_kw={'projection': None})
    
    for i, (scenario, title) in enumerate(scenarios):
        print(f"Creating plot for: {scenario}")
        # Note: This would create separate plots
        # For a more advanced version, you could modify the class 
        # to accept custom subplot axes
        plotter.plot_spatial_rainfall(
            data_file=None,
            title_date=title,
            save_plot=False  # Don't save individual plots
        )
    
    print("✓ Multiple comparison plots created!\n")

def main():
    """Run all examples."""
    print("ERA5 Kathmandu Valley Rainfall - Usage Examples")
    print("=" * 60)
    
    # Example 1: Basic usage
    example_basic_usage()
    
    # Example 2: Custom date (requires CDS API)
    example_custom_date()
    
    # Example 3: Multiple plots
    example_multiple_plots()
    
    print("All examples completed!")
    print("\nGenerated files:")
    print("- kathmandu_rainfall_SampleData.png")
    print("- era5_rainfall_kathmandu.nc (if ERA5 download successful)")
    print("- kathmandu_rainfall_20230720.png (if ERA5 download successful)")
    print("- kathmandu_rainfall_timeseries.png (if ERA5 download successful)")

if __name__ == "__main__":
    main()