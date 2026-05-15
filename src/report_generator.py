import pandas as pd


def create_quality_report(before_metrics, after_metrics, output_path=None):
    report_data = []

    for metric in before_metrics:
        before_value = before_metrics[metric]
        after_value = after_metrics[metric]

        if isinstance(before_value, (int, float)) and isinstance(after_value, (int, float)):
            change = after_value - before_value
        else:
            change = ""

        report_data.append({
            "metric": metric,
            "before": before_value,
            "after": after_value,
            "change": change
        })

    report_df = pd.DataFrame(report_data)

    if output_path is not None:
        report_df.to_csv(output_path, index=False)
        print("Data quality report saved to:", output_path)

    return report_df