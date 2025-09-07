#!/usr/bin/env python3

import csv
import sys

def update_farm_data(csv_path):
    """Update the CSV file with farm data in a systematic way"""
    
    # Farm data to update (row_number: [has_upick, upick_offerings, upick_sources])
    updates = {
        925: ["Yes", "strawberries, raspberries, pumpkins", "https://www.deeplyrootedfarms.net/harvestcal.php"],  # Deeply Rooted Farms
        926: ["Yes", "strawberries, pumpkins, vegetables", "https://upickfarmsusa.com/il/rock-island-county/happy-hollow-u-pick/"],  # Happy Hollow U-Pick  
        927: ["Yes", "pumpkins, Christmas trees", "https://www.pumpkinpatches.com/puckervillefarms"],  # Puckerville Farms
    }
    
    # Read all lines
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Update specified rows
    for row_num, data in updates.items():
        if len(lines) > row_num - 1:  # Convert to 0-based index
            line = lines[row_num - 1].strip()
            if line.endswith(',,,'):
                # Replace the last three empty columns with our data
                new_line = line[:-3] + f',{data[0]},"{data[1]}",{data[2]}\n'
                lines[row_num - 1] = new_line
                print(f"Updated row {row_num}")
            else:
                print(f"Row {row_num} doesn't end with ,,, - skipping")
    
    # Write back to file
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("Update complete")

if __name__ == "__main__":
    csv_path = "/Users/pablo/Desktop/upick farms data/upickfarms_enriched_updated.csv"
    update_farm_data(csv_path)