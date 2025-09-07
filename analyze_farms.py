import pandas as pd
import numpy as np
import random
import csv
from collections import Counter

def analyze_unknown_farms():
    # Read the CSV file
    file_path = r"C:\Users\pablo\Desktop\upickfarmsdata\upickfarms_enriched_updated.csv"
    df = pd.read_csv(file_path)
    
    print("Dataset shape:", df.shape)
    print("\nColumn names:")
    print(df.columns.tolist())
    
    # Check the 'has upick' column
    has_upick_column = 'has upick'
    print(f"\nValue counts for '{has_upick_column}' column:")
    print(df[has_upick_column].value_counts())
    
    # Find farms with 'unknown' status (case insensitive)
    unknown_farms = df[df[has_upick_column].str.lower() == 'unknown'].copy()
    
    print(f"\nNumber of farms with 'unknown' status: {len(unknown_farms)}")
    
    if len(unknown_farms) > 0:
        print("\nFirst few farms with 'unknown' status:")
        print(unknown_farms[['id', 'name', 'city', 'state', 'has upick']].head(10))
        
        # Randomly shuffle the unknown farms
        unknown_farms_shuffled = unknown_farms.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Distribute farms evenly across 6 agents
        num_agents = 6
        farms_per_agent = len(unknown_farms_shuffled) // num_agents
        remainder = len(unknown_farms_shuffled) % num_agents
        
        agent_assignments = {}
        start_idx = 0
        
        for agent_num in range(1, num_agents + 1):
            # Some agents get one extra farm if there's a remainder
            current_batch_size = farms_per_agent + (1 if agent_num <= remainder else 0)
            end_idx = start_idx + current_batch_size
            
            agent_farms = unknown_farms_shuffled.iloc[start_idx:end_idx]
            agent_assignments[f'agent_{agent_num}'] = agent_farms
            
            print(f"\nAgent {agent_num} assigned {len(agent_farms)} farms:")
            print("Farm IDs:", agent_farms['id'].tolist())
            print("Farm Names:", agent_farms['name'].tolist()[:3], "..." if len(agent_farms) > 3 else "")
            
            start_idx = end_idx
        
        # Verify no duplicates across agents
        all_assigned_ids = []
        for agent, farms in agent_assignments.items():
            all_assigned_ids.extend(farms['id'].tolist())
        
        print(f"\nVerification:")
        print(f"Total farms assigned: {len(all_assigned_ids)}")
        print(f"Unique farms assigned: {len(set(all_assigned_ids))}")
        print(f"No duplicates: {len(all_assigned_ids) == len(set(all_assigned_ids))}")
        
        return agent_assignments
    
    return {}

def update_farm_status(farm_id, new_status):
    """Update the has_upick status for a specific farm in the CSV file"""
    file_path = r"C:\Users\pablo\Desktop\upickfarmsdata\upickfarms_enriched_updated.csv"
    
    # Read current data
    df = pd.read_csv(file_path)
    
    # Update the specific farm
    mask = df['id'] == farm_id
    if mask.any():
        df.loc[mask, 'has upick'] = new_status
        
        # Save back to CSV
        df.to_csv(file_path, index=False)
        print(f"Updated farm ID {farm_id} status to '{new_status}'")
        return True
    else:
        print(f"Farm ID {farm_id} not found")
        return False

if __name__ == "__main__":
    agent_assignments = analyze_unknown_farms()