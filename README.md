# LinkedIn Post Generator

A CLI tool that uses DeepSeek AI to generate viral LinkedIn posts or post ideas in seconds.

## Features

- Generate a **full LinkedIn post** or a list of **post ideas**
- Choose from curated topics across 5 areas or **enter your own topic**
- Supports **3 languages**: Portuguese (Brazil), English (US), Spanish (Argentina)
- **Random topic generator** by area of interest
- Output is automatically **copied to clipboard** (Windows)
- Built-in **viralization techniques**: hook, storytelling, punchy sentences, hashtags, CTA

## Requirements

- Python 3.8+
- [DeepSeek API key](https://platform.deepseek.com/)
- `requests` library

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/linkedin-post-bot.git
cd linkedin-post-bot
```

**2. Install dependencies**

```bash
pip install requests
```

**3. Configure your API key**

Copy the example env file and add your DeepSeek API key:

```bash
cp .env.example .env
```

Edit `.env`:

```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

Alternatively, set the environment variable directly:

```bash
# Linux / macOS
export DEEPSEEK_API_KEY=your_key_here

# Windows CMD
set DEEPSEEK_API_KEY=your_key_here

# Windows PowerShell
$env:DEEPSEEK_API_KEY="your_key_here"
```

## Usage

```bash
python linkedin_post_generator.py
```

The CLI will guide you through:

1. **Topic** — enter a custom topic or pick a random one by area
2. **Mode** — full post or a list of ideas
3. **Language** — Portuguese (Brazil), English (US), or Spanish (Argentina)
4. **Confirmation** — review your choices before generating

### Available topic areas for random generation

| Area | Sample topics |
|------|--------------|
| `technology` | AI impact on daily work, automation, remote work |
| `career` | Promotions, rejections, job interviews, networking |
| `entrepreneurship` | Validating ideas, personal brand, scaling |
| `leadership` | Remote teams, feedback, leadership styles |
| `productivity` | Time management, deep work, procrastination |

## Example output

```
══════════════════════════════════════════════════════════
  RESULT
══════════════════════════════════════════════════════════

I almost quit my job the day I discovered this technique.

3 years ago, I was overwhelmed. 60+ emails a day. Back-to-back meetings.
Zero time to think.

Then I tried time-blocking — and everything changed.

...

#Productivity #DeepWork #CareerGrowth #Leadership #WorkLifeBalance
══════════════════════════════════════════════════════════
Content copied to clipboard.
```

## How it works

1. You select a topic and mode via the interactive CLI
2. The tool builds a structured prompt with LinkedIn viralization guidelines
3. The prompt is sent to the DeepSeek API (`deepseek-chat` model)
4. The generated content is printed and copied to your clipboard

## Configuration

All configuration lives at the top of `linkedin_post_generator.py`:

| Variable | Description |
|----------|-------------|
| `DEEPSEEK_MODEL` | DeepSeek model to use (default: `deepseek-chat`) |
| `SYSTEM_PROMPT` | The expert persona and viralization rules |
| `TOPICS_BY_AREA` | Topic pool for random generation |
| `LANGUAGE_INSTRUCTIONS` | Per-language instructions appended to each prompt |

## License

MIT
