import os
from collections import Counter

import matplotlib.pyplot as plt


OUTPUT_DIR = "output/graphs"


def create_output_directory():
    """
    Creates output directory for graph images.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_function_lengths_histogram(results):
    """
    Creates histogram of function lengths.
    """

    function_lengths = []

    for result in results:

        analysis_result = result["analysis_result"]

        for function in analysis_result["functions"]:

            function_lengths.append(
                function["line_count"]
            )

    plt.figure(figsize=(8, 5))

    plt.hist(function_lengths)

    plt.title("Distribution of Function Lengths")
    plt.xlabel("Function Length (Lines)")
    plt.ylabel("Number of Functions")

    path = os.path.join(
        OUTPUT_DIR,
        "function_lengths_histogram.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def create_issues_by_type_pie_chart(results):
    """
    Creates pie chart of issue types.
    """

    issue_types = []

    for result in results:

        for alert in result["alerts"]:

            issue_types.append(alert["type"])

    counter = Counter(issue_types)

    plt.figure(figsize=(8, 8))

    plt.pie(
        counter.values(),
        labels=counter.keys(),
        autopct="%1.1f%%"
    )

    plt.title("Issues By Type")

    path = os.path.join(
        OUTPUT_DIR,
        "issues_by_type_pie.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def create_issues_per_file_bar_chart(results):
    """
    Creates bar chart of issues per file.
    """

    filenames = []
    issue_counts = []

    for result in results:

        filenames.append(
            result["filename"]
        )

        issue_counts.append(
            len(result["alerts"])
        )

    plt.figure(figsize=(10, 5))

    plt.bar(
        filenames,
        issue_counts
    )

    plt.title("Issues Per File")
    plt.xlabel("Filename")
    plt.ylabel("Number Of Issues")

    plt.xticks(rotation=45)

    path = os.path.join(
        OUTPUT_DIR,
        "issues_per_file_bar.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def generate_graphs(results):
    """
    Main graph generation function.

    Receives all results and creates:
    1. Histogram
    2. Pie Chart
    3. Bar Chart

    Returns paths of generated images.
    """

    create_output_directory()

    histogram_path = create_function_lengths_histogram(results)

    pie_chart_path = create_issues_by_type_pie_chart(results)

    bar_chart_path = create_issues_per_file_bar_chart(results)

    return {
        "histogram": histogram_path,
        "pie_chart": pie_chart_path,
        "bar_chart": bar_chart_path
    }