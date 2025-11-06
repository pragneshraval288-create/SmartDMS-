from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Document
from ..forms.document_forms import DocumentForm
from ..utils.files import allowed_file, save_file
from ..utils.versioning import next_version_for_filename
from ..utils.audit import log_audit
from ..utils.permissions import user_or_admin_owns

# ✅ FIX — Blueprint MUST be defined before using @bp.route
bp = Blueprint('documents', __name__)

def _user_scoped_query():
    return Document.query if current_user.role == 'admin' else Document.query.filter_by(uploader_id=current_user.id)


# ✅ Upload
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = DocumentForm()
    if form.validate_on_submit() and form.file.data and allowed_file(form.file.data.filename):
        version = next_version_for_filename(form.file.data.filename)
        stored_filename = save_file(form.file.data)

        doc = Document(
            title=form.title.data,
            filename=stored_filename,
            uploader_id=current_user.id,
            tags=form.tags.data,
            version=version
        )

        db.session.add(doc)
        db.session.commit()
        log_audit('uploaded', doc.filename, doc.version)
        flash('File uploaded successfully', 'success')

        return redirect(url_for('documents.list'))

    return render_template('upload.html', form=form)


# ✅ Documents List
@bp.route('/documents')
@login_required
def list():
    page = int(request.args.get('page', 1))
    per_page = 10

    q = _user_scoped_query()

    title = request.args.get('title')
    tags  = request.args.get('tags')
    ftype = request.args.get('type')

    # ✅ Title filter
    if title:
        q = q.filter(Document.title.ilike(f'%{title}%'))

    # ✅ Tag filter
    if tags:
        q = q.filter(Document.tags.ilike(f'%{tags}%'))

    # ✅ File type filter
    if ftype:
        if ftype == "image":
            q = q.filter(
                Document.filename.ilike('%.jpg') |
                Document.filename.ilike('%.jpeg') |
                Document.filename.ilike('%.png')
            )
        else:
            q = q.filter(Document.filename.ilike(f'%.{ftype}'))

    total = q.count()
    docs = (
        q.order_by(Document.upload_date.desc())
         .offset((page - 1) * per_page)
         .limit(per_page)
         .all()
    )

    return render_template(
        'documents.html',
        documents=docs,
        page=page,
        total_pages=(total // per_page) + (1 if total % per_page > 0 else 0)
    )


# ✅ Download
@bp.route('/download/<int:doc_id>')
@login_required
def download(doc_id):
    doc = Document.query.get_or_404(doc_id)

    if not user_or_admin_owns(doc):
        flash('Permission denied!', 'danger')
        return redirect(url_for('documents.list'))

    from flask import current_app
    log_audit('downloaded', doc.filename, doc.version)

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        doc.filename,
        as_attachment=True
    )


# ✅ Preview
@bp.route('/preview/<int:doc_id>')
@login_required
def preview(doc_id):
    doc = Document.query.get_or_404(doc_id)

    if not user_or_admin_owns(doc):
        flash('Permission denied!', 'danger')
        return redirect(url_for('documents.list'))

    from flask import current_app

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        doc.filename,
        as_attachment=False
    )


# ✅ Update
@bp.route('/update/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def update(doc_id):
    original = Document.query.get_or_404(doc_id)

    if not user_or_admin_owns(original):
        flash('Permission denied', 'danger')
        return redirect(url_for('documents.list'))

    form = DocumentForm()

    if form.validate_on_submit():
        original.title = form.title.data
        original.tags  = form.tags.data
        db.session.commit()

        # File updated also → create new version
        if form.file.data and allowed_file(form.file.data.filename):
            new_version = next_version_for_filename(form.file.data.filename)
            stored = save_file(form.file.data)

            new_doc = Document(
                title=original.title,
                filename=stored,
                uploader_id=original.uploader_id,
                tags=original.tags,
                version=new_version
            )

            db.session.add(new_doc)
            db.session.commit()

            log_audit('updated', new_doc.filename, new_doc.version)
            flash('New version created', 'success')

        else:
            flash('Document updated', 'success')

        return redirect(url_for('documents.list'))

    # GET request → load existing values
    if request.method == 'GET':
        form.title.data = original.title
        form.tags.data  = original.tags

    return render_template('update_document.html', form=form, doc=original)


# ✅ Delete
@bp.route('/delete/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def delete(doc_id):
    doc = Document.query.get_or_404(doc_id)

    if not user_or_admin_owns(doc):
        flash('Permission denied', 'danger')
        return redirect(url_for('documents.list'))

    try:
        from flask import current_app
        import os

        path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
        if os.path.exists(path):
            os.remove(path)

        db.session.delete(doc)
        db.session.commit()

        log_audit('deleted', doc.filename, doc.version)
        flash('Document deleted', 'success')

    except:
        flash('Error deleting document', 'danger')

    return redirect(url_for('documents.list'))
