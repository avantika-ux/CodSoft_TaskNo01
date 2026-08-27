"""
Task 5 (continued): Visualizing trends in the scraped GitHub Trending data.
Run scrape_github_trending.py first to generate github_trending_repos.csv.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.autolayout"] = True

df = pd.read_csv("github_trending_repos.csv")

# Language distribution
plt.figure(figsize=(8, 5))
lang_counts = df["Language"].value_counts()
sns.barplot(x=lang_counts.index, y=lang_counts.values, hue=lang_counts.index,
            palette="crest", legend=False)
plt.title("Trending Repos by Language")
plt.xlabel("Language")
plt.ylabel("Number of Repos")
plt.xticks(rotation=30)
plt.savefig("chart1_language_distribution.png", dpi=150)
plt.close()

# Top repos by total stars
plt.figure(figsize=(9, 5))
top10 = df.sort_values("TotalStars", ascending=False).head(10)
sns.barplot(data=top10, x="TotalStars", y="RepoName", hue="RepoName", palette="mako", legend=False)
plt.title("Top 10 Trending Repos by Total Stars")
plt.xlabel("Total Stars")
plt.ylabel("")
plt.savefig("chart2_top_repos_by_stars.png", dpi=150)
plt.close()

# Total stars vs stars gained recently (scatter)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="TotalStars", y="StarsGainedRecently", hue="Language", s=100)
plt.title("Total Stars vs Recent Momentum")
plt.xlabel("Total Stars")
plt.ylabel("Stars Gained Today/This Week")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.savefig("chart3_stars_vs_momentum.png", dpi=150)
plt.close()

print("Saved 3 charts.")
