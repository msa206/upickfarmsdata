#!/usr/bin/env python3
import csv
import sys

def update_farm_upick(csv_file, farm_id, has_upick, offerings, sources):
    """Update a farm's U-pick information in the CSV file"""
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and row[0] == str(farm_id):
                # Update the upick columns (assuming they are the last 3 columns)
                row[-3] = has_upick
                row[-2] = offerings
                row[-1] = sources
            rows.append(row)
    
    # Write back to file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

if __name__ == "__main__":
    csv_file = "/Users/pablo/Desktop/upick farms data/upickfarms_enriched_updated.csv"
    
    # Update multiple farms
    updates = [
        # Hazeye Farms (ID: 1252) - NO u-pick based on research (farm market)
        (1252, "NO", "", ""),
        
        # Dowless Blueberry Farm (ID: 1253) - YES u-pick
        (1253, "YES", "blueberries", "https://upickfarmsusa.com/fl/duval-county/dowless-blueberry-farm/, https://www.pickyourown.org/FLnorth-Dowless-Blueberries.php"),
        
        # Bees & Trees Farm (ID: 1254) - YES u-pick
        (1254, "YES", "apples, strawberries, peaches", "https://www.virginia.org/listing/bees-&-trees-farm/13572/, https://www.yelp.com/biz/bees-and-trees-farm-elkwood"),
    ]
    
    for farm_id, has_upick, offerings, sources in updates:
        update_farm_upick(csv_file, farm_id, has_upick, offerings, sources)
        print(f"Updated farm ID {farm_id}")