import json
from pathlib import Path
from typing import Dict, Set

import aiofiles
from loguru import logger


async def adelete_dup(
    line_id_each_file: Dict[str, Set[int]],
    file_path: Path,
    save_dup_path: Path,
    save_data_path: Path,
) -> int:
    """
    Deletes duplicate entries from the given JSON files based on the provided indices of duplicate lines.
    The duplicate entries are saved to a new file specified by the save_dup_path.

    Parameters:
        line_id_each_file (Dict[str, Set[int]]): A dictionary where keys are file names and values are sets of line indices
                                    that are considered duplicates.
        save_dup_path (str): The path where the deduplicated data will be saved.

    Returns:
        int: The number of duplicate entries that were deleted.
    """

    line_id = line_id_each_file.get(file_path.name, [])
    dup_data = []
    old_data = []
    async with (
        aiofiles.open(file_path, "r", encoding="utf-8") as fr,
        aiofiles.open(save_dup_path, "w", encoding="utf-8") as fw,
        aiofiles.open(save_data_path, "w", encoding="utf-8") as fw_o,
    ):
        src_content = await fr.read()
        src_data = json.loads(src_content)
        if line_id:
            for idx, data in enumerate(src_data):
                if idx in line_id:
                    dup_data.append(data)
                else:
                    old_data.append(data)
            await fw.write(json.dumps(dup_data, indent=4, ensure_ascii=False))
            await fw_o.write(json.dumps(old_data, indent=4, ensure_ascii=False))
        else:
            await fw.write(json.dumps(dup_data, indent=4, ensure_ascii=False))
            await fw_o.write(json.dumps(src_data, indent=4, ensure_ascii=False))
    logger.info(
        f"{file_path}: Delete {len(dup_data)} duplicate data.The deduplication is completed and the results are saved in {save_dup_path}"
    )
    logger.info(f"The filtered data has been saved to {save_data_path}.")

    logger.info(
        f"本次共检测了 {len(src_data)} 条数据, 异常的数据有 {len(dup_data)} 条"
    )
    logger.info("异常检出率为：{:.2%}".format(len(dup_data)/len(src_data)))


    return len(dup_data)
