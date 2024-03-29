from setuptools import setup

setup(
    name="crawlergooglescholar",
    version="0.1",
    description="A crawler to download researchers' statistics from google scholar",
    long_description="This bot crawls and downloads statistics and pictures from google scholar's researchers. Single threaded as well as multithreading scripts are provided.",
    url="http://github.com/vignif/crawler-google-scholar",
    author="Francesco Vigni",
    author_email="vignif@gmail.com",
    license="MIT",
    keywords="crawler researchers professors google scholar statistics",
    packages=["crawlergooglescholar"],
    install_requires=["bs4", "pandas", "aiohttp", "asyncio", "openpyxl"],
    zip_safe=False,
)
