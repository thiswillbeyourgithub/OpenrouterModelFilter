import os
from setuptools import setup, find_packages

# Function to read the long description from README.md
def get_long_description():
    # TODO: Create a README.md file for your package
    # For now, provides a default if README.md is missing
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    return "A CLI tool to fetch, filter, and sort models from the OpenRouter API."

setup(
    name="openrouter-model-filter",
    version="0.1.0",  # TODO: Increment version for new releases
    author="TODO: Your Name", # TODO: Replace with your name
    author_email="TODO: your.email@example.com", # TODO: Replace with your email
    description="A CLI tool to fetch, filter, and sort models from the OpenRouter API.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="TODO: https://github.com/yourusername/openrouter-model-filter", # TODO: Replace with your project's URL
    packages=find_packages(),
    install_requires=[
        "requests",
        "click",
        # Add 'typing_extensions' here if supporting Python < 3.8 and using Literal
    ],
    python_requires=">=3.8", # Uses typing.Literal; for 3.7, add typing_extensions
    entry_points={
        "console_scripts": [
            "openrouter_model_filter=openrouter_model_filter.filter:cli",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", # TODO: Choose your license and update
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    # TODO: Consider adding keywords e.g. keywords="openrouter api llm models filter cli",
)
