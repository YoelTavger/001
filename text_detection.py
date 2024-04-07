import re
from google.cloud import vision
from google.auth import credentials

GOOGLE_CLOUD_API_KEY_FILE = 'path/to/your/service-account-key.json'

def detect_text(path):
    """Detects text in the file."""
    credentials = credentials.ServiceAccountCredentials.from_service_account_file(GOOGLE_CLOUD_API_KEY_FILE)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts: ", texts[0].description)
    try:
        newText = re.findall(r'\b\d{3}\b', texts[0].description)
        print(f"newText-success: {newText}")
    except:
        newText = [999]
        print(f"newText-error: {newText}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return newText

if __name__ == "__main__":
    detect_text("./image.jpg")