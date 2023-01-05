from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

<<<<<<< HEAD
VERSION = '2.0.0'
=======
VERSION = '1.1.1'
>>>>>>> 7a04fa1269750b2bf0b83ad7937c0f75e26a3ee4
DESCRIPTION = 'Enhanced FAKEYOU.COM API lib'
LONG_DESCRIPTION = 'None'

# Setting up
setup(
    name="fakeyou",
    version=VERSION,
    author="Shards-7",
    author_email="notmyemail@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests','aiohttp'],
    keywords=['fakeyou','fakeyou.py','fakeyou api','rappers voice','sing AI','text to speech','text to singing','text to song','lyrics to song','tts'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
