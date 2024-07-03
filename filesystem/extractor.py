import os
import zipfile

def extract_osz_files(osz_directory, extract_to):
    for file_name in os.listdir(osz_directory):
        if file_name.endswith('.osz'):
            file_path = os.path.join(osz_directory, file_name)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
