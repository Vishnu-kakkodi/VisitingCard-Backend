from fastapi import APIRouter, UploadFile, File, Form
import json
import uuid
from cloudinary.uploader import upload

from app.core.database import templates_collection

router = APIRouter()

# ✅ CREATE TEMPLATE (ADMIN)
@router.post("/")
async def create_template(
    name: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(...),
    placeholders: str = Form(...),
):
    upload_result = upload(
        image.file,
        folder="visiting_cards/templates",
        public_id=str(uuid.uuid4()),
    )

    template_doc = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "imageUrl": upload_result["secure_url"],
        "placeholders": json.loads(placeholders),
        "isActive": True,
    }

    templates_collection.insert_one(template_doc)
    return template_doc


# ✅ LIST TEMPLATES (FLUTTER APP)
@router.get("/")
def list_templates():
    templates = list(
        templates_collection.find({"isActive": True})
    )

    for t in templates:
        t["_id"] = str(t["_id"])

    return templates
