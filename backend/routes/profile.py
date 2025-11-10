from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from backend.extensions import db
from backend.forms.profile_form import ProfileForm
from backend.models import User   # ✅ NECESSARY FIX

bp = Blueprint("profile", __name__)

@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():

        # ✅ Email unique check
        if form.email.data.lower() != current_user.email:
            if User.query.filter_by(email=form.email.data.lower()).first():
                flash("Email already taken!", "danger")
                return render_template("profile.html", form=form)

        # ✅ Mobile unique check
        if form.mobile.data != current_user.mobile:
            if User.query.filter_by(mobile=form.mobile.data).first():
                flash("Mobile already used!", "danger")
                return render_template("profile.html", form=form)

        # ✅ Update values
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data.lower()
        current_user.mobile = form.mobile.data
        current_user.dob = form.dob.data

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.profile"))

    # ✅ Pre-fill form
    form.full_name.data = current_user.full_name
    form.email.data = current_user.email
    form.mobile.data = current_user.mobile
    form.dob.data = current_user.dob

    return render_template("profile.html", form=form)
