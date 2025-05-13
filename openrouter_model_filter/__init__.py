# This file makes openrouter_model_filter a Python package.
# It re-exports the main function and the CLI command for convenience.

from .filter import openrouter_model_filter, cli

__all__ = ["openrouter_model_filter", "cli"]
