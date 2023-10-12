from io import BytesIO
from PIL import Image
import base64, os

def decode_image(image_data: str, output_name: str = "decoded_image.jpg", output_path: str = "downloaded_images"):
    # Decode the base64 image data
    image_bytes = base64.b64decode(image_data)

    # Convert the bytes to an image
    new_image = Image.open(BytesIO(image_bytes))

    # Save the image to the given path
    output_location = os.path.join(output_path, output_name)

    # Save the image
    new_image.save(output_location, format='JPEG')

    # Display the image
    new_image.show()


def encode_image(path: str):
    # Open the image from the given path
    image = Image.open(path)

    # Convert the image to a base64 string
    buffer = BytesIO()

    # Save the image to the buffer
    image.save(buffer, format='png')
    
    # Encode the image to base64
    return base64.b64encode(buffer.getvalue()).decode('utf-8')