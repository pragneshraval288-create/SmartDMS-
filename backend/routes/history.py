from flask import Blueprint, render_template_string, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Document

bp = Blueprint('history', __name__)

def _owns(doc):
    return (current_user.role=='admin') or (current_user.id==doc.uploader_id)

@bp.route('/history/<int:doc_id>')
@login_required
def show(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if not _owns(doc): flash('Permission denied!', 'danger'); return redirect(url_for('documents.list'))
    base, ext = (doc.filename.rsplit('.',1)+[''])[:2]
    logical_base = base.split('_')[0]
    versions = Document.query.filter(Document.filename.like(f"{logical_base}%." + ext)).order_by(Document.version.desc()).all()
    tmpl = """
    {% extends 'base.html' %}
    {% block title %}History · DMS{% endblock %}
    {% block content %}
    <div class="card p-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div class="fw-semibold">Version History – {{ title }}</div>
        <a class="btn btn-sm btn-outline-secondary" href="{{ url_for('documents.list') }}">Back</a>
      </div>
      <div class="table-responsive">
        <table class="table align-middle">
          <thead><tr><th>Version</th><th>Filename</th><th>Uploaded</th><th class="text-end">Actions</th></tr></thead>
          <tbody>
            {% for v in versions %}
            <tr>
              <td class="fw-semibold">v{{ v.version }}</td>
              <td>{{ v.filename }}</td>
              <td>{{ v.upload_date.strftime('%d %b %Y %H:%M') }}</td>
              <td class="text-end">
                <a class="btn btn-sm btn-outline-secondary" href="{{ url_for('documents.download', doc_id=v.id) }}"><i class="bi bi-download"></i></a>
                <a class="btn btn-sm btn-outline-secondary" href="{{ url_for('documents.preview', doc_id=v.id) }}"><i class="bi bi-eye"></i></a>
              </td>
            </tr>
            {% else %}
            <tr><td colspan="4" class="text-center text-muted">No versions found.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
    {% endblock %}
    """
    return render_template_string(tmpl, versions=versions, title=doc.title)
