import os

from setuptools import setup, find_packages

from fakeyou import __version__, __author__

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="fakeyou",
    version=__version__,
    author=__author__,
    description="Enhanced FAKEYOU.COM API Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shards-7/fypy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp"
    ],
    keywords=[
        "fakeyou",
        "fakeyou.py",
        "fakeyou api",
        "rappers voice",
        "sing AI",
        "text to speech",
        "text to singing",
        "text to song",
        "lyrics to song",
        "tts"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.4",
)
