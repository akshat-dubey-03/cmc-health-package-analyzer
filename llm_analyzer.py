import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def analyze_packages(text):
    """Use OpenRouter LLM to analyze scraped health package data."""
    if not text or text.startswith("Error") or text.startswith("No health"):
        return text

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "❌ **OpenRouter API key not found.** Please create a `.env` file with:\n\n```\nOPENROUTER_API_KEY=your_key_here\n```"

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        prompt = f"""You are a healthcare analyst. Analyze the following health package data scraped from a website.

For each package found, extract and present:
1. **Package Name**
2. **Number of Parameters/Tests included**
3. **Tests Included** (list them)
4. **Discounted Price (₹)**
5. **Original Price (₹)**
6. **Discount Percentage**

After listing all packages, provide:
- A **comparison table** in markdown
- **Star ratings** (⭐ out of 5) based on value for money (tests per rupee)
- **Recommendations** for:
  - 🧑 Young Adults
  - 👴 Senior Citizens
  - 💰 Budget-Friendly Option
  - 🏆 Best Overall Value

Here is the scraped data:
---
{text}
---

Format your response in clean markdown."""

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful healthcare package analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        result = response.choices[0].message.content
        return result

    except Exception as e:
        return f"❌ **LLM Analysis Error:** {e}"