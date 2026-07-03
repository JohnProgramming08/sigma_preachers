from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from project.services import SearchUsersService
import json

search_users_api_bp = Blueprint("search_users_api", __name__)


@search_users_api_bp.route(
    "/search_users_api/<username>/<int:start>", methods=["POST"]
)
def search_users_api(username, start):
    service = SearchUsersService(username, start)
    found_users = service.fetch_next_10_users()
    found_users["last"] = start
    found_users_json = json.dumps(found_users)

    return found_users_json
