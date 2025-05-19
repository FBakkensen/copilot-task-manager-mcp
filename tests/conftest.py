"""Common pytest fixtures and configurations."""
import os
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent


@pytest.fixture(scope="session")
def test_data_dir(project_root: Path) -> Path:
    """Return the test data directory."""
    data_dir = project_root / "tests" / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Set up environment variables for testing."""
    monkeypatch.setenv("TESTING", "1")


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file and return its path."""
    temp_file = tmp_path / "test_file.txt"
    temp_file.write_text("")
    return temp_file


def pytest_configure(config):
    """Configure custom markers."""
    for marker in [
        "unit",
        "integration",
        "e2e",
        "slow",
    ]:
        config.addinivalue_line(
            "markers",
            f"{marker}: Mark test as {marker} test"
        )
