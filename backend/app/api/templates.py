# from fastapi import APIRouter, UploadFile, File, Form
# import json
# import uuid
# from cloudinary.uploader import upload

# from app.core.database import templates_collection

# router = APIRouter()

# # ✅ CREATE TEMPLATE (ADMIN)
# @router.post("/")
# async def create_template(
#     name: str = Form(...),
#     description: str = Form(""),
#     image: UploadFile = File(...),
#     placeholders: str = Form(...),
# ):
#     upload_result = upload(
#         image.file,
#         folder="visiting_cards/templates",
#         public_id=str(uuid.uuid4()),
#     )

#     template_doc = {
#         "_id": str(uuid.uuid4()),
#         "name": name,
#         "description": description,
#         "imageUrl": upload_result["secure_url"],
#         "placeholders": json.loads(placeholders),
#         "isActive": True,
#     }

#     templates_collection.insert_one(template_doc)
#     return template_doc


# # ✅ LIST TEMPLATES (FLUTTER APP)
# @router.get("/")
# def list_templates():
#     templates = list(
#         templates_collection.find({"isActive": True})
#     )

#     for t in templates:
#         t["_id"] = str(t["_id"])

#     return templates



























from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from cloudinary.uploader import upload
from app.core.database import templates_collection
from typing import Optional
import json
import uuid

router = APIRouter()


# =====================================================
# ✅ CREATE TEMPLATE (ADMIN)
# =====================================================
@router.post("/")
async def create_template(
    name: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(...),
    placeholders: str = Form(...),
):
    try:
        placeholders_data = json.loads(placeholders)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid placeholders JSON")

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
        "placeholders": placeholders_data,
        "isActive": True,
    }

    templates_collection.insert_one(template_doc)
    return template_doc


# =====================================================
# ✅ LIST ALL ACTIVE TEMPLATES
# =====================================================
@router.get("/")
def list_templates():
    templates = list(
        templates_collection.find({"isActive": True})
    )

    for t in templates:
        t["_id"] = str(t["_id"])

    return templates


# =====================================================
# ✅ GET TEMPLATE BY ID
# =====================================================
@router.get("/{template_id}")
def get_template_by_id(template_id: str):
    template = templates_collection.find_one(
        {"_id": template_id, "isActive": True}
    )

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    template["_id"] = str(template["_id"])
    return template


# =====================================================
# ✅ UPDATE TEMPLATE BY ID (ADMIN)
# =====================================================
@router.put("/{template_id}")
async def update_template(
    template_id: str,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    placeholders: Optional[str] = Form(None),
):
    template = templates_collection.find_one({"_id": template_id})

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    update_data = {}

    if name is not None:
        update_data["name"] = name

    if description is not None:
        update_data["description"] = description

    if placeholders is not None:
        try:
            update_data["placeholders"] = json.loads(placeholders)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid placeholders JSON")

    if image is not None:
        upload_result = upload(
            image.file,
            folder="visiting_cards/templates",
        )
        update_data["imageUrl"] = upload_result["secure_url"]

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    templates_collection.update_one(
        {"_id": template_id},
        {"$set": update_data}
    )

    return {
        "message": "Template updated successfully",
        "templateId": template_id,
        "updatedFields": list(update_data.keys())
    }
