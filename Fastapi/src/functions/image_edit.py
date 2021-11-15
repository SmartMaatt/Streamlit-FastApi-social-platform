import io
from fastapi import File, status, HTTPException
from starlette.responses import Response
from PIL import Image


def crop_profile_image(image: bytes = File(...)):
    try:
        input_image = Image.open(io.BytesIO(image)).convert("RGB")
        profile_picture = crop_max_square(input_image)
        bytes_io = io.BytesIO()
        profile_picture.save(bytes_io, format="PNG")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except OSError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Couldn't process given parameters! Are you sure you've posted a picture?")


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))
