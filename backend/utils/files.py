import os
from werkzeug.utils import secure_filename
from flask import current_app
from .versioning import next_version_for_filename

def allowed_file(filename:str)->bool:
    exts = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf','docx','txt','xlsx','pptx','jpg','jpeg','png'})
    return ('.' in filename) and (filename.rsplit('.',1)[1].lower() in exts)

def save_file(file_storage):
    """Save under UPLOAD_FOLDER with collision-safe name."""
    filename = secure_filename(file_storage.filename)
    folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    base, ext = os.path.splitext(filename)
    candidate = filename
    i = 1
    while os.path.exists(os.path.join(folder, candidate)):
        candidate = f"{base}_{i}{ext}"; i += 1
    file_storage.save(os.path.join(folder, candidate))
    return candidate
