import base64


async def convert_base64(image_name, encoded_image):
    with open("../images/{image_name}.png".format(image_name=image_name), "wb") as fh:
        fh.write(base64.decodebytes(encoded_image))
    return "../images/{image_name}.png".format(image_name=image_name)
