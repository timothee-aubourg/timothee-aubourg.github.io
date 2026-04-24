import sys
from scholarly import scholarly as sc
import yaml
from datetime import date

SCHOLAR_ID = "y9gR9AYAAAAJ"

def fetch_stats():
    try:
        author = sc.search_author_id(SCHOLAR_ID)
        author = sc.fill(author, sections=["basics", "indices", "publications"])

        stats = {
            "citations":    author.get("citedby", 0),
            "h_index":      author.get("hindex", 0),
            "publications": len(author.get("publications", [])),
            "patent":       1,
            "last_updated": str(date.today()),
        }
        return stats

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    stats = fetch_stats()
    with open("_data/scholar_stats.yml", "w") as f:
        yaml.dump(stats, f, default_flow_style=False, allow_unicode=True)
    print(f"Updated: {stats}")
