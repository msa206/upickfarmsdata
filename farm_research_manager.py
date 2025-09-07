#!/usr/bin/env python3
"""
Farm Research Manager
Handles CSV parsing, farm assignment to agents, and result tracking
"""

import csv
import json
import datetime
import os
import random

class FarmResearchManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.load_csv_data()
        self.assignment_log_file = "farm_assignments_log.txt"
        self.batch_log_file = "current_batch_assignments.json"
    
    def load_csv_data(self):
        """Load CSV data into memory"""
        self.data = []
        self.headers = []
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            for row in reader:
                self.data.append(row)
        
        print(f"Loaded {len(self.data)} farms from CSV")
        
    def find_blank_upick_farms(self, limit=200):
        """Find farms with blank 'has upick' column"""
        blank_farms = []
        
        for row in self.data:
            upick_value = row.get('has upick', '')
            if upick_value is None:
                upick_value = ''
            upick_value = str(upick_value).strip()
            if not upick_value or upick_value.lower() in ['', 'nan', 'none', 'null']:
                blank_farms.append(row)
        
        print(f"Found {len(blank_farms)} farms with blank 'has upick' column")
        
        if len(blank_farms) < limit:
            print(f"Only {len(blank_farms)} farms available, using all of them")
            return blank_farms
        else:
            # Randomly sample the requested number
            random.seed(42)  # For reproducible results
            selected_farms = random.sample(blank_farms, limit)
            print(f"Selected {len(selected_farms)} farms for research")
            return selected_farms
    
    def distribute_farms_to_agents(self, farms_list, num_agents=10):
        """Distribute farms to agents (20 farms each)"""
        farms_per_agent = len(farms_list) // num_agents
        remainder = len(farms_list) % num_agents
        
        agent_assignments = {}
        
        start_idx = 0
        for agent_id in range(1, num_agents + 1):
            # Give extra farms to first few agents if there's a remainder
            agent_farm_count = farms_per_agent + (1 if agent_id <= remainder else 0)
            end_idx = start_idx + agent_farm_count
            
            agent_farms = farms_list[start_idx:end_idx]
            agent_assignments[f"agent_{agent_id}"] = {
                "farms": agent_farms,
                "count": len(agent_farms),
                "status": "assigned",
                "assigned_at": datetime.datetime.now().isoformat()
            }
            
            start_idx = end_idx
            
        return agent_assignments
    
    def log_assignments(self, agent_assignments):
        """Log farm assignments to files"""
        # Write to JSON file for programmatic access
        with open(self.batch_log_file, 'w') as f:
            json.dump(agent_assignments, f, indent=2, default=str)
        
        # Write to text file for human readability
        with open(self.assignment_log_file, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Farm Research Batch - {datetime.datetime.now()}\n")
            f.write(f"{'='*50}\n")
            
            for agent_id, data in agent_assignments.items():
                f.write(f"\n{agent_id.upper()} - {data['count']} farms:\n")
                f.write("-" * 40 + "\n")
                
                for i, farm in enumerate(data['farms'], 1):
                    f.write(f"{i:2d}. {farm['name']} (ID: {farm['id']})\n")
                    f.write(f"    {farm['city']}, {farm['state']}\n")
                    f.write(f"    {farm['site']}\n\n")
        
        print(f"Assignments logged to {self.assignment_log_file} and {self.batch_log_file}")
    
    def update_farm_status(self, farm_id, has_upick, upick_offerings="", upick_source=""):
        """Update a farm's upick status in the CSV"""
        # Find the farm by ID
        found_farm = None
        farm_index = None
        
        for i, row in enumerate(self.data):
            if row['id'] == str(farm_id):
                found_farm = row
                farm_index = i
                break
        
        if not found_farm:
            print(f"Warning: Farm ID {farm_id} not found in CSV")
            return False
        
        # Update the columns
        self.data[farm_index]['has upick'] = has_upick
        if upick_offerings:
            self.data[farm_index]['upick offerings'] = upick_offerings
        if upick_source:
            self.data[farm_index]['upick source'] = upick_source
        
        # Save the updated CSV
        self.save_csv()
        print(f"Updated farm ID {farm_id} with upick status: {has_upick}")
        return True
    
    def save_csv(self):
        """Save the current data back to CSV"""
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.data)
    
    def get_research_prompt_for_agent(self, agent_farms):
        """Generate research prompt for an agent"""
        prompt = """You are a farm research agent. Your task is to research each farm to determine if they offer U-Pick (pick-your-own) services.

For each farm, please:
1. Visit their website if available
2. Look for information about U-Pick, pick-your-own, or self-harvest services
3. Determine if they offer U-Pick services (Yes/No)
4. If yes, list what crops/items are available for U-Pick
5. Provide the source URL where you found this information

Here are the farms to research:

"""
        
        for i, farm in enumerate(agent_farms, 1):
            prompt += f"{i}. **{farm['name']}** (ID: {farm['id']})\n"
            prompt += f"   Website: {farm['site']}\n"
            prompt += f"   Location: {farm['city']}, {farm['state']}\n"
            prompt += f"   Phone: {farm['phone']}\n\n"
        
        prompt += """Please respond with your findings in this format for each farm:

Farm ID: [farm_id]
Farm Name: [name]
Has U-Pick: [Yes/No]
U-Pick Offerings: [list of crops/items, or "N/A" if no U-Pick]
Source: [URL where you found this information, or "No information found"]

---

Start your research now and provide detailed findings for all assigned farms."""

        return prompt

def main():
    # Initialize the manager
    manager = FarmResearchManager("upickfarms_enriched_updated.csv")
    
    # Find farms with blank upick column
    print("Finding farms with blank 'has upick' column...")
    blank_farms = manager.find_blank_upick_farms(200)
    
    if not blank_farms:
        print("No farms found with blank 'has upick' column!")
        return
    
    print(f"Found {len(blank_farms)} farms to research")
    
    # Distribute farms to agents
    print("Distributing farms to 10 agents...")
    agent_assignments = manager.distribute_farms_to_agents(blank_farms, 10)
    
    # Log the assignments
    manager.log_assignments(agent_assignments)
    
    print("\nAgent farm distribution:")
    for agent_id, data in agent_assignments.items():
        print(f"{agent_id}: {data['count']} farms")
    
    return agent_assignments

if __name__ == "__main__":
    assignments = main()