import firebase_admin
from firebase_admin import credentials, storage

# Replace 'path/to/your/serviceAccountKey.json' with the path to your Firebase service account key file
cred = credentials.Certificate('backend/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'numplate-face.appspot.com'})

def download_image_from_storage(image_path_in_storage, local_file_path):
    bucket = storage.bucket()
    blob = bucket.blob(image_path_in_storage)

    try:
        blob.download_to_filename(local_file_path)
        print(f"Image downloaded successfully to {local_file_path}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Replace 'Registration/GJ01234' with the correct path in your Firebase Storage
# Replace 'backend/test.png' with the local path where you want to save the downloaded image
download_image_from_storage('Registration/GJ01234', 'backend/test.png')
