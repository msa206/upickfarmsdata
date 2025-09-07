#!/usr/bin/env python3
"""
Update CSV with farm research results - fixed version
"""

import csv
import shutil
from datetime import datetime

def update_csv_with_findings():
    """Update the main CSV with research findings"""
    
    # Research results from agents - only the ones with definitive findings
    definitive_findings = [
        # Agent 1 - only Annie's Orchard had definitive U-Pick info
        {"farm_id": "1421", "has_upick": "Yes", "upick_offerings": "strawberries; cherries; blueberries; peaches; apples", "upick_source": "https://upickfarmsusa.com/in/tippecanoe-county/annies-orchard/"},
        
        # Agent 3 - farms confirmed as NOT having U-Pick
        {"farm_id": "1137", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.twinoaksfarm.com/ - equine therapy, not agricultural u-pick"},
        {"farm_id": "1142", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.greenmeadowfarm.org/ - horse mentoring, no u-pick"},
        {"farm_id": "1150", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.localharvest.org/pleasant-valley-farm-M18676 - farmers markets only"},
        
        # Agent 4 - farms confirmed as NOT having U-Pick  
        {"farm_id": "1160", "has_upick": "No", "upick_offerings": "", "upick_source": "http://pinehillfarmvegetables.org/ - farm stand only, not U-Pick"},
        {"farm_id": "1162", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.greenhillsfarm.net/ - rental accommodations, not agricultural"},
        {"farm_id": "1165", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.rollingmeadowsfarm.com/ - horse breeding, not U-Pick"},
        {"farm_id": "1172", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.meadowridgefarm.com/ - wedding venue, not agricultural"},
        {"farm_id": "1175", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.countrymeadowfarm.com/ - horse breeding, wrong location"},
    ]
    
    # Create backup first
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f'upickfarms_enriched_updated_backup_{timestamp}.csv'
    shutil.copy('upickfarms_enriched_updated.csv', backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    # Read current CSV
    rows = []
    with open('upickfarms_enriched_updated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            # Clean up any None keys that might cause issues
            clean_row = {k: v for k, v in row.items() if k is not None}
            rows.append(clean_row)
    
    print(f"Loaded {len(rows)} rows from CSV")
    print(f"Headers: {headers}")
    
    # Update rows with findings
    updates_made = 0
    for finding in definitive_findings:
        farm_id = finding["farm_id"]
        for row in rows:
            if row.get('id') == farm_id:
                current_upick = row.get('has upick', '').strip()
                if not current_upick:  # Only update if blank
                    row['has upick'] = finding["has_upick"]
                    row['upick offerings'] = finding["upick_offerings"] 
                    row['upick source'] = finding["upick_source"]
                    updates_made += 1
                    print(f"✓ Updated farm ID {farm_id} ({row.get('name', 'Unknown')}) - {finding['has_upick']}")
                else:
                    print(f"⚠ Farm ID {farm_id} already has upick data: {current_upick}")
                break
    
    # Write updated CSV
    print(f"\nWriting updated CSV with {updates_made} changes...")
    with open('upickfarms_enriched_updated.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ CSV updated successfully! Made {updates_made} updates.")
    
    # Log the updates
    with open('research_updates_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Farm Research Updates - {datetime.now()}\n")
        f.write(f"{'='*50}\n")
        f.write(f"Total updates made: {updates_made}\n\n")
        
        for finding in definitive_findings:
            f.write(f"Farm ID {finding['farm_id']}: {finding['has_upick']}\n")
            if finding['upick_offerings']:
                f.write(f"  Offerings: {finding['upick_offerings']}\n")
            f.write(f"  Source: {finding['upick_source']}\n\n")
    
    return updates_made

if __name__ == "__main__":
    updates_made = update_csv_with_findings()
    print(f"\n🎉 Completed: {updates_made} farms updated in CSV")
    print("📝 Updates logged to research_updates_log.txt")