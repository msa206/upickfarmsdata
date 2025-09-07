#!/usr/bin/env python3
"""
Extract farms marked as 'Unknown' for re-research with improved methods
"""

import csv
import json
import random

def extract_unknown_farms():
    """Extract farms marked as Unknown that need better research"""
    
    unknown_farms = []
    
    # Read current CSV
    with open('upickfarms_enriched_updated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            upick_status = row.get('has upick', '').strip()
            if upick_status == 'Unknown':
                unknown_farms.append(row)
    
    print(f"Found {len(unknown_farms)} farms marked as 'Unknown'")
    
    # Select a manageable number for re-research (let's do 100 farms across 5 agents = 20 each)
    if len(unknown_farms) > 100:
        selected_farms = random.sample(unknown_farms, 100)
        print(f"Selected 100 farms for re-research")
    else:
        selected_farms = unknown_farms
        print(f"Will re-research all {len(selected_farms)} unknown farms")
    
    # Distribute to 5 agents (20 farms each)
    farms_per_agent = len(selected_farms) // 5
    remainder = len(selected_farms) % 5
    
    agent_assignments = {}
    start_idx = 0
    
    for agent_id in range(1, 6):  # 5 agents
        agent_farm_count = farms_per_agent + (1 if agent_id <= remainder else 0)
        end_idx = start_idx + agent_farm_count
        
        agent_farms = selected_farms[start_idx:end_idx]
        agent_assignments[f"improved_agent_{agent_id}"] = {
            "farms": agent_farms,
            "count": len(agent_farms),
            "status": "ready_for_research"
        }
        
        start_idx = end_idx
    
    # Save assignments
    with open('unknown_farms_reassignment.json', 'w') as f:
        json.dump(agent_assignments, f, indent=2, default=str)
    
    print("\nImproved Agent Assignments:")
    for agent_id, data in agent_assignments.items():
        print(f"{agent_id}: {data['count']} farms")
    
    return agent_assignments

if __name__ == "__main__":
    assignments = extract_unknown_farms()