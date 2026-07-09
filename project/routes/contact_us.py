from project.services import ContactUsService
from project.forms import ContactUsForm
from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required

contact_us_bp = Blueprint("contact_us", __name__)


@contact_us_bp.route("/contact_us", methods=["GET", "POST"])
@login_required
def contact_us():
    form = ContactUsForm()
    # User has not submitted a valid form
    if not form.validate_on_submit():
        return render_template("contact_us.html", form=form)

    # User has submitted a valid form
    type_id = form.message_type.data
    title = form.title.data
    message = form.message.data

    service = ContactUsService(title, message, current_user.id, type_id)
    service.send_admin_message()

    flash("Message sent.", "success")
    return redirect(url_for("home.home"))
