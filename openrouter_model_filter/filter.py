from typing import Literal, Optional, Union
import json
import re
import requests
import click

__version__ = "1.0.0"


def openrouter_model_filter(
    n: int = -1,
    return_format: Literal["dict", "json", "str"] = "str",
    keep_regexes: str = ".*:free",
    remove_regexes: Optional[str] = r".*\bbase\b.*,.*\binstruct\b.*,.*\bmath\b",
    openrouter_endpoint: str = "https://openrouter.ai/api/v1/",
    model_url: str = "/models",
    sort_key: Optional[str] = "context_length",
) -> Union[str, dict]:
    """
    Fetches, filters, and sorts models from the OpenRouter API.

    Args:
        n: Number of models to return. If -1, returns all matching models.
        return_format: The format of the returned data ("dict", "json", "str").
        keep_regexes: Comma-separated regexes. Models matching ALL regexes are kept.
        remove_regexes: Comma-separated regexes. Models matching ANY regex are removed.
        openrouter_endpoint: The base URL for the OpenRouter API.
        model_url: The API endpoint for fetching models.
        sort_key: The key to sort models by (e.g., "context_length"). If None, no sorting.

    Returns:
        A string, dictionary, or JSON string containing the filtered model data,
        depending on the return_format.
    """
    # prepare args
    assert n == -1 or n > 0, "Invalid n argument"
    url = f"{openrouter_endpoint}/{model_url}"
    url = "https://" + re.sub("/+", "/", url.split("https://", 1)[1])

    # compile the regexes
    keep_regexes = [re.compile(r) for r in keep_regexes.split(",")]
    remove_regexes = (
        [re.compile(r) for r in remove_regexes.split(",")] if remove_regexes else []
    )

    # fetch model list
    response = requests.get(url)
    response.raise_for_status()
    rep_as_json = response.json()
    data_raw = rep_as_json["data"]

    # sort to have the large context models first
    if sort_key:
        data_raw = sorted(data_raw, key=lambda model: model[sort_key], reverse=True)

    # format into a usable dict
    data = {d.pop("id"): d for d in data_raw}

    # regex filtering
    remove = []
    for did, d in data.items():
        if not all(r.match(did) for r in keep_regexes):
            remove.append(did)
        elif any(r.match(did) for r in remove_regexes):
            remove.append(did)
    for rem in remove:
        del data[rem]
    assert data, "No openrouter models were kept after regex filtering!"

    # crop
    if n != -1:
        # Convert dictionary to list of items, slice, then convert back to dict
        data = dict(list(data.items())[:n])

    # return
    if return_format == "dict":
        return data
    elif return_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif return_format == "str":
        s = "\n".join(data.keys())
        return s
    else:
        raise ValueError(return_format)


@click.command()
@click.option(
    "--n",
    default=-1,
    type=int,
    show_default=True,
    help="Number of models to return. -1 for all.",
)
@click.option(
    "--return-format",
    default="str",
    type=click.Choice(["dict", "json", "str"]),
    show_default=True,
    help="Output format.",
)
@click.option(
    "--keep-regexes",
    default=".*:free",
    type=str,
    show_default=True,
    help="Comma-separated regexes. Models matching ALL regexes are kept.",
)
@click.option(
    "--remove-regexes",
    default=r".*\bbase\b.*,.*\binstruct\b.*,.*\bmath\b",
    type=str,
    show_default=True,
    help='Comma-separated regexes. Models matching ANY regex are removed. Pass "" for no removal regexes.',
)
@click.option(
    "--openrouter-endpoint",
    default="https://openrouter.ai/api/v1/",
    type=str,
    show_default=True,
    help="OpenRouter API base URL.",
)
@click.option(
    "--model-url",
    default="/models",
    type=str,
    show_default=True,
    help="API endpoint for fetching models.",
)
@click.option(
    "--sort-key",
    default="context_length",
    type=str,
    show_default=True,
    help='Key to sort models by. Pass "" for no sorting.',
)
def cli(
    n: int,
    return_format: str,
    keep_regexes: str,
    remove_regexes: str,
    openrouter_endpoint: str,
    model_url: str,
    sort_key: str,
):
    """
    Fetches, filters, and sorts models from the OpenRouter API.
    Outputs the result to standard output.
    """
    # Handle empty string for sort_key to mean None (no sorting)
    actual_sort_key = sort_key if sort_key else None

    # If remove_regexes is an empty string, openrouter_model_filter handles it correctly
    # (it results in an empty list of regexes) due to `if remove_regexes else []`.

    try:
        result = openrouter_model_filter(
            n=n,
            return_format=return_format,
            keep_regexes=keep_regexes,
            remove_regexes=remove_regexes,  # Pass as is
            openrouter_endpoint=openrouter_endpoint,
            model_url=model_url,
            sort_key=actual_sort_key,
        )

        if return_format == "dict":  # The function returns a dict
            # For CLI, print dicts as JSON
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:  # The function returns a string (for "json" or "str" formats)
            click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        # Consider exiting with a non-zero status code, e.g. raise click.ClickException(str(e))
