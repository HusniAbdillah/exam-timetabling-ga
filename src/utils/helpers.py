from pathlib import Path


def get_project_root() -> Path:
    """Return the absolute path to the project root directory.

    Returns:
        Path: The project root directory.
    """
    return Path(__file__).parents[2].resolve()
