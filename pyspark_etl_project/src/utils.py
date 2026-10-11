from pathlib import Path
import yaml


def project_root() -> Path:
    """Return the repository root (the parent of src/)."""
    return Path(__file__).resolve().parents[1]


def load_config():
    config_path = project_root() / "config" / "config.yaml"
    with config_path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def resolve_path(relative_path: str) -> str:
    return str((project_root() / relative_path).resolve())
