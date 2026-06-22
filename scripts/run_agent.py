import os
import sys
import json
import requests

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

MODELS = [
    "qwen/qwen3-coder:free",
    "openai/gpt-oss-120b:free",
    "poolside/laguna-xs.2:free"
]


AGENT_MAP = {
    "architecture": (
        "common-ci/agents/architecture-review-agent.md",
        "common-ci/skills/spring-boot-architecture-skill.md"
    ),
    "code": (
        "common-ci/agents/code-review-agent.md",
        "common-ci/skills/java-code-review-skill.md"
    ),
    "security": (
        "common-ci/agents/security-review-agent.md",
        "common-ci/skills/java-security-skill.md"
    ),
    "testing": (
        "common-ci/agents/test-quality-agent.md",
        "common-ci/skills/java-testing-skill.md"
    )
}

agent_type = sys.argv[1]
context_file = sys.argv[2]
output_file = sys.argv[3]

agent_file, skill_file = AGENT_MAP[agent_type]

with open(agent_file) as f:
    agent_prompt = f.read()

with open(skill_file) as f:
    skill_prompt = f.read()

with open(context_file) as f:
    review_context = f.read()

prompt = f"""
{agent_prompt}

{skill_prompt}

Review the following pull request context:

{review_context}

Return markdown only.
"""

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    },
    timeout=120
)

print("Status:", response.status_code)
print("Response:", response.text)

response.raise_for_status()

result = response.json()

content = result["choices"][0]["message"]["content"]

with open(output_file, "w") as f:
    f.write(content)

print(f"Generated {output_file}")
