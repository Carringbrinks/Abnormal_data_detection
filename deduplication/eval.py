
import argparse
import asyncio
from pathlib import Path

from loguru import logger

from generate_connected_components import (
    generate_connected_components_mp,
)
from generate_dup_data import (
    adelete_dup,
)
from generate_minhash import (
    agenerate_line_bind_hash,
    generate_dep_pairs,
)

async def adup_workflow(file_path: Path, save_dup_path: Path, save_data_path: Path):
    band_hash_value_list = await agenerate_line_bind_hash(file_path)
    logger.info(f"{file_path} Hash calculation completed")

    generated_dup_pairs = generate_dep_pairs(band_hash_value_list)
    res = generate_connected_components_mp(generated_dup_pairs)
    logger.info(f"{file_path} Line repeated calculation is completed")

    await adelete_dup(res, file_path, save_dup_path, save_data_path)
    logger.info(f"{file_path} Remove duplicate data and save")

def main():
    parser = argparse.ArgumentParser(description="Run deduplication workflow.")
    parser.add_argument("--file_path", type=str, required=True, help="Path to the input data file")
    parser.add_argument("--save_dep_path", type=str, required=True, help="Path to save duplicate data")
    parser.add_argument("--save_data_path", type=str, required=True, help="Path to normal data")
    
    args = parser.parse_args()
    
    asyncio.run(adup_workflow(Path(args.file_path), Path(args.save_dep_path), Path(args.save_data_path)))


if __name__ == "__main__":
    main()

