__title__ = "fakeyou.py"
__author__ = "Shards-7"
__license__ = "GNU"
__copyright__ = "Copyright 2023 Shards"
__version__ = "1.2.2"

from .fakeyou import FakeYou
from .asynchronous_fakeyou import AsyncFakeYou
from requests import get
__newest__=get("https://pypi.python.org/pypi/fakeyou/json").json()["info"]["version"]

if __newest__ != __version__:
	print(f"New version of fakeyou.py is out : {__newest__} (Using {__version__})")
