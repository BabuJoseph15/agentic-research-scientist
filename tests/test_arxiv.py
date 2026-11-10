from tools.arxiv_tool import search_arxiv

results = search_arxiv(
    "climate change dengue"
)

print(f"Found {len(results)} papers")

for paper in results:
    print("-" * 50)
    print("Title:", paper["title"])
    print("Published:", paper["published"])