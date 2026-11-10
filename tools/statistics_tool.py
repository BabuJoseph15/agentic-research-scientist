from scipy.stats import pearsonr


def correlation_analysis(df):

    target = "total_cases"

    results = {}

    for col in df.columns:

        if col == target:
            continue

        if str(df[col].dtype) == "object":
            continue

        corr, _ = pearsonr(
            df[col],
            df[target]
        )

        results[col] = round(
            corr,
            4
        )

    return results