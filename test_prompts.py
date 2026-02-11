"""Test script to verify agent prompts load correctly from markdown files."""

import json
from pathlib import Path

def load_prompt(agent_name):
    """Load agent prompt from markdown file in prompts directory."""
    prompt_dir = Path(__file__).parent / "prompts"
    prompt_file = prompt_dir / f"{agent_name}.md"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()

# Agent names
AGENT_NAMES = [
    "RouterAgent",
    "DataExtractionAgent",
    "MarketResearchAgent",
    "ValuationAgent",
    "ScenarioAgent",
    "RiskAgent",
    "SynthesisAgent"
]

if __name__ == "__main__":
    print("Testing prompt loading from markdown files...\n")
    
    # Load all prompts
    AGENTS = {name: load_prompt(name) for name in AGENT_NAMES}
    
    print(f"✓ Successfully loaded {len(AGENTS)} agent prompts")
    print(f"✓ Agents: {', '.join(AGENTS.keys())}\n")
    
    # Show sample of RouterAgent prompt
    print("=" * 60)
    print("RouterAgent prompt preview:")
    print("=" * 60)
    print(AGENTS['RouterAgent'][:300])
    print("...\n")
    
    # Verify all prompts have content
    for name, prompt in AGENTS.items():
        print(f"✓ {name:25s} - {len(prompt):4d} characters")
    
    print("\n✓ All prompts loaded successfully!")
