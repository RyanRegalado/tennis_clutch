import os
import requests
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_slam_pointbypoint/master"

# Define years and slams for data organization
YEARS = {
    2011: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2012: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2013: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2014: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2015: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2016: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2017: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2018: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2019: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2020: ['ausopen', 'frenchopen', 'usopen'],  # No Wimbledon (COVID-19)
    2021: ['ausopen', 'frenchopen', 'wimbledon', 'usopen'],
    2022: ['wimbledon', 'usopen'],  # Partial data
    2023: ['wimbledon', 'usopen'],  # Partial data
    2024: ['wimbledon', 'usopen'],  # Partial data
}

# Generate FILE_MAPPINGS dynamically from YEARS
FILE_MAPPINGS = {}
for year, slams in YEARS.items():
    for slam in slams:
        FILE_MAPPINGS[f"{year}-{slam}-matches.csv"] = f"data/raw/match/{year}-{slam}-matches.csv"
        FILE_MAPPINGS[f"{year}-{slam}-points.csv"] = f"data/raw/points/{year}-{slam}-points.csv"


def download_file(remote_filename, local_path):
    """Download a file from the repository to the local path."""
    url = f"{BASE_URL}/{remote_filename}"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    print(f"Downloading {remote_filename}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Saved to {local_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to download {remote_filename}: {e}")
        return False


def download_all_files():
    """Download all files defined in FILE_MAPPINGS."""
    success_count = 0
    total_count = len(FILE_MAPPINGS)
    
    for remote_file, local_file in FILE_MAPPINGS.items():
        if download_file(remote_file, local_file):
            success_count += 1
    
    print(f"\nDownload complete: {success_count}/{total_count} files successful")


def download_specific_year_and_slam(year, slam):
    """Download specific year and slam data.
    
    Args:
        year: Year (e.g., 2024)
        slam: Tournament name ('usopen', 'wimbledon', 'frenchopen', 'ausopen')
    """
    files = {
        f"{year}-{slam}-matches.csv": f"data/raw/match/{year}-{slam}-matches.csv",
        f"{year}-{slam}-points.csv": f"data/raw/points/{year}-{slam}-points.csv",
    }
    
    for remote_file, local_file in files.items():
        download_file(remote_file, local_file)


def download_year(year):
    """Download all slam data from specified year.
    
    Args:
        year: Year (e.g., 2024)
    """
    year_int = int(year)
    if year_int not in YEARS:
        print(f"✗ No data available for year {year}")
        return
    
    success_count = 0
    slams = YEARS[year_int]
    total = len(slams) * 2  # matches + points for each slam
    
    for slam in slams:
        files = {
            f"{year}-{slam}-matches.csv": f"data/raw/match/{year}-{slam}-matches.csv",
            f"{year}-{slam}-points.csv": f"data/raw/points/{year}-{slam}-points.csv",
        }
        for remote_file, local_file in files.items():
            if download_file(remote_file, local_file):
                success_count += 1
    
    print(f"\nYear {year} download complete: {success_count}/{total} files successful")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Download specific year and slam
        year = sys.argv[1]
        slam = sys.argv[2]
        download_specific_year_and_slam(year, slam)
    elif len(sys.argv) == 2:
        # Download entire year
        year = sys.argv[1]
        download_year(year)
    else:
        # Download all predefined files
        download_all_files()
