from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="news-scraper",
    version="0.1.0",
    author="Jerry Agenyi",
    author_email="your.email@example.com",
    description="A flexible news scraper that extracts articles from any website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerryagenyi/scraper-2",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "news-scraper=scraper.main:main",
        ],
    },
)
