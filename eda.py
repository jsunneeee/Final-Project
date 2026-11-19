"""
Jason Lee
CSE 163
Explores documented purposes and access controls of web crawler tokens.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_FILE = 'data/crawlers.csv'
FIGURE_DIRECTORY = 'figures'
REQUIRED_COLUMNS = [
    'provider', 'token', 'category', 'automatic_crawler',
    'robots_txt_behavior', 'primary_purpose', 'source_url',
    'source_checked'
]


def load_data(file_name: str) -> pd.DataFrame:
    """Reads a CSV with required fields and distinct crawler tokens."""
    data = pd.read_csv(file_name)
    if not set(REQUIRED_COLUMNS).issubset(data.columns):
        raise ValueError('Missing required crawler columns')
    if not data['token'].is_unique:
        raise ValueError('Crawler tokens must be unique')
    return data


def count_missing_rows(data: pd.DataFrame) -> int:
    """Returns the number of records containing at least one missing value."""
    return int(data.isnull().any(axis=1).sum())


def count_categories(data: pd.DataFrame, column: str) -> pd.Series:
    """Returns frequencies of all values, including missing values."""
    return data[column].value_counts(dropna=False)


def plot_category_counts(data: pd.DataFrame, output: Path) -> None:
    """Saves a labeled plot of the number of tokens by purpose."""
    sns.set_theme()
    chart = sns.catplot(data=data, x='category', kind='count',
                        color='steelblue', height=4.5, aspect=1.9)
    chart.set_axis_labels('Crawler purpose', 'Number of documented tokens')
    chart.fig.suptitle('Figure 1: Documented crawler tokens by purpose')
    chart.fig.subplots_adjust(top=0.88, bottom=0.33)
    plt.xticks(rotation=20, ha='right')
    chart.savefig(output / 'figure1.png', dpi=180)
    plt.close(chart.fig)


def plot_provider_categories(data: pd.DataFrame, output: Path) -> None:
    """Saves a grouped plot of category counts for each provider."""
    sns.set_theme()
    chart = sns.catplot(data=data, x='provider', hue='category',
                        kind='count', height=4.5, aspect=1.7)
    chart.set_axis_labels('Provider', 'Number of documented tokens')
    chart.fig.suptitle('Figure 2: Crawler purposes by provider')
    chart.fig.subplots_adjust(top=0.89, right=0.64)
    chart.ax.set_yticks([0, 1])
    chart.savefig(output / 'figure2.png', dpi=180)
    plt.close(chart.fig)


def main() -> None:
    """Loads the source, prints EDA summaries, and saves both figures."""
    data = load_data(DATA_FILE)
    output = Path(FIGURE_DIRECTORY)
    output.mkdir(exist_ok=True)

    print('Rows:', len(data))
    print('Columns:', len(data.columns))
    print('Rows with missing data:', count_missing_rows(data))
    print('Missing values by column:')
    print(data.isnull().sum())

    for column in REQUIRED_COLUMNS:
        print('\nCounts for', column)
        print(count_categories(data, column))

    plot_category_counts(data, output)
    plot_provider_categories(data, output)


if __name__ == '__main__':
    main()
