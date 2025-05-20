import os
import aiofiles


async def save_to_disk(file: bytes, path: str) -> bool:
    # check if the folders /mnt/upload exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # writing file in that folder
    async with aiofiles.open(path, "wb") as out_file:
        await out_file.write(file)

    return True
