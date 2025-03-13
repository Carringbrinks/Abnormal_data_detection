import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Union

import aiofiles
from datasketch import MinHash
from loguru import logger
from nltk import ngrams

from config import (
    BANDS,
    CONTENT_FIELD_NAME,
    DOC_ID_FIELD_NAME,
    HASH_FILE_NAME,
    WIDTH,
    r,
)


def _H(hs: Union[bytearray, memoryview]) -> bytes:
    """
    Transforms an array (bytearray or memoryview) to a byte representation for hashing.

    Parameters:
        hs (Union[bytearray, memoryview]): The input array (either bytearray or memoryview) to be transformed.

    Returns:
        bytes: The byte representation of the input array.
    """
    return bytes(hs.byteswap().data)


def generate_hash_values(text: str):
    """
    Generate hash values for a given text using MinHash.
    """
    features = map(lambda x: "".join(x), ngrams(text, WIDTH))
    m = MinHash(num_perm=128)
    [m.update(x.encode("utf8")) for x in features]
    ret = []
    for idx in range(BANDS):
        ret.append(_H(m.hashvalues[idx * r : (idx + 1) * r]))
    return ret


async def agenerate_line_bind_hash(file_path: Path) -> List[List[Dict[str, Any]]]:
    """
    Function to compute hash values for each line in a file and group them into bands.

    Parameters:
        file_path: The path to the input JSON file.

    Returns:
        A nested list where:
        - Each inner list corresponds to a specific band.
        - Each dictionary in the inner list contains:
            - 'doc_id': A unique identifier for the document, combining the file name and line index.
            - 'hash': The hash value for that specific band.
    """
    file_name = file_path.name
    logger.info(f"process file {file_name}")
    band_hash_value_list = [[] for _ in range(BANDS)]
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        content = await f.read()
        data = json.loads(content)
        for idx, line in enumerate(data):
            try:
                json_doc = "\n".join(
                    [value for key, value in line.items() if key in CONTENT_FIELD_NAME]
                )
                doc_id = f"{file_name}@{idx}"
                hash_value_list = generate_hash_values(json_doc)
                for idx in range(BANDS):
                    save_doc = {}
                    save_doc[DOC_ID_FIELD_NAME] = doc_id
                    save_doc[HASH_FILE_NAME] = hash_value_list[idx]
                    band_hash_value_list[idx].append(save_doc)
            except Exception as e:
                logger.warning(f"procces file {file_name} line {idx} error happe: {e}")
                continue
        return band_hash_value_list


def generate_dep_pairs(
    band_hash_value_list: List[List[Dict[str, Any]]],
) -> list[list[str]]:
    """
    Function to identify and save pairs of lines with high similarity based on hash values.

    Parameters:
        band_hash_value_list: A nested list of hash values

    Returns:
        A list of lists, where each inner list contains pairs of document IDs with high similarity based
        on the hash values.
    """
    results: list[list[str]] = []
    for bucket_dir_name in band_hash_value_list:
        lsh_dict = defaultdict(str)
        result = []
        for doc in bucket_dir_name:
            try:
                key = doc[DOC_ID_FIELD_NAME]
                H = doc[HASH_FILE_NAME]
                cand = lsh_dict.get(H)
                if cand is not None:
                    result.append(f"{key} :: {cand}\n")
                else:
                    lsh_dict[H] = key
            except Exception:
                pass
            results.append(result)
    return results
