"""Utility functions for GitHub Actions."""
from __future__ import annotations

import os
from pathlib import Path


def set_action_outputs(output_pairs: dict[str, str]) -> None:
    """Sets the GitHub Action outputs, with backwards compatibility for self-hosted runners without a GITHUB_OUTPUT environment file. Keyword arguments: output_pairs - Dictionary of outputs with values."""
    if "GITHUB_OUTPUT" in os.environ:
        with Path(os.environ["GITHUB_OUTPUT"]).open(mode="a") as f:
            for key, value in output_pairs.items():
                f.write(f"{key}={value}\n")
    else:
        for key, value in output_pairs.items():
            print(f"::set-output name={key}::{value}")  # noqa: T201
