from graph.workflow import graph

initial_state = {
    "question":
    "Can climate change increase dengue outbreaks in India?",
    "papers": [],
    "evidence": []
}

result = graph.invoke(
    initial_state
)

print("\nResearch Papers Found:\n")

for paper in result["papers"]:

    print("=" * 100)

    print(
        f"Title: {paper['title']}"
    )

    print(
        f"Published: {paper['published']}"
    )

print("\nEvidence Extracted:\n")

for item in result["evidence"]:

    print(item)