import os
from dotenv import load_dotenv
from ..db.collections.files import files_collection
from bson import ObjectId
from pdf2image import convert_from_path
import base64
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

async def process_file(id: str, file_path: str):
    print(f"Processing file with id: {id}")
    
    # changing the status of the file to processing in mongodb
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "processing"}}
    )
    
    # Step 1: Convert the file to pdf
    images = convert_from_path(file_path)
    image_paths = []
    
    # Create directory for saving images
    image_dir = f"/mnt/upload/images/{id}"
    os.makedirs(image_dir, exist_ok=True)
    
    # Save each image
    for i, image in enumerate(images):
        image_save_path = f"{image_dir}/image-{i}.jpg"
        image.save(image_save_path, 'JPEG') 
        image_paths.append(image_save_path)
    # Update the status of the file to converting to images success
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "converting to images success"}}
    )
    
    # Step 2: Calling openai with image
    # it contains the base64 encoded of all the images
    images_base64 = [encode_image(image_path) for image_path in image_paths]
    
    print("Calling openai...")
    
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "what's in this image?" },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{images_base64[0]}",
                        },
                    },
                ],
            }
        ],
    )
    
    print(completion.choices[0].message.content)
    
    # Update the status of the file to processed and storing the AI result
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "processed", "result": completion.choices[0].message.content}}
    )