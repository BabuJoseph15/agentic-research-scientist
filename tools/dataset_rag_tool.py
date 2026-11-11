"""Extract, clean, embed, and retrieve dengue CSV observations with Chroma."""

from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "dengue.csv"
CLEAN_FILE = ROOT / "data" / "processed" / "dengue_clean.csv"
VECTOR_DIR = ROOT / "data" / "chroma_dengue"

COLUMNS = ["temperature", "humidity", "rainfall", "total_cases"]
COLLECTION = "dengue_dataset"
DATASET_ID = "dengue"


def extract_and_clean_dataset(source: Path = RAW_FILE) -> pd.DataFrame:
    """Load the CSV, validate its required columns, and remove invalid rows."""
    df = pd.read_csv(source)

    missing_columns = set(COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"{source} is missing required columns: {sorted(missing_columns)}"
        )

    df = df[COLUMNS].copy()

    for column in COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=COLUMNS)

    valid_rows = (
        df["humidity"].between(0, 100)
        & df["rainfall"].ge(0)
        & df["total_cases"].ge(0)
    )
    df = df.loc[valid_rows]
    df = df.drop_duplicates(subset=COLUMNS).reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid dataset rows remain after cleaning.")

    return df


def rows_to_documents(df: pd.DataFrame) -> list[Document]:
    """Convert each cleaned CSV row into a document with searchable text and metadata."""
    documents = []

    for row_id, row in enumerate(df.to_dict(orient="records"), start=1):
        content = (
            f"Dengue dataset observation {row_id}: "
            f"temperature={row['temperature']}, "
            f"humidity={row['humidity']}, "
            f"rainfall={row['rainfall']}, "
            f"total_cases={row['total_cases']}."
        )

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "dataset_id": DATASET_ID,
                    "source": RAW_FILE.name,
                    "row_id": row_id,
                    "temperature": float(row["temperature"]),
                    "humidity": float(row["humidity"]),
                    "rainfall": float(row["rainfall"]),
                    "total_cases": float(row["total_cases"]),
                },
            )
        )

    return documents


def _get_vector_store() -> Chroma:
    """Create the persistent Chroma store and configure its embedding model."""
    load_dotenv()

    return Chroma(
        collection_name=COLLECTION,
        embedding_function=OpenAIEmbeddings(
            model="text-embedding-3-small",
        ),
        persist_directory=str(VECTOR_DIR),
    )


def build_dataset_index() -> int:
    """Clean the source CSV, save the cleaned data, and rebuild its vector index."""
    df = extract_and_clean_dataset()

    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_FILE, index=False)

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vector_store = _get_vector_store()

    existing_ids = vector_store.get(
        where={"dataset_id": DATASET_ID}
    )["ids"]
    if existing_ids:
        vector_store.delete(ids=existing_ids)

    documents = rows_to_documents(df)
    document_ids = [
        f"dengue-row-{index}"
        for index in range(1, len(documents) + 1)
    ]
    vector_store.add_documents(documents=documents, ids=document_ids)

    return len(documents)


def retrieve_dataset_context(
    query: str,
    top_k: int = 3,
) -> list[tuple[Document, float]]:
    """Find the top matching dataset rows for a natural-language query."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not VECTOR_DIR.exists():
        raise FileNotFoundError(
            f"Dataset index not found at {VECTOR_DIR}. "
            "Build it first with: python -m tools.dataset_rag_tool"
        )

    vector_store = _get_vector_store()
    return vector_store.similarity_search_with_relevance_scores(
        query,
        k=top_k,
    )


if __name__ == "__main__":
    """Build the index when this module is run as a script."""
    indexed_rows = build_dataset_index()
    print(f"Indexed {indexed_rows} cleaned dengue dataset rows.")
    print(f"Cleaned CSV: {CLEAN_FILE}")
    print(f"Vector index: {VECTOR_DIR}")