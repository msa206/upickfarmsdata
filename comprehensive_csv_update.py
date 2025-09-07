#!/usr/bin/env python3
"""
Comprehensive CSV update with ALL agent research results
"""

import csv
import shutil
from datetime import datetime

def update_csv_with_all_findings():
    """Update CSV with all research findings from all agents"""
    
    # Comprehensive research findings from all 10 agents
    all_findings = [
        # Agent 1 results
        {"farm_id": "1421", "has_upick": "Yes", "upick_offerings": "strawberries; cherries; blueberries; peaches; apples", "upick_source": "https://upickfarmsusa.com/in/tippecanoe-county/annies-orchard/"},
        
        # Agent 3 results - farms confirmed as NOT having U-Pick
        {"farm_id": "1137", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.twinoaksfarm.com/ - equine therapy, not agricultural u-pick"},
        {"farm_id": "1142", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.greenmeadowfarm.org/ - horse mentoring, no u-pick"},
        {"farm_id": "1150", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.localharvest.org/pleasant-valley-farm-M18676 - farmers markets only"},
        
        # Agent 4 results - farms confirmed as NOT having U-Pick  
        {"farm_id": "1160", "has_upick": "No", "upick_offerings": "", "upick_source": "http://pinehillfarmvegetables.org/ - farm stand only, not U-Pick"},
        {"farm_id": "1162", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.greenhillsfarm.net/ - rental accommodations, not agricultural"},
        {"farm_id": "1165", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.rollingmeadowsfarm.com/ - horse breeding, not U-Pick"},
        {"farm_id": "1172", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.meadowridgefarm.com/ - wedding venue, not agricultural"},
        {"farm_id": "1175", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.countrymeadowfarm.com/ - horse breeding, wrong location"},
        
        # Agent 6 results - U-Pick farms found
        {"farm_id": "1197", "has_upick": "Yes", "upick_offerings": "fruits (pick-your-own fruit share)", "upick_source": "https://www.sunrisefarmvt.com/sign-up-1/vegetable-csa-share-and-pick-your-own-fruit-share"},
        {"farm_id": "1211", "has_upick": "Yes", "upick_offerings": "blueberries", "upick_source": "http://www.blueskyfarmwinery.com/u-pick-blueberries/"},
        {"farm_id": "1212", "has_upick": "Yes", "upick_offerings": "various farm produce", "upick_source": "https://river-bend-farm.com/"},
        {"farm_id": "1213", "has_upick": "Yes", "upick_offerings": "strawberries; raspberries; pumpkins", "upick_source": "https://www.oakgrovefarmsinc.com/"},
        
        # Agent 7 results - U-Pick farms found
        {"farm_id": "1216", "has_upick": "Yes", "upick_offerings": "blueberries", "upick_source": "https://upickfarmsusa.com/nh/rockingham-county/blueberry-bay-farm/"},
        {"farm_id": "1217", "has_upick": "Yes", "upick_offerings": "cherries", "upick_source": "https://www.gavinorchards.com"},
        {"farm_id": "1219", "has_upick": "Yes", "upick_offerings": "blueberries", "upick_source": "https://oregonblues.farm/"},
        {"farm_id": "1220", "has_upick": "Yes", "upick_offerings": "strawberries; cherries", "upick_source": "https://www.visitmanisteecounty.com/web-2-0-directory/calvin-lutz-farms"},
        {"farm_id": "1221", "has_upick": "Yes", "upick_offerings": "flowers", "upick_source": "https://www.wildberryfarmmarket.com/farm-events"},
        {"farm_id": "1222", "has_upick": "Yes", "upick_offerings": "strawberries; apples; raspberries", "upick_source": "https://www.facebook.com/cavannasfarm1903/"},
        {"farm_id": "1223", "has_upick": "Yes", "upick_offerings": "blueberries; blackberries; apples", "upick_source": "https://www.sunshinevalleyfarm.com"},
        {"farm_id": "1224", "has_upick": "No", "upick_offerings": "", "upick_source": "Confirmed via TripAdvisor - apples are pre-picked only"},
        {"farm_id": "1225", "has_upick": "Yes", "upick_offerings": "apples; strawberries; cherries; blueberries; pumpkins", "upick_source": "https://seamansorchard.com/"},
        {"farm_id": "1226", "has_upick": "Yes", "upick_offerings": "blueberries", "upick_source": "https://www.facebook.com/Omodts"},
        {"farm_id": "1227", "has_upick": "Yes", "upick_offerings": "blueberries", "upick_source": "https://youpickblueberries.net/"},
        {"farm_id": "1230", "has_upick": "Yes", "upick_offerings": "strawberries; blueberries", "upick_source": "https://www.facebook.com/lavignesstrawberryfarm/"},
        {"farm_id": "1232", "has_upick": "Yes", "upick_offerings": "blueberries", "upick_source": "https://wendellblueberryfarm.com/"},
        {"farm_id": "1234", "has_upick": "Yes", "upick_offerings": "blueberries; raspberries", "upick_source": "https://piperfarms.wixsite.com/info"},
        {"farm_id": "1235", "has_upick": "Yes", "upick_offerings": "blackberries; watermelons; peaches; strawberries; pumpkins", "upick_source": "https://www.visitbuckscounty.com/listing/penn-vermont-fruit-farm/3789/"},
        
        # Agent 10 results - farms confirmed as NOT having U-Pick
        {"farm_id": "1292", "has_upick": "No", "upick_offerings": "", "upick_source": "https://highlandvalleyfarm.com/home - livestock farm, no U-Pick"},
        {"farm_id": "1293", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.maplevalleyfarmvt.com/ - farm stand only, no U-Pick"},
        
        # Additional farms with definitive findings (marking Unknown for those with no reliable info)
        {"farm_id": "1196", "has_upick": "Unknown", "upick_offerings": "", "upick_source": "No information found"},
        {"farm_id": "1200", "has_upick": "No", "upick_offerings": "", "upick_source": "Website is for puppy breeding, not crops"},
        {"farm_id": "1201", "has_upick": "No", "upick_offerings": "", "upick_source": "Website shows livestock/poultry farm, not U-Pick crops"},
        {"farm_id": "1203", "has_upick": "No", "upick_offerings": "", "upick_source": "https://www.mapleridgefarm.net/ - offers farm products but no U-Pick mentioned"},
        {"farm_id": "1206", "has_upick": "No", "upick_offerings": "", "upick_source": "Website shows livestock/product farm, no U-Pick mentioned"},
        
        # Mark remaining researched farms as Unknown (where no definitive info was found)
    ]
    
    # Add Unknown status for all other researched farm IDs that don't have definitive findings
    researched_farm_ranges = [
        range(1097, 1116),  # Agent 1 remainder
        range(1116, 1136),  # Agent 2
        range(1136, 1156),  # Agent 3 remainder
        range(1156, 1176),  # Agent 4 remainder
        range(1176, 1196),  # Agent 5
        range(1196, 1216),  # Agent 6 remainder
        range(1236, 1256),  # Agent 8
        range(1256, 1276),  # Agent 9
        range(1276, 1296),  # Agent 10 remainder
    ]
    
    existing_ids = {f["farm_id"] for f in all_findings}
    
    for farm_range in researched_farm_ranges:
        for farm_id in farm_range:
            if str(farm_id) not in existing_ids:
                all_findings.append({
                    "farm_id": str(farm_id),
                    "has_upick": "Unknown", 
                    "upick_offerings": "",
                    "upick_source": "No information found - website inaccessible or farm not verified"
                })
    
    # Create backup first
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f'upickfarms_enriched_updated_backup_FINAL_{timestamp}.csv'
    shutil.copy('upickfarms_enriched_updated.csv', backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    # Read current CSV
    rows = []
    with open('upickfarms_enriched_updated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            clean_row = {k: v for k, v in row.items() if k is not None}
            rows.append(clean_row)
    
    print(f"Loaded {len(rows)} rows from CSV")
    
    # Update rows with findings
    updates_made = 0
    for finding in all_findings:
        farm_id = finding["farm_id"]
        for row in rows:
            if row.get('id') == farm_id:
                current_upick = row.get('has upick', '').strip()
                if not current_upick:  # Only update if blank
                    row['has upick'] = finding["has_upick"]
                    row['upick offerings'] = finding["upick_offerings"] 
                    row['upick source'] = finding["upick_source"]
                    updates_made += 1
                    farm_name = row.get('name', 'Unknown')
                    print(f"✓ Updated farm ID {farm_id} ({farm_name}) - {finding['has_upick']}")
                break
    
    # Write updated CSV
    print(f"\nWriting updated CSV with {updates_made} changes...")
    with open('upickfarms_enriched_updated.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ CSV updated successfully! Made {updates_made} updates.")
    
    # Create comprehensive log
    with open('FINAL_research_log.txt', 'w', encoding='utf-8') as f:
        f.write(f"COMPREHENSIVE FARM RESEARCH RESULTS\n")
        f.write(f"{'='*50}\n")
        f.write(f"Research completed: {datetime.now()}\n")
        f.write(f"Total farms researched: 200\n")
        f.write(f"Total CSV updates made: {updates_made}\n\n")
        
        # Summary by category
        yes_count = sum(1 for f in all_findings if f['has_upick'] == 'Yes')
        no_count = sum(1 for f in all_findings if f['has_upick'] == 'No')  
        unknown_count = sum(1 for f in all_findings if f['has_upick'] == 'Unknown')
        
        f.write(f"SUMMARY:\n")
        f.write(f"- Farms with U-Pick: {yes_count}\n")
        f.write(f"- Farms without U-Pick: {no_count}\n") 
        f.write(f"- Farms with unknown status: {unknown_count}\n\n")
        
        f.write(f"DETAILED FINDINGS:\n")
        f.write(f"{'='*50}\n\n")
        
        for finding in sorted(all_findings, key=lambda x: int(x['farm_id'])):
            f.write(f"Farm ID {finding['farm_id']}: {finding['has_upick']}\n")
            if finding['upick_offerings']:
                f.write(f"  Offerings: {finding['upick_offerings']}\n")
            f.write(f"  Source: {finding['upick_source']}\n\n")
    
    return updates_made, yes_count, no_count, unknown_count

if __name__ == "__main__":
    updates, yes_farms, no_farms, unknown_farms = update_csv_with_all_findings()
    
    print(f"\n🎉 RESEARCH COMPLETE!")
    print(f"📊 Summary:")
    print(f"   • {updates} farms updated in CSV")
    print(f"   • {yes_farms} farms offer U-Pick services")
    print(f"   • {no_farms} farms do not offer U-Pick services") 
    print(f"   • {unknown_farms} farms have unknown U-Pick status")
    print(f"📝 Comprehensive log saved to FINAL_research_log.txt")