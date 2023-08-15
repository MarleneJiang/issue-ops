"""This module contains the main script for the GitHub actions."""

from importlib.metadata import Distribution, metadata

pypi_name = "alicebot"


print(Distribution.from_name(pypi_name).read_text("METADATA"))
print(metadata(pypi_name).get_all("Project-URL"))
