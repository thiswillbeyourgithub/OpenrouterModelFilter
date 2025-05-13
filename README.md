# OpenRouter Model Filter

[![PyPI version](https://badge.fury.io/py/openrouter-model-filter.svg)](https://badge.fury.io/py/openrouter-model-filter)

`openrouter_model_filter` is a command-line tool designed to fetch, filter, and sort models from the OpenRouter API.

The primary idea behind this tool was to make it easy to identify and use the best currently available free models on OpenRouter. However, its filtering capabilities are flexible and can be adapted for various other criteria and use cases beyond just free models.

## Installation

```bash
pip install openrouter-model-filter
```

## Usage

No API keys are required to use this tool as it only fetches publicly available model information.

By default, `openrouter_model_filter` fetches models, keeps those tagged as `:free`, removes common `base`, `instruct`, or `math` specific models (which are often less suitable for general chat), sorts them by context length (descending), and returns a newline-separated list of model IDs. This sorting order generally places models with larger context windows, often the most recent or "frontier-like" ones, at the top of the list.

You can customize the behavior using various command-line options:

```bash
openrouter_model_filter --help
```

### Example with `llm` by Simon Willison

This tool was initially created to be integrated with Simon Willison's [llm](https://github.com/simonw/llm/) tool. The following command demonstrates how to use `openrouter_model_filter` to select one of the top 5 free models at random and then use it with `llm`:

```bash
llm --model "openrouter/$(openrouter_model_filter --n 5 | shuf | head -n 1)" "Hi, please tell me which model you are and what company made you."
```

**Note:** When using models via OpenRouter, you often need to explicitly agree to their terms, which may include allowing your prompts to be used for training by the model providers. Please check the OpenRouter documentation and model-specific terms.

## Filtering Options

- `--n`: Number of models to return (-1 for all).
- `--return-format`: Output format (`dict`, `json`, `str`). Default is `str`.
- `--keep-regexes`: Comma-separated regexes. Models matching ALL regexes are kept. Default is `.*:free`.
- `--remove-regexes`: Comma-separated regexes. Models matching ANY regex are removed. Default is `.*\bbase\b.*,.*\binstruct\b.*,.*\bmath\b`. Pass `""` for no removal.
- `--sort-key`: Key to sort models by (e.g., `context_length`, `name`). Default is `context_length`. Pass `""` for no sorting.

For example, to get the top 3 free models sorted by name:
```bash
openrouter_model_filter --n 3 --sort-key name
```

To get all models that are *not* free, in JSON format, without sorting:
```bash
openrouter_model_filter --keep-regexes ".*" --remove-regexes ".*:free" --return-format json --sort-key ""
```

## Development

This project uses `click` for the CLI and `requests` for API interaction.

Further development and contributions are welcome!

---
_This project was developed with assistance from [aider.chat](https://github.com/Aider-AI/aider/)._
