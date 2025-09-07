#!/usr/bin/env python3
import json

def get_agent_farms(agent_id):
    """Get farms for a specific agent"""
    with open("current_batch_assignments.json", 'r') as f:
        data = json.load(f)
    
    return data[f"agent_{agent_id}"]["farms"]

def create_prompt(agent_id):
    """Create research prompt for agent"""
    farms = get_agent_farms(agent_id)
    
    prompt = f"""Research the following {len(farms)} farms to determine if they offer U-Pick (pick-your-own) services.

For each farm:
1. Visit their website if available
2. Search for U-Pick, pick-your-own, or self-harvest information
3. Determine: Yes/No/Unknown
4. List available crops if U-Pick is offered
5. Provide source URL

Your assigned farms:

"""
    
    for i, farm in enumerate(farms, 1):
        prompt += f"{i}. **{farm['name']}** (ID: {farm['id']})\n"
        prompt += f"   Website: {farm.get('site', 'No website')}\n"
        prompt += f"   Location: {farm.get('city', '')}, {farm.get('state', '')}\n"
        prompt += f"   Phone: {farm.get('phone', 'No phone')}\n\n"
    
    prompt += """Please respond for each farm in this format:

FARM_ID: [farm_id]
FARM_NAME: [name]
HAS_UPICK: [Yes/No/Unknown] 
UPICK_OFFERINGS: [crops/items or "N/A"]
SOURCE: [URL or "No information found"]
---

Research all farms thoroughly and provide findings for ALL assigned farms."""

    return prompt

# Generate prompts for all 10 agents
if __name__ == "__main__":
    for i in range(1, 11):
        prompt = create_prompt(i)
        print(f"=== AGENT {i} PROMPT ===")
        print(prompt[:500] + "...")
        print("\n")