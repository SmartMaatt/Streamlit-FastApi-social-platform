from fastapi import APIRouter, File, status
from ..functions import image_edit

router = APIRouter(
    prefix='/image-edit',
    tags=['Image edit']
)


@router.post('/crop-profile-image', status_code=status.HTTP_201_CREATED)
def crop_profile_image(file: bytes = File(...)):
    return image_edit.crop_profile_image(file)
