from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

from backend.extensions import db
from backend.forms.profile_form import ProfileForm
from backend.models.models import User
from backend.security_helpers import validate_password  # your existing validator

bp = Blueprint("profile", __name__)

ALLOWED_IMG_EXT = {"jpg", "jpeg", "png"}


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    form = ProfileForm()

    # Pre-fill on GET (or initial render)
    if request.method == "GET":
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
        try:
            form.dob.data = current_user.dob
        except Exception:
            # if dob stored as string, leave as-is
            pass

    if form.validate_on_submit():
        # We'll allow updates — but for sensitive changes require current_password
        wants_to_change_sensitive = False
        if (form.new_password.data and form.new_password.data.strip()) or \
           (form.email.data and form.email.data.lower() != (current_user.email or "").lower()) or \
           (form.mobile.data and form.mobile.data != current_user.mobile):
            wants_to_change_sensitive = True

        # If user wants sensitive changes, current_password must be provided and correct
        if wants_to_change_sensitive:
            if not form.current_password.data:
                flash("Current password is required to change email/mobile/password.", "danger")
                return render_template("profile.html", form=form)
            if not check_password_hash(current_user.password, form.current_password.data):
                flash("Current password is incorrect.", "danger")
                return render_template("profile.html", form=form)

        # ----- Email uniqueness check -----
        new_email = (form.email.data or "").lower()
        if new_email and new_email != (current_user.email or "").lower():
            if User.query.filter(User.email == new_email, User.id != current_user.id).first():
                flash("Email already in use by another account.", "danger")
                return render_template("profile.html", form=form)

        # ----- Mobile uniqueness check -----
        if form.mobile.data and form.mobile.data != current_user.mobile:
            if User.query.filter(User.mobile == form.mobile.data, User.id != current_user.id).first():
                flash("Mobile number already in use by another account.", "danger")
                return render_template("profile.html", form=form)

        # ----- Profile picture upload -----
        image_file = request.files.get("profile_pic")
        if image_file and image_file.filename:
            ext = image_file.filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_IMG_EXT:
                flash("Only JPG/PNG images allowed for profile picture.", "danger")
                return render_template("profile.html", form=form)

            # Save under frontend/static/profile_pics/
            filename = f"user_{current_user.id}_{secrets.token_hex(6)}.{ext}"
            save_dir = os.path.join(current_app.root_path, "frontend", "static", "profile_pics")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            image_file.save(save_path)

            # OPTIONAL: delete previous custom file (if not default)
            try:
                prev = current_user.profile_pic or ""
                if prev and prev not in ("default_user.png", "default.png"):
                    prev_path = os.path.join(save_dir, prev)
                    if os.path.exists(prev_path):
                        os.remove(prev_path)
            except Exception:
                pass

            current_user.profile_pic = filename

        # ----- Password change -----
        if form.new_password.data and form.new_password.data.strip():
            ok, msg = validate_password(form.new_password.data)
            if not ok:
                flash(msg, "danger")
                return render_template("profile.html", form=form)
            current_user.password = generate_password_hash(form.new_password.data)
            flash("Password updated successfully.", "success")

        # ----- Update other fields -----
        current_user.full_name = form.full_name.data
        current_user.email = new_email or None
        current_user.mobile = form.mobile.data or None
        # dob might be Date or string; store as string if needed
        try:
            current_user.dob = form.dob.data
        except Exception:
            current_user.dob = form.dob.data

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.profile_page"))

    return render_template("profile.html", form=form)
