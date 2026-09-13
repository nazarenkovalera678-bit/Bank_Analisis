"""
Bank Customer Churn Analysis
Tests three business hypotheses about customer churn using chi-square
tests of independence (with Cramer's V effect size) and a Mann-Whitney U
test, then saves the supporting charts to ../visualizations/.

Dataset: Bank_CLEANED.csv - 10,000 bank customers, 14 features
(demographics, activity, products, balance, churn flag `Exited`).
The file is not included in this repository; place it next to this
script (or update DATA_PATH) to reproduce the results.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency, mannwhitneyu

DATA_PATH = Path(__file__).resolve().parent / "Bank_CLEANED.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "visualizations"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Some exports store thousands-separated numbers as strings
    for col in ["Balance", "EstimatedSalary"]:
        if df[col].dtype == object:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False),
                errors="coerce",
            )
    return df


def chi2_report(df: pd.DataFrame, cat: str) -> tuple[pd.DataFrame, float, float, float]:
    """Chi-square test of independence between `cat` and churn, with Cramer's V."""
    ct = pd.crosstab(df[cat], df.Exited)
    chi2, p, dof, _ = chi2_contingency(ct)
    v = np.sqrt(chi2 / (len(df) * (min(ct.shape) - 1)))
    return ct, chi2, p, v


def test_h1_products(df: pd.DataFrame) -> None:
    """H1: customers with a single product churn more often (weaker attachment)."""
    df["OneProduct"] = (df.NumOfProducts == 1).astype(int)

    _, chi2, p, v = chi2_report(df, "OneProduct")
    rate_by_products = df.groupby("NumOfProducts").Exited.mean() * 100

    print(
        f"\nH1: 1 продукт={df[df.OneProduct == 1].Exited.mean() * 100:.2f}% "
        f"vs 2+ продукти={df[df.OneProduct == 0].Exited.mean() * 100:.2f}% "
        f"| хі-квадрат={chi2:.1f}, p={p:.2e}, V={v:.3f}"
    )

    # Does a single product make customers leave sooner, not just more often?
    tenure_one_product = df[(df.OneProduct == 1) & (df.Exited == 1)].Tenure
    tenure_multi_product = df[(df.OneProduct == 0) & (df.Exited == 1)].Tenure
    mwu_p = mannwhitneyu(tenure_one_product, tenure_multi_product).pvalue
    print(f"Перевірка швидкості відтоку (Tenure серед тих, хто пішов): MWU p={mwu_p:.3f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    rate_by_products.plot(kind="bar", ax=axes[0], color="steelblue")
    axes[0].set_title("Відтік залежно від кількості продуктів, %")
    axes[0].set_ylabel("%")
    axes[0].set_xlabel("Кількість продуктів")

    sns.boxplot(data=df[df.Exited == 1], x="OneProduct", y="Tenure", ax=axes[1])
    axes[1].set_title("Tenure клієнтів, які пішли: 0 = 2+ продукти, 1 = 1 продукт")
    axes[1].set_xlabel("Один продукт")
    axes[1].set_ylabel("Tenure")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "h1_churn_by_products.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def test_h2_activity(df: pd.DataFrame) -> None:
    """H2: inactive customers (IsActiveMember = 0) are the main churn-risk group."""
    _, chi2, p, v = chi2_report(df, "IsActiveMember")

    print(
        f"\nH2: неактивні={df[df.IsActiveMember == 0].Exited.mean() * 100:.2f}% "
        f"vs активні={df[df.IsActiveMember == 1].Exited.mean() * 100:.2f}% "
        f"| хі-квадрат={chi2:.1f}, p={p:.2e}, V={v:.3f}"
    )

    fig, ax = plt.subplots()
    (df.groupby("IsActiveMember").Exited.mean() * 100).plot(
        kind="bar", ax=ax, color=["tomato", "seagreen"]
    )
    ax.set_title("Відтік: неактивні (0) vs активні (1), %")
    ax.set_ylabel("%")
    ax.set_xlabel("Статус активності")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Неактивні", "Активні"], rotation=0)

    fig.savefig(OUTPUT_DIR / "h2_churn_by_activity.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def test_h3_balance_card(df: pd.DataFrame) -> None:
    """H3: high-balance customers without a credit card churn more (fewer perks)."""
    high_balance = df[df.Balance >= 100_000]
    _, chi2, p, v = chi2_report(high_balance, "HasCrCard")

    print(
        f"\nH3 (Баланс >= 100 000, N={len(high_balance)}): "
        f"без картки={high_balance[high_balance.HasCrCard == 0].Exited.mean() * 100:.2f}% "
        f"vs з карткою={high_balance[high_balance.HasCrCard == 1].Exited.mean() * 100:.2f}% "
        f"| хі-квадрат={chi2:.2f}, p={p:.3f}, V={v:.3f}"
    )

    fig, ax = plt.subplots()
    (high_balance.groupby("HasCrCard").Exited.mean() * 100).plot(
        kind="bar", ax=ax, color="slateblue"
    )
    ax.set_title("Високий баланс: відтік залежно від наявності кредитної картки, %")
    ax.set_ylabel("%")
    ax.set_xlabel("Наявність кредитної картки")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Без кредитної картки", "Є кредитна картка"], rotation=0)
    ax.set_ylim(0, 35)

    fig.savefig(OUTPUT_DIR / "h3_churn_by_balance_card.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = load_data()
    print(f"N={len(df)}, загальний рівень відтоку={df.Exited.mean() * 100:.2f}%")

    OUTPUT_DIR.mkdir(exist_ok=True)
    test_h1_products(df)
    test_h2_activity(df)
    test_h3_balance_card(df)


if __name__ == "__main__":
    main()
