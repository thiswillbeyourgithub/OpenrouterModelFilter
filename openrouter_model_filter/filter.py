from typing import Literal, Optional, Union
import json
import re
import requests


def main(
    n: int = -1,
    return_all: bool = False,
    return_format: Literal["dict", "json", "str"] = "str",
    keep_regexes: str = ".*:free",
    remove_regexes: Optional[str] = r".*\bbase\b.*,.*\binstruct\b.*,.*\bmath\b",
    openrouter_endpoint: str = "https://openrouter.ai/api/v1/",
    model_url: str = "/models",
    sort_key: Optional[str] = "context_length",
    ) -> Union[str, dict]:

    # prepare args
    assert n == -1 or n > 0, "Invalid n argument"
    url = f"{openrouter_endpoint}/{model_url}"
    url = "https://" + re.sub("/+", "/", url.split("https://", 1)[1])

    # compile the regexes
    keep_regexes = [re.compile(r) for r in keep_regexes.split(",")]
    remove_regexes = [re.compile(r) for r in remove_regexes.split(",")] if remove_regexes else []

    # fetch model list
    response = requests.get(url)
    response.raise_for_status()
    rep_as_json = response.json()
    data_raw = rep_as_json["data"]

    # sort to have the large context models first
    if sort_key:
        data_raw = sorted(
            data_raw,
            key=lambda model: model[sort_key],
            reverse=True
        )

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
        data = data[:n]

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

