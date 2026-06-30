from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.menu_service import MenuService
from app.utils.upload import save_upload_file

router = APIRouter(prefix="/menu", tags=["Menu Items"])


@router.post("/")
def create_menu_item(data: dict, db: Session = Depends(get_db)):
    return MenuService.create(db, data)


@router.get("/")
def get_all_menu_items(db: Session = Depends(get_db)):
    return MenuService.get_all(db)


@router.get("/{item_id}")
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    return MenuService.get_by_id(db, item_id)


@router.put("/{item_id}")
def update_menu_item(item_id: int, data: dict, db: Session = Depends(get_db)):
    return MenuService.update(db, item_id, data)


@router.post("/{item_id}/image")
def upload_menu_image(item_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_path = save_upload_file(file, subdirectory=str(item_id))
    return MenuService.upload_image(db, item_id, image_path)


@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    return MenuService.delete(db, item_id)