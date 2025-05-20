"""Common pytest fixtures and configurations."""

from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture  # type: ignore[misc]
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent


@pytest.fixture  # type: ignore[misc]
def test_data_dir(project_root: Path) -> Path:
    """Return the test data directory."""
    data_dir = project_root / 'tests' / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(autouse=True)  # type: ignore[misc]
def env_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up environment variables for testing."""
    monkeypatch.setenv('TESTING', '1')


@pytest.fixture  # type: ignore[misc]
def temp_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary file and return its path."""
    temp_file = tmp_path / 'test_file.txt'
    temp_file.write_text('')
    yield temp_file


def pytest_configure(config: pytest.Config) -> None:
    """Configure custom markers."""
    markers = ['unit', 'integration', 'e2e', 'slow']
    for marker in markers:
        config.addinivalue_line(
            'markers',
            f'{marker}: Mark test as {marker} test',
        )
