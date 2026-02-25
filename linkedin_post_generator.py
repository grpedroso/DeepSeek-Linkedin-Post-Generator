import os
import subprocess
import sys
import json
import random
import requests
from pathlib import Path


def load_dotenv(env_path: str = ".env"):
    """Load variables from a .env file into os.environ."""
    path = Path(env_path)
    if not path.exists():
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


load_dotenv()

# ──────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

SYSTEM_PROMPT = """You are an expert at creating viral LinkedIn posts.
Always apply modern viralization techniques:
- Storytelling: start with a personal story or relatable situation
- Short, punchy sentences: maximum 2 lines per paragraph
- Strong hook on the first line to grab attention immediately
- Strategic emojis to boost visual engagement
- Relevant hashtags at the end (5 to 8)
- Clear and direct call to action at the end
- Structure: Hook -> Development -> Insight -> CTA
- Tone: authentic, human, straight to the point

Your goal is to create content that drives real engagement, comments, and shares."""

TOPICS_BY_AREA = {
    "technology": [
        "How AI is changing my daily work routine",
        "Digital transformation: what nobody tells you",
        "Most valuable tech skills in 2025",
        "The future of remote and hybrid work",
        "Automation: career threat or opportunity?",
    ],
    "career": [
        "How I got promoted without asking",
        "Mistakes I made in the early years of my career",
        "The importance of authentic networking",
        "How to handle professional rejections",
        "What really matters in a job interview",
    ],
    "entrepreneurship": [
        "How I validated my business idea with $0",
        "The biggest mistakes first-time entrepreneurs make",
        "Building a strong personal brand from scratch",
        "The truth about being an entrepreneur nobody talks about",
        "How to scale a business without losing its soul",
    ],
    "leadership": [
        "What I learned leading remote teams",
        "How to give tough feedback with empathy",
        "The difference between being a boss and a leader",
        "How to motivate a team during a crisis",
        "Situational leadership: adapting is the key",
    ],
    "productivity": [
        "How I organize my week to do more in less time",
        "The technique that changed my relationship with work",
        "Why doing less can deliver more results",
        "How I finally stopped procrastinating",
        "Deep work: the power of focused effort",
    ],
}

LANGUAGE_INSTRUCTIONS = {
    "pt-br": "Respond in Brazilian Portuguese.",
    "en-us": "Respond in English (US).",
    "es-ar": "Respond in Spanish (Argentina).",
}

LANGUAGE_OPTIONS = {
    "1": ("pt-br", "Portuguese (Brazil)"),
    "2": ("en-us", "English (US)"),
    "3": ("es-ar", "Spanish (Argentina)"),
}

MODE_LABELS = {
    "1": "Full post",
    "2": "Post ideas",
}


# ──────────────────────────────────────────────────────────────
# PROMPT BUILDER
# ──────────────────────────────────────────────────────────────
def build_prompt(topic: str, mode: str, language: str) -> str:
    lang_instruction = LANGUAGE_INSTRUCTIONS[language]

    if mode == "1":
        action = (
            "Write a complete LinkedIn post about the topic below. "
            "The post should be between 150 and 300 words, engaging, human, "
            "and follow LinkedIn best practices for virality."
        )
    else:
        action = (
            "Suggest 5 creative LinkedIn post ideas about the topic below. "
            "For each idea provide: a hook (opening line) and a brief summary "
            "of the narrative angle to explore."
        )

    return f"{lang_instruction}\n\n{action}\n\nTopic: {topic}"


# ──────────────────────────────────────────────────────────────
# API CALLER
# ──────────────────────────────────────────────────────────────
def call_deepseek_api(prompt: str, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.85,
        "max_tokens": 1024,
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        raise RuntimeError("Connection timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Connection error. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 401:
            raise RuntimeError("Invalid or unauthorized API key.")
        elif status == 429:
            raise RuntimeError("Rate limit reached. Please wait and try again.")
        else:
            raise RuntimeError(f"API error (HTTP {status}): {e.response.text}")
    except (KeyError, IndexError, json.JSONDecodeError):
        raise RuntimeError("Unexpected API response. Please try again.")


# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
def sep(char="─", width=58):
    print(char * width)


def ask(prompt: str, valid: list = None) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("  Invalid input. Please try again.")
            continue
        if valid and value not in valid:
            print(f"  Invalid option. Choose from: {', '.join(valid)}")
            continue
        return value


def get_random_topic(area: str) -> str:
    area_lower = area.lower().strip()
    for key, topics in TOPICS_BY_AREA.items():
        if key in area_lower or area_lower in key:
            return random.choice(topics)
    all_topics = [t for topics in TOPICS_BY_AREA.values() for t in topics]
    return random.choice(all_topics)


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────
def main():
    print()
    sep("═")
    print("  LINKEDIN POST GENERATOR")
    print("  Powered by DeepSeek AI")
    sep("═")
    print()

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable not found.")
        print("Set it before running the script:")
        print("  export DEEPSEEK_API_KEY=your_key_here   (Linux/Mac)")
        print("  set DEEPSEEK_API_KEY=your_key_here      (Windows CMD)")
        sys.exit(1)

    # ── Topic ─────────────────────────────────────────────────
    sep()
    print("  [1] Enter topic manually")
    print("  [2] Generate random topic by area of interest")
    print()
    topic_mode = ask("  Choose [1/2]: ", ["1", "2"])

    if topic_mode == "1":
        topic = ask("\n  Enter the post topic: ")
    else:
        areas = ", ".join(TOPICS_BY_AREA.keys())
        area = ask(f"\n  Area of interest ({areas}): ")
        topic = get_random_topic(area)
        print(f"\n  Random topic: {topic}")

    # ── Mode ──────────────────────────────────────────────────
    print()
    sep()
    print("  [1] Generate the full post")
    print("  [2] Only suggest post ideas")
    print()
    mode = ask("  Choose [1/2]: ", ["1", "2"])

    # 
    # print()
    # sep()
    # print("Would you like to add instructions?")
    # print()
    # mode = ask("  Choose [s/n]: ", ["s", "n"])
    # ── Language ──────────────────────────────────────────────
    print()
    sep()
    print("  [1] Portuguese (Brazil)")
    print("  [2] English (US)")
    print("  [3] Spanish (Argentina)")
    print()
    lang_choice = ask("  Choose [1/2/3]: ", ["1", "2", "3"])
    language, language_label = LANGUAGE_OPTIONS[lang_choice]

    # ── Confirmation ──────────────────────────────────────────
    print()
    sep()
    print(f"  Topic    : {topic}")
    print(f"  Mode     : {MODE_LABELS[mode]}")
    print(f"  Language : {language_label}")
    sep()
    print()
    confirm = ask("  Confirm and generate? [y/n]: ", ["y", "n", "Y", "N"])
    if confirm.lower() == "n":
        print("\n  Operation cancelled.")
        sys.exit(0)

    # ── API call ──────────────────────────────────────────────
    print()
    print("  Generating content, please wait...")
    print()

    prompt = build_prompt(topic, mode, language)

    try:
        result = call_deepseek_api(prompt, api_key)
    except RuntimeError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    # ── Result ────────────────────────────────────────────────
    sep("═")
    print("  RESULT")
    sep("═")
    print()
    print(result)
    print()
    sep("═")
    print()
    try:                                                                          
        subprocess.run(["clip"], input=result.encode("utf-16"), check=True)                                                                           
        copied = True
    except Exception:                                                             
        copied = False

    if copied:
        print("Content copied to clipboard.")

if __name__ == "__main__":
    main()
