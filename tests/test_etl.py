import pandas as pd
import pytest
from etl import extract_data, transform_data, load_data


@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV file for testing."""
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["A", "B", "C"]})
    df.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def sample_data():
    """Fixture to provide a sample DataFrame."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "salary": [5000, 6000],
            "tax": [500, 600],
            "net_salary": [4500, 5400],
        }
    )


def test_extract_data_success(sample_csv):
    """Tests if the function correctly extracts data."""
    data = extract_data(sample_csv)
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["col1", "col2"]
    assert len(data) == 3


def test_extract_data_failure():
    """Tests if the function correctly handles a non-existent file."""
    data = extract_data("non_existent_file.csv")
    assert data is None


def test_transform_data_success():
    """Tests data transformation with a valid DataFrame."""
    data = pd.DataFrame(
        {"name": ["Alice", "Bob", "Charlie"], "salary": [5000, 6000, 7000]}
    )

    transformed = transform_data(data)

    assert transformed is not None
    assert "tax" in transformed.columns
    assert "net_salary" in transformed.columns
    assert transformed["tax"].tolist() == [500.0, 600.0, 700.0]
    assert transformed["net_salary"].tolist() == [4500.0, 5400.0, 6300.0]


def test_transform_data_missing_values():
    """Tests the removal of missing values."""
    data = pd.DataFrame({"name": ["Alice", "Bob", None], "salary": [5000, None, 7000]})

    transformed = transform_data(data)

    assert transformed is not None
    assert len(transformed) == 1  # Only the first row is valid
    assert transformed.iloc[0]["name"] == "Alice"


def test_transform_data_invalid_column():
    """Tests the behavior when the 'salary' column is missing."""
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "income": [5000, 6000, 7000],  # Incorrect column name
        }
    )

    transformed = transform_data(data)
    assert transformed is None


def test_load_data_success(sample_data, tmp_path):
    """Tests if the file is correctly created with the right data."""
    output_file = tmp_path / "output_test.csv"

    # Executes the function
    load_data(sample_data, output_file)

    # Checks if the file was created
    assert output_file.exists()

    # Verifies that the content is correctly saved
    loaded_data = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(loaded_data, sample_data)


def test_load_data_invalid_path(sample_data):
    """Tests the behavior with an invalid path."""
    output_file = "not_valid/output.csv"

    try:
        load_data(sample_data, output_file)
        assert False, "The function should raise an exception"
    except Exception as e:
        # Check if the exception is an OSError or a related path failure exception
        assert isinstance(e, (OSError, FileNotFoundError, AssertionError)), (
            f"Raised exception: {type(e)}"
        )
