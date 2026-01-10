from fastapi import APIRouter, UploadFile, File, Form
import json
import uuid
from cloudinary.uploader import upload

from app.core.database import templates_collection
from app.core.cloudinary import cloudinary

router = APIRouter()


router = APIRouter()

@router.post("/")
async def create_template(
    name: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(...),
    placeholders: str = Form(...),
):
    # Upload image to Cloudinary
    upload_result = upload(
        image.file,
        folder="visiting_cards/templates",
        public_id=str(uuid.uuid4()),
    )

    image_url = upload_result["secure_url"]

    template_doc = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "imageUrl": image_url,
        "placeholders": json.loads(placeholders),
        "isActive": True,
    }

    templates_collection.insert_one(template_doc)

    return template_doc
