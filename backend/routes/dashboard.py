from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from ..models import Document, Audit

bp = Blueprint('dashboard', __name__)

def _user_scoped_query(model):
    # ✅ Admin can see everything, user only sees their own
    return model.query if current_user.role == 'admin' else model.query.filter_by(uploader_id=current_user.id)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def home():
    # ✅ Document Stats
    q = _user_scoped_query(Document)
    total_docs = q.count()

    since = datetime.utcnow() - timedelta(days=7)
    week_uploads = q.filter(Document.upload_date >= since).count()

    # ✅ Audit Logs (Recent Activity)
    activity_q = Audit.query.order_by(Audit.timestamp.desc())

    if current_user.role != 'admin':
        activity_q = activity_q.filter_by(user_id=current_user.id)

    recent = activity_q.limit(8).all()

    # ✅ Include username + action + version + timestamp clean format
    recent_activity = [
        f"{a.user.username.title()} • {a.action.title()} • {a.filename} (v{a.version}) • {a.timestamp.strftime('%d %b %Y %H:%M')}"
        for a in recent
    ]

    stats = {
        'total_docs': total_docs,
        'week_uploads': week_uploads
    }

    return render_template('dashboard.html', stats=stats, recent_activity=recent_activity)
