from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_required
from project.services import AdminMessagesService
import json

admin_messages_bp = Blueprint("admin_messages", __name__)


@admin_messages_bp.route("/admin_messages")
@login_required
def admin_messages():
    if current_user.status not in ["MASTER", "ADMIN"]:
        flash("You are not a high enough status for this page.", "warning")
        return redirect(url_for("home.home"))

    messages = AdminMessagesService.fetch_all_messages()
    return render_template("admin_messages.html", messages=messages)


@admin_messages_bp.route("/admin_messages_api/retrieve/<int:message_id>")
@login_required
def admin_messages_api_retrieve(message_id):
    if current_user.status not in ["MASTER", "ADMIN"]:
        return json.dumps({})

    message_data = AdminMessagesService.fetch_message_data(message_id)
    if message_data is None:
        message_data = {}

    message_data_json = json.dumps(message_data)

    return message_data_json


@admin_messages_bp.route("/admin_messages/dismiss/<int:message_id>")
@login_required
def admin_messages_dismiss(message_id):
    if current_user.status not in ["MASTER", "ADMIN"]:
        flash("You are not a high enough status for this page.", "warning")
        return redirect(url_for("home.home"))

    AdminMessagesService.dismiss_message(message_id)
    messages = AdminMessagesService.fetch_all_messages()

    return render_template("admin_messages.html", messages=messages)
