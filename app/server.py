from fastapi import FastAPI, UploadFile, Path
from uuid import uuid4
from .utils.file import save_to_disk
from .db.collections.files import files_collection, FileSchema
from .queue.queue import q
from .queue.workers import process_file
from bson import ObjectId

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

@app.get('/{id}')
async def get_file_by_id(id:str = Path(..., description="The id of the file to get")):
    db_file = await files_collection.find_one({"_id": ObjectId(id)})
    
    return {
        "_id": str(db_file["_id"]),
        "name": db_file["name"],
        "status": db_file["status"],
        "result": db_file["result"] if "result" in db_file else None
    }
    