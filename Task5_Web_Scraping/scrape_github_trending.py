"""
Task 5: Web Data Extraction & Analysis
------------------------------------------
- Collect data from a publicly available website using BeautifulSoup.
- Extract structured information (repo name, language, stars, description).
- Clean and organize the collected data into a structured dataset.
- Perform exploratory analysis to identify trends and patterns.
- Bonus: Automate the scraping process and export results to CSV/Excel.

Source: https://github.com/trending (GitHub's public Trending Repositories page)

Note on ethics/legality: this scrapes a single public page, respects a normal browser
User-Agent, makes only one request, and does not hit the site repeatedly or bypass any
login/paywall. Always check a site's robots.txt and Terms of Service before scraping.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

URL = "https://github.com/trending"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraping exercise; contact: student project)"}


def fetch_page(url):
    """Fetch a page with a polite delay and basic error handling."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    time.sleep(1)  # be polite - avoid hammering the server
    return response.text


def parse_star_count(text):
    """Convert GitHub's formatted star counts (e.g. '12,345') into an integer."""
    if not text:
        return 0
    cleaned = text.strip().replace(",", "")
    return int(cleaned) if cleaned.isdigit() else 0


def extract_repos(html):
    """Extract structured repo data from the Trending page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    repo_cards = soup.select("article.Box-row")

    records = []
    for card in repo_cards:
        # Repo name — build from the URL (owner/repo) since the visible text
        # is split across separate nodes with inconsistent whitespace
        title_tag = card.select_one("h2 a")
        full_name = title_tag["href"].strip("/") if title_tag else None

        # Description
        desc_tag = card.select_one("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # Programming language
        lang_tag = card.select_one('[itemprop="programmingLanguage"]')
        language = lang_tag.get_text(strip=True) if lang_tag else "Not specified"

        # Total stars (first star link in the card)
        star_tag = card.select_one('a[href*="/stargazers"]')
        total_stars = parse_star_count(star_tag.get_text(strip=True)) if star_tag else 0

        # Stars gained today/this week (shown as "N stars today")
        today_tag = card.select_one("span.d-inline-block.float-sm-right")
        stars_today = 0
        if today_tag:
            match = re.search(r"([\d,]+)\s+stars? (today|this week)", today_tag.get_text(strip=True))
            if match:
                stars_today = parse_star_count(match.group(1))

        repo_url = "https://github.com" + title_tag["href"] if title_tag else None

        records.append({
            "RepoName": full_name,
            "Description": description,
            "Language": language,
            "TotalStars": total_stars,
            "StarsGainedRecently": stars_today,
            "URL": repo_url,
        })

    return records


def clean_dataset(df):
    """Basic cleaning: drop incomplete rows, fill blanks, correct types."""
    df = df.dropna(subset=["RepoName"])
    df["Description"] = df["Description"].replace("", "No description provided")
    df["Language"] = df["Language"].replace("", "Not specified")
    df["TotalStars"] = df["TotalStars"].astype(int)
    df["StarsGainedRecently"] = df["StarsGainedRecently"].astype(int)
    df = df.drop_duplicates(subset=["RepoName"])
    return df.reset_index(drop=True)


def analyze(df):
    """Print exploratory analysis of the scraped data."""
    print("\n--- EXPLORATORY ANALYSIS ---")
    print(f"Total repos scraped: {len(df)}")

    print("\nLanguage distribution:")
    print(df["Language"].value_counts())

    print("\nTop 5 repos by total stars:")
    print(df.sort_values("TotalStars", ascending=False)[["RepoName", "TotalStars", "Language"]].head())

    print("\nTop 5 repos by stars gained today/this week:")
    print(df.sort_values("StarsGainedRecently", ascending=False)[["RepoName", "StarsGainedRecently"]].head())

    print("\nAverage total stars by language (top languages only):")
    top_langs = df["Language"].value_counts().head(5).index
    print(df[df["Language"].isin(top_langs)].groupby("Language")["TotalStars"].mean().sort_values(ascending=False))


if __name__ == "__main__":
    print(f"Fetching {URL} ...")
    html = fetch_page(URL)

    print("Extracting structured data...")
    records = extract_repos(html)
    df = pd.DataFrame(records)
    print(f"Extracted {len(df)} repositories.")

    print("Cleaning dataset...")
    df = clean_dataset(df)

    analyze(df)

    # Bonus: export to CSV and Excel
    df.to_csv("github_trending_repos.csv", index=False)
    df.to_excel("github_trending_repos.xlsx", index=False)
    print("\nSaved github_trending_repos.csv and github_trending_repos.xlsx")
