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
    
    # Update Ochs Orchard PYO Cash Registers (ID: 1249)
    update_farm_upick(csv_file, 1249, "YES", "strawberries, cherries, blueberries, raspberries, blackberries, peaches, plums, nectarines, pears, apples, tomatoes, vegetables, pumpkins, gourds", "https://www.ochsorchard.com/pick-your-own, https://www.hudsonvalleysojourner.com/country-delights/farms-orchards/u-pick-farms-orchards/ochs-orchard/")
    
    print("Updated Ochs Orchard PYO Cash Registers")