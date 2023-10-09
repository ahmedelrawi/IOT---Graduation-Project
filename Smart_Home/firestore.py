from firebase_admin import credentials, initialize_app
from firebase_admin.firestore import client
from hash import check_password


# Use a global variable to check if Firebase Admin SDK is already initialized
firebase_initialized = False

def firebase_init():
    global firebase_initialized
    if not firebase_initialized:
        # Initialize Firebase Admin SDK
        firbase_credentials = credentials.Certificate('./serviceAccountKey.json')

        # Initialize the app with a service account, granting admin privileges
        initialize_app(firbase_credentials)

        # Set the global variable to True
        firebase_initialized = True

def upload_image(image_string: str, image_id: str):
    try:
        # Create a Firestore client
        firestore = client()

        # Save the image bytes to Firestore images collection
        image_document  = firestore.collection('images').document(image_id)

        # Set the image data in the document
        image_document.set({'image_data': image_string})

        print(f"{image_id} Image has been uploaded successfully.")
    except Exception as e:
        print(f"An error occurred while uploading the image: {str(e)}")

def download_image(id: str):
    # Create a Firestore client
    firestore = client()

    # Fetch the data from Firestore
    img_doc = firestore.collection('images').document(id)

    # Get the image data
    data = img_doc.get()

    # Check if the document exists
    image_data = data.get('image_data')

    # Return the image data  
    return image_data

def check_user_and_pass(collection_name, username, password):
    # Create a Firestore client
    db = client()

    # Reference the collection you want to loop through (e.g., 'users')
    users_ref = db.collection(collection_name)

    # Fetch all documents in the collection
    users = users_ref.stream()

    # Iterate through the documents
    for user in users:
        # Get the data from each document
        user_data = user.to_dict()

        # Check if the username and password match
        if user_data['Username'] == username:
            print("Username found")
            if check_password(password, user_data['Password']):
                print("Password matches")
                return True
            else:
                print("Password does not match")
                return False
        print("Username not found")
        return False

def download_images():
    # Create a Firestore client
    db = client()

    # Reference the collection you want to loop through (e.g., 'users')
    users_ref = db.collection('images')

    # Fetch all documents in the collection
    images = users_ref.stream()

    # all images data list as {"data": "encoded_image_1", "name": "2023-01-15.jpg"},
    all_images = []

    # Iterate through the documents
    for image in images:
        # get document name
        doc_name = image.id

        # get document data "image_data"
        image_data = image.to_dict()

        # get image data
        image_string = image_data['image_data']

        # append in first place to all_images
        all_images.insert(0, {"data": image_string, "name": doc_name})
        
    # return all images
    return all_images