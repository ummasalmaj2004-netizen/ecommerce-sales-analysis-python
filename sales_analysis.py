from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load e-commerce sales data from a CSV file.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print("Dataset loaded successfully.")
    print(f"Rows: {len(df)}")

    return df


# ---------------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the sales dataset.
    """

    required_columns = {
        "product",
        "category",
        "quantity",
        "price"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Work on a copy
    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Clean text columns
    df["product"] = df["product"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    # Convert numerical columns
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Remove invalid numerical records
    df = df.dropna(
        subset=["quantity", "price"]
    )

    # Remove impossible values
    df = df[
        (df["quantity"] > 0)
        & (df["price"] >= 0)
    ]

    # Calculate revenue
    df["revenue"] = (
        df["quantity"] * df["price"]
    )

    return df


# ---------------------------------------------------------
# BUSINESS METRICS
# ---------------------------------------------------------

def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate important business KPIs.
    """

    total_revenue = df["revenue"].sum()

    total_units = df["quantity"].sum()

    average_revenue = df["revenue"].mean()

    best_selling_row = df.loc[
        df["quantity"].idxmax()
    ]

    highest_revenue_row = df.loc[
        df["revenue"].idxmax()
    ]

    metrics = {
        "total_revenue": total_revenue,
        "total_units": total_units,
        "average_revenue": average_revenue,
        "best_selling_product":
            best_selling_row["product"],
        "best_selling_units":
            best_selling_row["quantity"],
        "highest_revenue_product":
            highest_revenue_row["product"],
        "highest_product_revenue":
            highest_revenue_row["revenue"],
    }

    return metrics


# ---------------------------------------------------------
# PRODUCT ANALYSIS
# ---------------------------------------------------------

def analyze_products(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregate sales performance by product.
    """

    product_summary = (
        df.groupby("product", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            average_price=("price", "mean"),
        )
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    return product_summary


# ---------------------------------------------------------
# CATEGORY ANALYSIS
# ---------------------------------------------------------

def analyze_categories(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregate performance by product category.
    """

    category_summary = (
        df.groupby("category", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    return category_summary


# ---------------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------------

def create_revenue_chart(
    product_summary: pd.DataFrame
) -> None:
    """
    Create revenue by product chart.
    """

    plt.figure(figsize=(10, 6))

    plt.bar(
        product_summary["product"],
        product_summary["total_revenue"]
    )

    plt.title(
        "Revenue by Product"
    )

    plt.xlabel("Product")
    plt.ylabel("Revenue")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "revenue_by_product.png",
        dpi=300
    )

    plt.close()


def create_quantity_chart(
    product_summary: pd.DataFrame
) -> None:
    """
    Create quantity sold by product chart.
    """

    quantity_data = product_summary.sort_values(
        "total_quantity",
        ascending=False
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        quantity_data["product"],
        quantity_data["total_quantity"]
    )

    plt.title(
        "Units Sold by Product"
    )

    plt.xlabel("Product")
    plt.ylabel("Units Sold")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "units_sold_by_product.png",
        dpi=300
    )

    plt.close()


def create_category_chart(
    category_summary: pd.DataFrame
) -> None:
    """
    Create revenue by category chart.
    """

    plt.figure(figsize=(8, 6))

    plt.bar(
        category_summary["category"],
        category_summary["total_revenue"]
    )

    plt.title(
        "Revenue by Category"
    )

    plt.xlabel("Category")
    plt.ylabel("Revenue")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "revenue_by_category.png",
        dpi=300
    )

    plt.close()


# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------

def save_results(
    df: pd.DataFrame,
    product_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
    metrics: dict,
) -> None:
    """
    Save processed datasets and business results.
    """

    df.to_csv(
        OUTPUT_DIR / "cleaned_sales_data.csv",
        index=False
    )

    product_summary.to_csv(
        OUTPUT_DIR / "product_summary.csv",
        index=False
    )

    category_summary.to_csv(
        OUTPUT_DIR / "category_summary.csv",
        index=False
    )

    report_file = (
        OUTPUT_DIR / "business_summary.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "E-COMMERCE SALES ANALYSIS\n"
        )

        file.write(
            "=" * 40 + "\n\n"
        )

        file.write(
            f"Total Revenue: "
            f"{metrics['total_revenue']:,.2f}\n"
        )

        file.write(
            f"Total Units Sold: "
            f"{metrics['total_units']:,.0f}\n"
        )

        file.write(
            f"Average Revenue Per Product: "
            f"{metrics['average_revenue']:,.2f}\n"
        )

        file.write(
            f"Best Selling Product: "
            f"{metrics['best_selling_product']}\n"
        )

        file.write(
            f"Best Selling Units: "
            f"{metrics['best_selling_units']:,.0f}\n"
        )

        file.write(
            f"Highest Revenue Product: "
            f"{metrics['highest_revenue_product']}\n"
        )

        file.write(
            f"Highest Product Revenue: "
            f"{metrics['highest_product_revenue']:,.2f}\n"
        )


# ---------------------------------------------------------
# DISPLAY REPORT
# ---------------------------------------------------------

def display_report(metrics: dict) -> None:
    """
    Display the final business report.
    """

    print("\n")
    print("=" * 55)
    print("       E-COMMERCE SALES ANALYSIS REPORT")
    print("=" * 55)

    print(
        f"Total Revenue: "
        f"{metrics['total_revenue']:,.2f}"
    )

    print(
        f"Total Units Sold: "
        f"{metrics['total_units']:,.0f}"
    )

    print(
        f"Average Revenue: "
        f"{metrics['average_revenue']:,.2f}"
    )

    print(
        f"Best Selling Product: "
        f"{metrics['best_selling_product']}"
    )

    print(
        f"Units Sold: "
        f"{metrics['best_selling_units']:,.0f}"
    )

    print(
        f"Highest Revenue Product: "
        f"{metrics['highest_revenue_product']}"
    )

    print(
        f"Highest Product Revenue: "
        f"{metrics['highest_product_revenue']:,.2f}"
    )

    print("=" * 55)


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

def main() -> None:
    """
    Run the complete sales analysis pipeline.
    """

    print(
        "Starting E-Commerce Sales Analysis..."
    )

    # Load
    sales_df = load_data(DATA_FILE)

    # Clean
    sales_df = clean_data(sales_df)

    # Analyze
    metrics = calculate_metrics(sales_df)

    product_summary = analyze_products(
        sales_df
    )

    category_summary = analyze_categories(
        sales_df
    )

    # Create visualizations
    create_revenue_chart(
        product_summary
    )

    create_quantity_chart(
        product_summary
    )

    create_category_chart(
        category_summary
    )

    # Save everything
    save_results(
        sales_df,
        product_summary,
        category_summary,
        metrics,
    )

    # Show final report
    display_report(metrics)

    print(
        "\nAnalysis completed successfully."
    )

    print(
        f"Results saved inside: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
