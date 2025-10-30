import random
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request

from .models import services_data

bookings_bp = Blueprint("bookings", __name__, url_prefix="/api/v1")


# Kullanıcıdan gelen rezervasyon isteğini doğrulayıp geçerliyse kayıt et değilse ilgili hatayı fırlat.
@bookings_bp.route("/bookings", methods=["POST"])
def create_booking():
    try:
        data = request.get_json()
        if not data:
            raise ValueError()
    except:
        current_app.logger.error(
            "Rezervasyon oluşturma hatası: Geçersiz veya boş JSON."
        )
        return jsonify({"error": "Geçersiz JSON formatı."}), 400

    errors = {}
    valid_service_ids = {s["id"] for s in services_data}

    if "service_ids" not in data or not isinstance(data["service_ids"], list):
        errors["service_ids"] = "service_ids alanı zorunudur ve bir liste olmalıdır."
    else:
        if len(data["service_ids"]) != len(set(data["service_ids"])):
            errors["service_ids"] = "Bir hizmet ID'si listeye birden fazla eklenemez."
        else:
            for service_id in data["service_ids"]:
                if service_id not in valid_service_ids:
                    errors["service_ids"] = (
                        f"Geçersiz hizmet ID'si: {service_id}. Bu ID sistemde mevcut değil."
                    )
                    break

    if "event_date" not in data:
        errors["event_date"] = "event_date alanı zorunludur."
    elif "event_date" not in errors and "service_ids" not in errors:
        try:
            event_date = datetime.strptime(data["event_date"], "%Y-%m-%d").date()
            if event_date < datetime.now().date():
                errors["event_date"] = "Tarih geçmiş bir tarih olamaz."
        except ValueError:
            errors["event_date"] = "Tarih formatı YYYY-MM-DD olmalıdır."

    if errors:
        key = list(errors.keys())[0]
        error_message = errors[key]
        current_app.logger.warning(
            f"Doğrulama hatası: Alan='{key}', Hata='{error_message}', Gelen Veri='{data}'"
        )
        return jsonify({"error": "Geçersiz veri.", "details": {key: errors[key]}}), 400

    booking_id = random.randint(1000, 9999)
    response = {"message": "Rezervasyon talebiniz alındı.", "booking_id": booking_id}
    current_app.logger.info(
        f"Yeni rezervasyon talebi başarıyla oluşturuldu: booking_id={booking_id}"
    )
    return jsonify(response), 201
