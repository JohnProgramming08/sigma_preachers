from project.services import EditProfileService
from project.forms import EditProfileForm
from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required

edit_profile_bp = Blueprint("edit_profile", __name__)


@edit_profile_bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        form.bio.data = current_user.bio
        return render_template("edit_profile.html", form=form)

    # User has submitted a valid form
    form_data = {
        "username": form.username.data,
        "gender": form.gender.data,
        "age": form.age.data,
        "location": form.location.data,
        "colour": form.colour.data,
        "bio": form.bio.data,
    }
    service = EditProfileService(current_user.id, form_data)
    update_success = service.update_profile()

    if update_success:
        return redirect(
            url_for("view_profile.view_profile", id=current_user.id)
        )

    # Profile update failed
    flash("That username is already taken.", "warning")
    return render_template("edit_profile.html", form=form)
