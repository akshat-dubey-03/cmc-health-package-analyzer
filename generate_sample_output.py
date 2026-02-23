import markdown
from scraper import scrape_health_packages
from llm_analyzer import analyze_packages


def parse_packages(raw_text):
    """
    Convert the raw scraped string into a list of dicts.
    Each block from the scraper looks like:
    '65% Off | Basic Panel in CMC (Vellore) Test | Include 83 Parameters | CBC,... | 799 2270 Read More'
    """
    packages = []
    for block in raw_text.split("\n\n"):
        block = block.strip()
        if not block:
            continue

        parts = [p.strip() for p in block.split(" | ")]

        # Extract discount e.g. "65% Off"
        discount = ""
        name = ""
        parameters = ""
        tests = ""
        discounted_price = ""
        original_price = ""

        for part in parts:
            if re.match(r"^\d+%\s*Off$", part, re.IGNORECASE):
                discount = part
            elif "Include" in part and "Parameters" in part:
                parameters = part
            elif "Read More" in part or re.search(r"^\d+\s+\d+", part):
                # price line like "799 2270 Read More"
                prices = re.findall(r"\d+", part)
                if len(prices) >= 2:
                    discounted_price = prices[0]
                    original_price = prices[1]
            elif "in CMC" in part or "Test" in part:
                # name line like "Basic Panel in CMC (Vellore) Test"
                name = re.sub(r"\s*Test\s*$", "", part).strip()
            elif not name and len(part) > 5:
                tests = part

        if not name:
            name = parts[0] if parts else "Unknown"

        packages.append({
            "name": name,
            "parameters": parameters or "N/A",
            "tests": tests or "N/A",
            "discounted_price": discounted_price or "N/A",
            "original_price": original_price or "N/A",
            "discount": discount or "N/A",
        })

    return packages


def generate_html(llm_markdown):
    # ── Convert LLM markdown → HTML ───────────────────────────────────────
    llm_html = markdown.markdown(llm_markdown, extensions=["tables", "fenced_code"])

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CMC Health Package Analysis</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f9;
            padding: 30px 40px;
            color: #333;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 10px;
            color: #2c3e50;
            font-size: 2em;
        }}
        .subtitle {{
            text-align: center;
            color: #777;
            margin-bottom: 30px;
            font-size: 0.95em;
        }}
        /* ── LLM Analysis ── */
        .llm-box {{
            background: white;
            border-radius: 10px;
            padding: 25px 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            line-height: 1.7;
        }}
        .llm-box h1, .llm-box h2, .llm-box h3 {{
            color: #2c3e50;
            margin: 18px 0 8px;
        }}
        .llm-box h2 {{ font-size: 1.15em; border-bottom: 1px solid #eee; padding-bottom: 4px; }}
        .llm-box table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 0.88em;
        }}
        .llm-box th {{ background: #3498db; color: white; padding: 10px 14px; }}
        .llm-box td {{ padding: 9px 14px; border-bottom: 1px solid #eee; }}
        .llm-box tr:hover td {{ background: #f0f7ff; }}
        .llm-box ul, .llm-box ol {{ margin: 8px 0 8px 22px; }}
        .llm-box li {{ margin: 4px 0; }}
        .llm-box code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .llm-box strong {{ color: #2c3e50; }}
    </style>
</head>
<body>
    <h1>🚀 CMC Health Package Analysis</h1>
    <p class="subtitle">Source: docopd.com — CMC Vellore</p>

    <div class="section-title">🧠 AI Analysis &amp; Recommendations</div>
    <div class="llm-box">
        {llm_html}
    </div>
</body>
</html>"""
    return html_content


if __name__ == "__main__":
    url = "https://www.docopd.com/en-in/lab/cmc-vellore"
    print("🔍 Scraping health packages...")
    raw_text = scrape_health_packages(url)

    if raw_text.startswith("Error") or raw_text.startswith("No health"):
        print(f"❌ {raw_text}")
        exit(1)

    print("🧠 Running LLM analysis (this may take a few seconds)...")
    llm_result = analyze_packages(raw_text)

    html_output = generate_html(llm_result)

    output_file = "docs/sample_output.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ Full sample output saved to '{output_file}' — open it in your browser!")