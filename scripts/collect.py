import urllib.request
import xml.etree.ElementTree as ET
import yaml
from datetime import datetime, timezone


def fetch_rss(url):
    print(f"Lecture du flux : {url}")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "MarketingMorning/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()

    root = ET.fromstring(data)

    articles = []

    for item in root.findall(".//item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        description = item.findtext("description", "")
        pub_date = item.findtext("pubDate", "")

        if title and link:
            articles.append({
                "title": title.strip(),
                "link": link.strip(),
                "description": description.strip(),
                "published": pub_date.strip()
            })

    return articles


def main():
    with open("sources/sources.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    all_articles = []

    for source in config["sources"]:
        rss = source.get("rss")

        if not rss:
            print(f"Pas de RSS pour : {source['name']}")
            continue

        try:
            articles = fetch_rss(rss)

            for article in articles:
                article["source"] = source["name"]
                article["category"] = source["category"]
                article["source_type"] = source["type"]

            all_articles.extend(articles)

            print(
                f"  → {len(articles)} article(s) trouvé(s)"
            )

        except Exception as error:
            print(
                f"  ⚠️ Impossible de récupérer {source['name']} : {error}"
            )

    with open("articles.yaml", "w", encoding="utf-8") as file:
        yaml.dump(
            {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "articles": all_articles
            },
            file,
            allow_unicode=True,
            sort_keys=False
        )

    print()
    print(f"TOTAL : {len(all_articles)} article(s) récupéré(s)")


if __name__ == "__main__":
    main()
