import pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CSV_FILE=ROOT/"results"/"results.csv"; df=pd.read_csv(CSV_FILE)
for col in ["first_token_ms","total_ms","tokens_in","tokens_out","retries"]: df[col]=pd.to_numeric(df[col],errors="coerce")
print("\n========== RESULTS BY SCENARIO ==========\n")
for (source,scenario),group in df.groupby(["source","scenario"],dropna=False):
    successful=group[group["status"]=="ok"]
    print("\nSource:",source); print("Scenario:",scenario); print("Requests:",len(group)); print("Successful:",len(successful)); print("Rate limited:",(group["status"]=="rate_limited").sum()); print("Timeouts:",(group["status"]=="timeout").sum()); print("Errors:",(group["status"]=="error").sum()); print("Retries:",group["retries"].fillna(0).sum())
    for column in ["first_token_ms","total_ms"]:
        values=successful[column].dropna()
        if len(values): print(f"{column}: p50={values.quantile(0.50):.2f} ms, p95={values.quantile(0.95):.2f} ms, p99={values.quantile(0.99):.2f} ms")
        else: print(column,": No successful measurements")
print("\n========== TOKEN COUNTS =========="); print(df.groupby("source")[["tokens_in","tokens_out"]].sum()); print("\n========== ANSWER GRADES =========="); print(df["answer_grade"].value_counts(dropna=False))
