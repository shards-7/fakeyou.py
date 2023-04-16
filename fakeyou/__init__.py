__title__ = "fakeyou.py"
__author__ = "Shards-7"
__license__ = "GNU"
__copyright__ = "Copyright 2023 Shards"
__version__ = "1.2.5"

from requests import get

from .asynchronous_fakeyou import AsyncFakeYou
from .fakeyou import FakeYou

latest_version = get("https://pypi.python.org/pypi/fakeyou/json").json()["info"]["version"]

if latest_version != __version__:
    print(f"A new version of FakeYou is available: {latest_version} (You're using version {__version__})")
    print("Visit the FakeYou Discord Server at https://discord.gg/fakeyou for more information.")
