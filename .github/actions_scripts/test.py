"""验证脚本能否正常运行."""
import os
from importlib.metadata import Distribution, metadata

pypi_name = os.environ["PYPI_NAME"]


print(Distribution.from_name(pypi_name).read_text("METADATA"))
print(metadata(pypi_name).get_all("Project-URL"))