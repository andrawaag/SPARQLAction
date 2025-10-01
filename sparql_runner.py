import argparse
import os
import pandas as pd
from wikidataintegrator import wdi_core
from datetime import datetime

def run_sparql(query, endpoint):
    results = wdi_core.WDItemEngine.execute_sparql_query(
        query,
        endpoint=endpoint,
        as_dataframe=True
    )
    return results

def generate_report(query, endpoint, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    df = run_sparql(query, endpoint)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = os.path.join(output_folder, f"sparql_report_{timestamp}.md")
    csv_file = os.path.join(output_folder, f"sparql_report_{timestamp}.csv")

    # Save CSV
    df.to_csv(csv_file, index=False)

    # Save Markdown preview (limit rows to avoid huge comments)
    md_lines = []
    md_lines.append(f"# SPARQL Report\n")
    md_lines.append(f"- **Endpoint**: {endpoint}")
    md_lines.append(f"- **Rows returned**: {len(df)}\n")
    md_lines.append("## Query")
    md_lines.append("```sparql")
    md_lines.append(query)
    md_lines.append("```\n")

    md_lines.append("## Results Preview\n")
    if not df.empty:
        md_lines.append(df.head(20).to_markdown(index=False))
        if len(df) > 20:
            md_lines.append(f"\n_...truncated, full results in artifact/CSV file_")
    else:
        md_lines.append("_No results returned._")

    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    return md_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a SPARQL query and save report")
    parser.add_argument("--query", type=str, required=True, help="SPARQL query string")
    parser.add_argument("--endpoint", type=str, required=True, help="SPARQL endpoint URL")
    parser.add_argument("--output-folder", type=str, default="reports", help="Output folder for results")
    args = parser.parse_args()

    report_path = generate_report(args.query, args.endpoint, args.output_folder)
    print(f"REPORT_PATH={report_path}")