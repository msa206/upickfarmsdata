#!/usr/bin/env python3
"""
Script to update U-pick farm data in CSV based on research findings
"""
import csv
import os

# Research findings for the 20 farms
research_data = {
    # Farm Name: (has_upick, offerings, sources)
    'Pine Valley Farm': ('No', '', ''),
    'Happy Valley Orchard': ('Yes', 'apples', 'http://www.happyvalleyorchard.com/'),
    'Goffle Brook Farm & Garden Center': ('Yes', 'blueberries; raspberries; elderberries', 'https://gofflebrookfarms.com/'),
    'Kinderhook Farm': ('No', '', ''),  # Focus on livestock, not public u-pick
    'North Star Orchard LLC': ('No', '', ''),  # No current u-pick, focus on farm store/tastings
    'Smith Orchard': ('Yes', 'apples; blueberries; peaches', 'https://smithorchard.net/'),
    "Honey's Harvest Farm": ('Yes', 'berries; nuts; fruits', 'https://honeysharvest.com/'),
    'Meacham Urban Farm': ('No', '', ''),  # Farm store only, no u-pick mentioned
    'Stanley Family Farms U Pick Cherries': ('Yes', 'cherries', 'https://www.facebook.com/stanleyfamilyfarmsupickcherries/'),
    'Fix Bros Inc fruit farms': ('Yes', 'cherries; peaches; apples; pumpkins', 'https://fixbrosfruitfarm.com/'),
    'Gooseberry Bridge Farm': ('Yes', 'flowers', 'http://www.gooseberrybridge.com/'),
    'Farm.One': ('No', '', ''),  # Indoor farm with tours, not u-pick
    'Hilltop Hanover Farm & Environmental Center': ('Yes', 'vegetables', 'http://hilltophanoverfarm.org/'),  # Educational farm with u-pick
    'Fischer Farm': ('No', '', ''),  # Sweet corn and pumpkin sales, no u-pick mentioned
    'Cucumber Hill Farm': ('Yes', 'pumpkins', 'http://www.cucumberhillfarm.com/'),  # U-pick pumpkins
    'Reese Farms': ('No', '', ''),  # No u-pick mentioned, just crop sales
    'Lundberg Family Farms': ('No', '', ''),  # Rice farm with tours, no u-pick
    "Lloyd's Family Farm": ('Yes', 'strawberries; blackberries; pumpkins; christmas trees', 'https://www.lloydsfamilyfarm.com/'),
    'Stone Tavern Orchards': ('Yes', 'apples; pumpkins; flowers', 'http://www.stonetavernorchards.com/'),
    'Jubilee Orchards': ('Yes', 'blueberries', 'http://jubileeorchards.com/'),
}

def update_csv(file_path):
    """Update the CSV file with research findings"""
    # Read the CSV file
    rows = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:  # Skip empty rows
                farm_name = row[1]  # Name is in column 1 (0-indexed)
                if farm_name in research_data:
                    has_upick, offerings, sources = research_data[farm_name]
                    # Update columns 18, 19, 20 (has upick, upick offerings, upick source)
                    if len(row) > 20:
                        row[18] = has_upick
                        row[19] = offerings
                        row[20] = sources
                    else:
                        # Extend row if needed
                        while len(row) < 21:
                            row.append('')
                        row[18] = has_upick
                        row[19] = offerings
                        row[20] = sources
                    print(f"Updated {farm_name}: {has_upick} - {offerings}")
            rows.append(row)
    
    # Write the updated CSV file
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print(f"CSV file updated successfully: {file_path}")

if __name__ == "__main__":
    csv_file = "/Users/pablo/Desktop/upick farms data/upickfarms_enriched_updated.csv"
    update_csv(csv_file)
    
    # Print summary
    print("\n--- Research Summary ---")
    for farm_name, (has_upick, offerings, sources) in research_data.items():
        if has_upick != 'Unknown':
            print(f"{farm_name}: {has_upick}")
            if offerings:
                print(f"  Crops: {offerings}")
            if sources:
                print(f"  Source: {sources}")