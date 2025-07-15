# ERA5 Kathmandu Valley Rainfall Visualization

A Python toolkit for downloading, processing, and visualizing spatial rainfall data from ERA5 reanalysis specifically for the Kathmandu Valley region in Nepal.

## Features

- **ERA5 Data Download**: Automated download of precipitation data from Copernicus Climate Data Store
- **Spatial Visualization**: High-quality maps showing rainfall distribution across Kathmandu Valley
- **Time Series Analysis**: Hourly precipitation trends and area-averaged rainfall
- **Geographic Context**: Includes major cities (Kathmandu, Lalitpur, Bhaktapur) and geographic features
- **Sample Data Mode**: Works with synthetic data when ERA5 access is not available

## Installation

### Prerequisites

1. **Python 3.7+** with pip
2. **CDS API Account** (for real ERA5 data download)
   - Register at [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
   - Accept the ERA5 terms and conditions

### Install Dependencies

```bash
# Clone or download the project files
# Navigate to the project directory

# Install required packages
pip install -r requirements.txt

# Alternative: Install packages individually
pip install numpy pandas xarray netcdf4 matplotlib cartopy cdsapi geopandas
```

### Configure CDS API (Optional but Recommended)

To download real ERA5 data, you need to configure your CDS API credentials:

1. **Get your API key**:
   - Login to [CDS](https://cds.climate.copernicus.eu/)
   - Go to your profile page
   - Copy your UID and API key

2. **Create configuration file**:
   ```bash
   # Linux/Mac
   nano ~/.cdsapirc
   
   # Windows
   notepad %USERPROFILE%\.cdsapirc
   ```

3. **Add your credentials**:
   ```
   url: https://cds.climate.copernicus.eu/api/v2
   key: {your-uid}:{your-api-key}
   ```

   See `cdsapirc_template.txt` for detailed instructions.

## Quick Start

### Basic Usage (Sample Data)

```python
from era5_kathmandu_rainfall import KathmanduRainfallPlotter

# Create plotter instance
plotter = KathmanduRainfallPlotter()

# Generate sample rainfall plot
plotter.plot_spatial_rainfall()
```

### Download and Plot Real ERA5 Data

```python
from era5_kathmandu_rainfall import KathmanduRainfallPlotter

plotter = KathmanduRainfallPlotter()

# Download data for specific date
data_file = plotter.download_era5_data(year=2023, month=7, day=15)

# Create spatial plot
plotter.plot_spatial_rainfall(data_file, "2023-07-15")

# Create time series plot
plotter.plot_time_series(data_file)
```

### Run Complete Example

```bash
# Run the main script (includes sample data fallback)
python era5_kathmandu_rainfall.py

# Run usage examples
python example_usage.py
```

## Code Structure

### Main Components

- **`era5_kathmandu_rainfall.py`**: Main script with `KathmanduRainfallPlotter` class
- **`example_usage.py`**: Demonstration script with various usage examples
- **`requirements.txt`**: Python dependencies
- **`cdsapirc_template.txt`**: CDS API configuration template

### Key Functions

#### `KathmanduRainfallPlotter` Class

- **`download_era5_data()`**: Download ERA5 precipitation data
- **`plot_spatial_rainfall()`**: Create spatial rainfall maps
- **`plot_time_series()`**: Generate time series plots
- **`load_sample_data()`**: Create synthetic rainfall data for testing

## Geographic Coverage

**Kathmandu Valley Bounds:**
- **North**: 27.8°N
- **South**: 27.6°N  
- **East**: 85.5°E
- **West**: 85.2°E

**Included Cities:**
- Kathmandu (85.324°E, 27.717°N)
- Lalitpur (85.321°E, 27.668°N)
- Bhaktapur (85.430°E, 27.671°N)

## Data Information

### ERA5 Reanalysis

- **Source**: ECMWF ERA5 reanalysis
- **Variable**: Total Precipitation (`tp`)
- **Temporal Resolution**: Hourly
- **Spatial Resolution**: ~31 km (0.25° × 0.25°)
- **Units**: meters (converted to mm for visualization)

### Sample Data

When ERA5 data is not available, the script generates realistic synthetic precipitation patterns that simulate:
- Orographic effects typical of Kathmandu Valley
- Monsoon season characteristics
- Spatial variability across the region

## Output Files

The script generates several types of output:

### Plots
- **`kathmandu_rainfall_YYYYMMDD.png`**: Spatial rainfall maps
- **`kathmandu_rainfall_timeseries.png`**: Hourly precipitation time series

### Data Files
- **`era5_rainfall_kathmandu.nc`**: Downloaded ERA5 NetCDF data

## Customization

### Modify Geographic Bounds

```python
# Edit KATHMANDU_BOUNDS in era5_kathmandu_rainfall.py
KATHMANDU_BOUNDS = {
    'north': 27.9,    # Extend northward
    'south': 27.5,    # Extend southward
    'east': 85.6,     # Extend eastward
    'west': 85.1      # Extend westward
}
```

### Change Date Range

```python
# Download multiple days
for day in range(1, 8):  # First week of July
    data_file = plotter.download_era5_data(year=2023, month=7, day=day)
    plotter.plot_spatial_rainfall(data_file, f"2023-07-{day:02d}")
```

### Customize Visualization

```python
# Modify plot parameters in plot_spatial_rainfall()
im = ax.contourf(
    ds.longitude, ds.latitude, daily_precip,
    levels=np.linspace(0, daily_precip.max(), 25),  # More contour levels
    cmap='plasma',  # Different colormap
    transform=ccrs.PlateCarree(),
    extend='max'
)
```

## Troubleshooting

### Common Issues

1. **CDS API Error**: 
   - Check `.cdsapirc` file location and format
   - Verify your CDS account has accepted ERA5 terms
   - Ensure your API key is correct

2. **Import Errors**:
   - Install missing packages: `pip install <package_name>`
   - Check cartopy installation (may need system dependencies)

3. **Plotting Issues**:
   - Update matplotlib: `pip install --upgrade matplotlib`
   - Install additional cartopy features: `pip install cartopy[plotting]`

### Cartopy Installation (Advanced)

If you encounter cartopy installation issues:

```bash
# Ubuntu/Debian
sudo apt-get install libproj-dev proj-data proj-bin libgeos-dev

# CentOS/RHEL
sudo yum install proj-devel geos-devel

# macOS (with Homebrew)
brew install proj geos

# Then install cartopy
pip install cartopy
```

## Examples and Use Cases

### Monsoon Analysis
```python
# Analyze monsoon season (June-September)
for month in [6, 7, 8, 9]:
    data_file = plotter.download_era5_data(year=2023, month=month, day=15)
    plotter.plot_spatial_rainfall(data_file, f"2023-{month:02d}-15")
```

### Drought Monitoring
```python
# Compare dry and wet periods
dry_period = plotter.download_era5_data(year=2023, month=12, day=15)
wet_period = plotter.download_era5_data(year=2023, month=7, day=15)

plotter.plot_spatial_rainfall(dry_period, "Dry Season")
plotter.plot_spatial_rainfall(wet_period, "Monsoon Season")
```

## Contributing

Feel free to enhance this toolkit by:
- Adding new visualization options
- Implementing additional meteorological variables
- Extending geographic coverage
- Improving data processing efficiency

## License

This code is provided for educational and research purposes. Please cite ERA5 data appropriately when using for publications:

*Hersbach, H., Bell, B., Berrisford, P., et al. (2020): The ERA5 global reanalysis. Quarterly Journal of the Royal Meteorological Society, 146(730), 1999-2049.*

## Contact

For questions about ERA5 data access, visit the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/).

For technical issues with this code, check the error messages and refer to the troubleshooting section above.