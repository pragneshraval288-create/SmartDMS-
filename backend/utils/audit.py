from ..extensions import db
from ..models import Audit
from flask_login import current_user

def log_audit(action, filename, version):
    if not current_user.is_authenticated: return
    db.session.add(Audit(user_id=current_user.id, action=action, filename=filename, version=version))
    db.session.commit()
