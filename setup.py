from setuptools import setup, find_packages


# Function to read the long description from README.md
def get_long_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


setup(
    name="openrouter-model-filter",
    version="1.0.0",
    author="thiswillbeyourgithub",
    description="A CLI tool to fetch, filter, and sort models from the OpenRouter API.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/thiswillbeyourgithub/OpenrouterModelFilter",
    packages=find_packages(),
    install_requires=[
        "requests",
        "click",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "openrouter_model_filter=openrouter_model_filter.filter:cli",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=["openrouter", "free", "LLM", "simonw", "models", "AI"],
)
