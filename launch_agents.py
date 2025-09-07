#!/usr/bin/env python3
"""
Launch farm research agents and handle their results
"""

import json
import csv

def load_assignments():
    """Load farm assignments from the JSON file"""
    try:
        with open("current_batch_assignments.json", 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading assignments: {e}")
        return None

def create_research_prompt(agent_id, farms):
    """Create research prompt for a specific agent"""
    prompt = f"""You are Farm Research Agent {agent_id}. Your task is to research each farm to determine if they offer U-Pick (pick-your-own) services.

For each farm, please:
1. Visit their website if available
2. Look for information about U-Pick, pick-your-own, or self-harvest services  
3. Determine if they offer U-Pick services (Yes/No/Unknown)
4. If yes, list what crops/items are available for U-Pick
5. Provide the source URL where you found this information

Here are your {len(farms)} assigned farms:

"""
    
    for i, farm in enumerate(farms, 1):
        prompt += f"{i}. **{farm['name']}** (ID: {farm['id']})\n"
        prompt += f"   Website: {farm.get('site', 'No website')}\n"
        prompt += f"   Location: {farm.get('city', '')}, {farm.get('state', '')}\n"
        prompt += f"   Phone: {farm.get('phone', 'No phone')}\n\n"
    
    prompt += """Please respond with your findings in this exact format for each farm:

FARM_ID: [farm_id]
FARM_NAME: [name]  
HAS_UPICK: [Yes/No/Unknown]
UPICK_OFFERINGS: [list of crops/items, or "N/A" if no U-Pick]
SOURCE: [URL where you found this information, or "No information found"]
---

Important: Research all farms thoroughly. If a website doesn't work, try searching for the farm name and location online. Be sure to provide findings for ALL assigned farms."""

    return prompt

def update_csv_with_results(farm_id, has_upick, upick_offerings, upick_source):
    """Update the main CSV file with research results"""
    try:
        # Read current CSV
        rows = []
        headers = []
        
        with open('upickfarms_enriched_updated.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                if row['id'] == str(farm_id):
                    row['has upick'] = has_upick
                    row['upick offerings'] = upick_offerings
                    row['upick source'] = upick_source
                rows.append(row)
        
        # Write updated CSV
        with open('upickfarms_enriched_updated.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            
        print(f"✓ Updated farm ID {farm_id} in CSV")
        return True
        
    except Exception as e:
        print(f"✗ Error updating CSV for farm {farm_id}: {e}")
        return False

def main():
    """Main function to launch agents"""
    assignments = load_assignments()
    if not assignments:
        print("Failed to load farm assignments")
        return
    
    print(f"Loaded assignments for {len(assignments)} agents")
    
    # Print agent assignments summary
    for agent_id, data in assignments.items():
        if 'farms' in data and data['farms']:
            print(f"{agent_id}: {len(data['farms'])} farms assigned")
    
    return assignments

if __name__ == "__main__":
    main()