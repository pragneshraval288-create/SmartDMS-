from sqlalchemy import func
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import Document

def next_version_for_filename(original_name:str)->int:
    clean = secure_filename(original_name)
    if '.' in clean:
        base, ext = clean.rsplit('.',1)
        pattern = f"{base}%." + ext
    else:
        base, ext = clean, ''
        pattern = clean + '%'
    max_ver = db.session.query(func.max(Document.version)).filter(Document.filename.like(pattern)).scalar()
    return (max_ver or 0) + 1
