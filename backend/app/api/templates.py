from fastapi import APIRouter, UploadFile, File, Form
from backend.app.core.database import templates_collection
from pathlib import Path
import uuid
import json
from datetime import datetime

router = APIRouter()

TEMPLATE_DIR = Path("app/storage/templates")
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def create_template(
    image: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(""),
    placeholders: str = Form(...),
):
    template_id = str(uuid.uuid4())

    # Save image
    image_path = TEMPLATE_DIR / f"{template_id}.png"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    placeholder_data = json.loads(placeholders)

    template_doc = {
        "_id": template_id,
        "name": name,
        "description": description,
        "imageUrl": f"/storage/templates/{template_id}.png",
        "placeholders": placeholder_data,
        "isActive": True,
        "createdAt": datetime.utcnow(),
    }

    templates_collection.insert_one(template_doc)

    return template_doc



@router.get("/")
def get_templates():
    templates = list(templates_collection.find({"isActive": True}))
    return templates
