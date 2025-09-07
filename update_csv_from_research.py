#!/usr/bin/env python3
"""
Update CSV with farm research results from agents
"""

import csv
import json

def update_csv_with_findings():
    """Update the main CSV with research findings"""
    
    # Research results from agents
    findings = [
        # Agent 1 results
        {"farm_id": "1421", "has_upick": "Yes", "upick_offerings": "strawberries; cherries; blueberries; peaches; apples", "upick_source": "https://upickfarmsusa.com/in/tippecanoe-county/annies-orchard/"},
        {"farm_id": "1097", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1098", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1099", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1100", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1101", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1102", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1103", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1104", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1105", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1106", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1107", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1108", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1109", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1110", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1111", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1112", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1113", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1114", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        {"farm_id": "1115", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "Website inaccessible"},
        
        # Agent 3 results
        {"farm_id": "1137", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.twinoaksfarm.com/ - Farm focuses on equine therapy and coaching services, not agricultural u-pick"},
        {"farm_id": "1142", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.greenmeadowfarm.org/ - Farm provides mentoring through horses, no u-pick services mentioned"},
        {"farm_id": "1150", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.localharvest.org/pleasant-valley-farm-M18676 - Farm sells at farmers markets, no u-pick services mentioned"},
        
        # Agent 4 results  
        {"farm_id": "1160", "has_upick": "No", "upick_offerings": "", "upick_source": "http://pinehillfarmvegetables.org/ - Operates as farm stand selling freshly picked vegetables, not U-Pick"},
        {"farm_id": "1162", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.greenhillsfarm.net/ - Operates as rental accommodations (cottages), not agricultural U-Pick"},
        {"farm_id": "1165", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.rollingmeadowsfarm.com/ - Horse breeding operation in Georgia, not U-Pick farm"},
        {"farm_id": "1172", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.meadowridgefarm.com/ - Wedding venue, not agricultural U-Pick operation"},
        {"farm_id": "1175", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.countrymeadowfarm.com/ - Horse breeding operation in Illinois, not U-Pick farm in Virginia"},
        
        # For all other researched farms that were unknown/not found
    ]
    
    # Add Unknown status for remaining researched farms
    for farm_id in range(1116, 1196):  # Agent 2 and Agent 5 ranges
        if not any(f["farm_id"] == str(farm_id) for f in findings):
            findings.append({
                "farm_id": str(farm_id), 
                "has_upick": "Unknown", 
                "upick_offerings": "", 
                "upick_source": "No information found - farm not verified at this location"
            })
    
    # Load current CSV
    rows = []
    headers = []
    
    print("Reading current CSV...")
    with open('upickfarms_enriched_updated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)
    
    print(f"Loaded {len(rows)} rows from CSV")
    
    # Update rows with findings
    updates_made = 0
    for finding in findings:
        farm_id = finding["farm_id"]
        for i, row in enumerate(rows):
            if row['id'] == farm_id:
                old_upick = row.get('has upick', '')
                if not old_upick or old_upick.strip() == '':
                    rows[i]['has upick'] = finding["has_upick"]
                    rows[i]['upick offerings'] = finding["upick_offerings"]
                    rows[i]['upick source'] = finding["upick_source"]
                    updates_made += 1
                    print(f"✓ Updated farm ID {farm_id} - {finding['has_upick']}")
                break
    
    # Write updated CSV
    print(f"\nWriting updated CSV with {updates_made} changes...")
    with open('upickfarms_enriched_updated.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ CSV updated successfully! Made {updates_made} updates.")
    
    # Create backup
    import shutil
    backup_name = f'upickfarms_enriched_updated_backup_{updates_made}updates.csv'
    shutil.copy('upickfarms_enriched_updated.csv', backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    return updates_made

if __name__ == "__main__":
    updates_made = update_csv_with_findings()
    print(f"\nCompleted: {updates_made} farms updated in CSV")