# Task 5: Web Data Extraction & Analysis

Internship task — scraping structured data from a live public website with BeautifulSoup,
cleaning it, and analyzing trends.

## Objective
- Collect data from a publicly available website using Python libraries such as BeautifulSoup or Scrapy.
- Extract structured information including product details, prices, ratings, or news articles.
- Clean and organize the collected data into a structured dataset.
- Perform exploratory analysis to identify trends and patterns.
- Bonus: Automate the scraping process and export results to CSV or Excel.

## Source
[github.com/trending](https://github.com/trending) — GitHub's public Trending Repositories
page, scraped live at runtime.

## Approach
1. **Fetch** — requested the page with `requests`, using a descriptive User-Agent and a short
   delay after the request (`time.sleep`) to be a polite, low-impact scraper.
2. **Extract** — parsed the HTML with `BeautifulSoup` to pull, for each trending repo:
   repository name, description, primary language, total stars, and stars gained
   today/this week.
3. **Clean** — dropped incomplete rows, filled blank descriptions/languages with clear
   placeholders, corrected numeric types (star counts parsed from formatted strings like
   `"12,345"`), and removed duplicates.
4. **Analyze** — computed language distribution, top repos by total stars, top repos by
   recent momentum, and average stars by language.
5. **Visualize** — 3 charts covering language distribution, top repos by stars, and a
   scatter plot of total stars vs. recent momentum.
6. **Bonus: automation + export** — the whole pipeline runs as a single script
   (`scrape_github_trending.py`) with no manual steps, and exports results to both
   `.csv` and `.xlsx`.

## A note on scraping responsibly
This script makes a single request to one public page, uses a descriptive User-Agent, and
adds a short delay — it does not hit the site repeatedly, bypass logins, or scrape private
data. Always check a site's `robots.txt` and Terms of Service before scraping, and prefer a
site's official API when one is available (GitHub has a REST API — this exercise
intentionally uses HTML scraping instead, to practice the technique itself).

## Files
| File | Description |
|---|---|
| `scrape_github_trending.py` | Main script — fetches, extracts, cleans, analyzes, and exports the data |
| `visualize_trends.py` | Generates the 3 trend charts from the scraped CSV |
| `github_trending_repos.csv` | Cleaned, structured dataset (CSV) |
| `github_trending_repos.xlsx` | Same dataset exported to Excel |
| `chart1_language_distribution.png` | Number of trending repos per language |
| `chart2_top_repos_by_stars.png` | Top 10 repos by total stars |
| `chart3_stars_vs_momentum.png` | Total stars vs. recent star growth, by language |

## Tools used
Python, Requests, BeautifulSoup, Pandas, Matplotlib, Seaborn, openpyxl

## Note on reproducing results
GitHub Trending changes constantly, so re-running the script will produce different repos
and numbers than shown in the saved output files — that's expected and is itself a good
demonstration that the scraper works on live, changing data rather than a static snapshot.
