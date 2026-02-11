import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI()

# -------------------------
# Load prompts from markdown files
# -------------------------
def load_prompt(agent_name):
    """Load agent prompt from markdown file in prompts directory."""
    prompt_dir = Path(__file__).parent / "prompts"
    prompt_file = prompt_dir / f"{agent_name}.md"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()

# -------------------------
# Agent registry
# -------------------------
AGENT_NAMES = [
    "RouterAgent",
    "DataExtractionAgent",
    "MarketResearchAgent",
    "ValuationAgent",
    "ScenarioAgent",
    "RiskAgent",
    "SynthesisAgent"
]

# Load all agent prompts at startup
AGENTS = {name: load_prompt(name) for name in AGENT_NAMES}

def run_agent(agent_name, user_input, context=None):
    system_prompt = AGENTS[agent_name]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    if context:
        messages.append({"role": "assistant", "content": json.dumps(context)})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=0
    )

    return json.loads(response.choices[0].message.content)

# -------------------------
# Orchestration
# -------------------------
def run_pipeline(user_request):
    # Step 1: Router
    plan = run_agent("RouterAgent", user_request)

    context = {}

    # Step 2: Execute agents in order
    for step in plan["tasks"]:
        agent = step["agent"]
        print(f"Running {agent}...")

        output = run_agent(agent, user_request, context)
        context[agent] = output

    # Step 3: Synthesis
    final_output = run_agent("SynthesisAgent", user_request, context)

    return final_output

# -------------------------
# Example
# -------------------------
if __name__ == "__main__":
    user_request = "Underwrite a 180-unit multifamily development in Helotes."
    result = run_pipeline(user_request)
    print(json.dumps(result, indent=2))