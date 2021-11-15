import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def post_image_to_backend(image, server_url: str):
    encoder = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})
    request = requests.post(
        server_url, data=encoder, headers={"Content-Type": encoder.content_type}, timeout=100
    )
    return request
