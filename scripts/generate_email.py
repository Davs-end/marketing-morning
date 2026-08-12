import json
from datetime import datetime
from pathlib import Path


INPUT_FILE = "analysis.json"
OUTPUT_FILE = "marketing_morning.html"


def importance_label(score):
    if score >= 5:
        return "🔥 À retenir"
    elif score >= 4:
        return "⭐ Important"
    else:
        return "💡 À connaître"


def generate_email(data):
    articles = data.get("articles", [])

    today = datetime.now().strftime("%d/%m/%Y")

    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Marketing Morning - {today}</title>

<style>

body {{
    margin: 0;
    padding: 0;
    background: #f4f6f8;
    font-family: Arial, Helvetica, sans-serif;
    color: #202124;
}}

.container {{
    max-width: 680px;
    margin: 0 auto;
    background: #ffffff;
}}

.header {{
    padding: 30px 25px;
    background: #111827;
    color: white;
}}

.header h1 {{
    margin: 0;
    font-size: 28px;
}}

.header p {{
    margin: 8px 0 0 0;
    color: #d1d5db;
}}

.content {{
    padding: 25px;
}}

.article {{
    padding: 22px 0;
    border-bottom: 1px solid #e5e7eb;
}}

.article:last-child {{
    border-bottom: none;
}}

.category {{
    font-size: 13px;
    font-weight: bold;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 8px;
}}

.article h2 {{
    margin: 5px 0 12px 0;
    font-size: 21px;
    line-height: 1.3;
}}

.summary {{
    font-size: 16px;
    line-height: 1.6;
}}

.box {{
    margin-top: 14px;
    padding: 14px;
    background: #f3f4f6;
    border-radius: 8px;
    line-height: 1.5;
}}

.source {{
    margin-top: 15px;
}}

.source a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: bold;
}}

.footer {{
    padding: 20px 25px;
    background: #f9fafb;
    color: #6b7280;
    font-size: 12px;
    line-height: 1.5;
}}

</style>
</head>

<body>

<div class="container">

<div class="header">

<h1>☀️ Marketing Morning</h1>

<p>Votre veille marketing quotidienne — {today}</p>

</div>

<div class="content">
"""

    if not articles:

        html += """
<h2>Aucune information majeure aujourd'hui.</h2>

<p>
Le système n'a identifié aucune actualité suffisamment
importante pour votre veille marketing.
</p>
"""

    else:

        for article in articles:

            title = article.get(
                "title",
                ""
            )

            category = article.get(
                "category",
                "Marketing"
            )

            importance = article.get(
                "importance",
                0
            )

            summary = article.get(
                "factual_summary",
                ""
            )

            why = article.get(
                "why_important",
                ""
            )

            impact = article.get(
                "marketing_impact",
                ""
            )

            recommendation = article.get(
                "recommendation",
                ""
            )

            source_name = article.get(
                "source_name",
                ""
            )

            source_url = article.get(
                "source_url",
                ""
            )

            html += f"""

<div class="article">

<div class="category">
{importance_label(importance)} · {category}
</div>

<h2>{title}</h2>

<div class="summary">
{summary}
</div>

<div class="box">
<strong>Pourquoi c'est important :</strong><br>
{why}
</div>

<div class="box">
<strong>Impact marketing :</strong><br>
{impact}
</div>

<div class="box">
<strong>🎯 À retenir / À faire :</strong><br>
{recommendation}
</div>

<div class="source">
🔗 <a href="{source_url}">
Lire la source officielle — {source_name}
</a>
</div>

</div>
"""

    html += """

</div>

<div class="footer">

Cette veille est générée automatiquement à partir
des sources sélectionnées dans Marketing Morning.

Les informations sont basées sur les sources originales.
Les liens renvoient vers les sources utilisées pour
l'analyse.

</div>

</div>

</body>
</html>
"""

    return html


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    html = generate_email(data)

    Path(
        OUTPUT_FILE
    ).write_text(
        html,
        encoding="utf-8"
    )

    print(
        f"Email généré : {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
