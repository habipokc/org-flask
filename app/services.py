from flask import Blueprint, jsonify

from .models import services_data

services_bp = Blueprint("services", __name__, url_prefix="/api/v1")


@services_bp.route("/services", methods=["GET"])
def get_service():
    return jsonify(services_data)
