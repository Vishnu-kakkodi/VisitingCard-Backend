# from fastapi import APIRouter, HTTPException
# from pathlib import Path
# import uuid

# from app.core.database import templates_collection
# from app.services.image_renderer import render_card

# router = APIRouter()


# router = APIRouter()

# GENERATED_DIR = Path("app/storage/generated")
# GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# @router.post("/{template_id}")
# def generate_card(template_id: str, payload: dict):
#     template = templates_collection.find_one({"_id": template_id})

#     if not template:
#         raise HTTPException(status_code=404, detail="Template not found")

#     image_path = Path("app") / template["imageUrl"].replace("/storage/", "storage/")
#     placeholders = template["placeholders"]
#     values = payload.get("values", {})

#     img = render_card(
#         template_path=image_path,
#         placeholders=placeholders,
#         values=values
#     )

#     output_name = f"{uuid.uuid4()}.png"
#     output_path = GENERATED_DIR / output_name
#     img.save(output_path)

#     return {
#         "imageUrl": f"/storage/generated/{output_name}"
#     }
























from fastapi import APIRouter, HTTPException
from app.core.database import templates_collection
from app.services.image_renderer import render_card
from pathlib import Path
import uuid
import requests
from io import BytesIO
from PIL import Image

router = APIRouter()

GENERATED_DIR = Path("app/storage/generated")
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/{template_id}")
def generate_card(template_id: str, payload: dict):
    template = templates_collection.find_one({"_id": template_id})

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    image_url = template["imageUrl"]  # Cloudinary URL
    placeholders = template["placeholders"]
    values = payload.get("values", {})

    # 🔥 Download image from Cloudinary
    response = requests.get(image_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download template image")

    img = Image.open(BytesIO(response.content)).convert("RGBA")

    img = render_card(
        img=img,
        placeholders=placeholders,
        values=values
    )

    output_name = f"{uuid.uuid4()}.png"
    output_path = GENERATED_DIR / output_name
    img.save(output_path)

    return {
        "imageUrl": f"/storage/generated/{output_name}"
    }
