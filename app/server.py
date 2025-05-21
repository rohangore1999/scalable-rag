from fastapi import FastAPI, UploadFile
from uuid import uuid4
from .utils.file import save_to_disk
from .db.collections.files import files_collection, FileSchema
from .queue.queue import q
from .queue.workers import process_file

app = FastAPI()


@app.get('/')
def hello():
    return {'status': 'Healthy!'}


@app.post('/upload')
async def upload_file(file: UploadFile):
    id = uuid4()

    # Saving in mongodb
    db_file = await files_collection.insert_one(
        document=FileSchema(
            name=file.filename,
            status="saving"
        )
    )

    # in linux, if we upload any thing it goes to mount (mnt dir)
    # need to typecast the inserted_id to str
    file_path = f"/mnt/upload/{str(db_file.inserted_id)}/{file.filename}"

    # save file
    # reading the file.read()
    await save_to_disk(file=await file.read(), path=file_path)

    # push to queue
    q.enqueue(process_file, str(db_file.inserted_id), file_path)

    # Once the file is saved, updating the mongo statue
    await files_collection.update_one(
        {'_id': db_file.inserted_id}, {
            "$set": {
                "status": "queued"
            }
        }
    )

    return {'file_id': str(db_file.inserted_id)}
