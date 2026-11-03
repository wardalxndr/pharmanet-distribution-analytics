"""Profile every CSV in data/: shape, dtypes, null counts, and whether
sales == quantity * price (best effort, column names matched case-insensitively).

Run from the project root:
    .venv\\Scripts\\python scripts\\profile_data.py
"""

import glob

import pandas as pd

TOLERANCE = 0.01


def profile(path: str) -> None:
    df = pd.read_csv(path)
    print("=" * 70)
    print(path, "shape:", df.shape)
    print("\n-- columns and dtypes --")
    print(df.dtypes)
    print("\n-- nulls per column --")
    print(df.isna().sum())

    cols = {c.lower().strip(): c for c in df.columns}
    if {"quantity", "price", "sales"} <= set(cols):
        q, p, s = cols["quantity"], cols["price"], cols["sales"]
        qty = pd.to_numeric(df[q], errors="coerce")
        price = pd.to_numeric(df[p], errors="coerce")
        sales = pd.to_numeric(df[s], errors="coerce")
        mismatch = ((qty * price) - sales).abs() > TOLERANCE
        print("\n-- price consistency --")
        print(f"rows where sales != quantity * price: {int(mismatch.sum())} / {len(df)}")
        if mismatch.any():
            print(df.loc[mismatch, [q, p, s]].head(10))

    dupes = df.duplicated().sum()
    print(f"\n-- exact duplicate rows: {dupes} --")


def main() -> None:
    csvs = sorted(glob.glob("data/*.csv"))
    if not csvs:
        print("no CSV found in data/. Run scripts/download_data.py first.")
        return
    for path in csvs:
        profile(path)


if __name__ == "__main__":
    main()
