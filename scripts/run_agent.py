import os
import sys
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

MODELS = [
    "qwen/qwen3-coder:free",
    "openai/gpt-oss-20b:free",
    "google/gemma-3-27b-it:free"
]

MAX_CONTEXT_CHARS = 15000


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


if len(sys.argv) != 3:
    print("Usage:")
    print("python run_agent.py <review-context.txt> <output.md>")
    sys.exit(1)

review_context_file = sys.argv[1]
output_file = sys.argv[2]

# Load all agents
architecture_agent = read_file(
    "common-ci/agents/architecture-review-agent.md"
)

code_agent = read_file(
    "common-ci/agents/code-review-agent.md"
)

security_agent = read_file(
    "common-ci/agents/security-review-agent.md"
)

testing_agent = read_file(
    "common-ci/agents/test-quality-agent.md"
)

# Load all skills
architecture_skill = read_file(
    "common-ci/skills/spring-boot-architecture-skill.md"
)

code_skill = read_file(
    "common-ci/skills/java-code-review-skill.md"
)

security_skill = read_file(
    "common-ci/skills/java-security-skill.md"
)

testing_skill = read_file(
    "common-ci/skills/java-testing-skill.md"
)

# Load review context
review_context = read_file(review_context_file)

# Limit size
review_context = review_context[:MAX_CONTEXT_CHARS]

prompt = f"""
You are a Senior Platform Engineer.

Perform ALL reviews below and generate ONE markdown report.

==================================================
ARCHITECTURE REVIEW
==================================================

{architecture_agent}

{architecture_skill}

==================================================
CODE REVIEW
==================================================

{code_agent}

{code_skill}

==================================================
SECURITY REVIEW
==================================================

{security_agent}

{security_skill}

==================================================
TEST QUALITY REVIEW
==================================================

{testing_agent}

{testing_skill}

==================================================
PULL REQUEST CONTEXT
==================================================

{review_context}

==================================================

Return ONLY markdown in this format:

# Architecture Findings

## Critical

## Warning

## Recommendation

# Code Review Findings

## Critical

## Warning

## Recommendation

# Security Findings

## Critical

## Warning

## Recommendation

# Test Quality Findings

## Critical

## Warning

## Recommendation
"""

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

last_error = "Unknown Error"

for model in MODELS:

    print(f"\nTrying model: {model}")

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2
            },
            timeout=180
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print(response.text)

            if response.status_code in [404, 429, 500, 502, 503]:
                last_error = response.text
                continue

            response.raise_for_status()

        data = response.json()

        content = data["choices"][0]["message"]["content"]

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Review generated successfully using {model}")

        sys.exit(0)

    except Exception as e:
        print(f"Model {model} failed")
        print(str(e))
        last_error = str(e)

# If all models fail
with open(output_file, "w", encoding="utf-8") as f:
    f.write(
        "# AI Review Failed\n\n"
        "Unable to generate AI review.\n\n"
        "Last Error:\n\n"
        "```\n"
        f"{last_error}\n"
        "```\n"
    )

raise RuntimeError("All OpenRouter models failed")
