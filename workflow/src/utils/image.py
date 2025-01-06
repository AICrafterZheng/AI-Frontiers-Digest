import mimetypes
import base64

 #Function to encode the image
def encode_image(image_path):
    # get the mime type of the image
    mime_type = get_image_mime_type(image_path)
    with open(image_path, "rb") as image_file:
        return f"data:{mime_type};base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

def get_image_mime_type(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type or 'application/octet-stream'