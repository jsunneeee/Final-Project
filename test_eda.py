"""
Jason Lee
CSE 163
Tests the crawler exploratory analysis using small, known datasets.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

import eda


TEST_FILE = 'data/test_crawlers.csv'


def make_test_data() -> pd.DataFrame:
    """Returns three known crawler records for use in tests."""
    return pd.DataFrame({
        'provider': ['A', 'A', 'B'],
        'token': ['one', 'two', 'three'],
        'category': ['search', 'training', 'search'],
        'automatic_crawler': [True, True, False],
        'robots_txt_behavior': ['honors', 'honors', 'unknown'],
        'primary_purpose': ['find', 'train', 'find'],
        'source_url': ['url-a', 'url-a', 'url-b'],
        'source_checked': ['2026-01-01'] * 3
    })


def test_load_data() -> None:
    """Tests valid records and rejection of repeated crawler tokens."""
    data = eda.load_data(TEST_FILE)
    assert len(data) == 3
    assert list(data['token']) == ['one', 'two', 'three']

    with TemporaryDirectory() as folder:
        repeated = make_test_data()
        repeated.loc[1, 'token'] = 'one'
        file_name = Path(folder) / 'duplicate.csv'
        repeated.to_csv(file_name, index=False)
        try:
            eda.load_data(str(file_name))
            assert False, 'Expected rejection of duplicate tokens'
        except ValueError:
            pass


def test_count_missing_rows() -> None:
    """Tests missing-value detection on complete and incomplete data."""
    complete = make_test_data()
    assert eda.count_missing_rows(complete) == 0

    incomplete = complete.copy()
    incomplete.loc[0, 'provider'] = None
    incomplete.loc[0, 'category'] = None
    incomplete.loc[2, 'source_url'] = None
    assert eda.count_missing_rows(incomplete) == 2
    assert incomplete.isnull().sum().sum() == 3


def test_count_categories() -> None:
    """Tests categorical counts and inclusion of missing categories."""
    data = make_test_data()
    counts = eda.count_categories(data, 'category')
    assert counts['search'] == 2
    assert counts['training'] == 1

    data.loc[1, 'category'] = None
    counts = eda.count_categories(data, 'category')
    assert counts['search'] == 2
    assert len(counts) == 2
    assert counts.sum() == 3


def test_plots() -> None:
    """Tests that both functions save nonempty image files."""
    data = make_test_data()
    with TemporaryDirectory() as folder:
        output = Path(folder)
        eda.plot_category_counts(data, output)
        eda.plot_provider_categories(data, output)
        assert (output / 'figure1.png').stat().st_size > 0
        assert (output / 'figure2.png').stat().st_size > 0


def main() -> None:
    """Runs every test."""
    test_load_data()
    test_count_missing_rows()
    test_count_categories()
    test_plots()
    print('All EDA tests passed.')


if __name__ == '__main__':
    main()
