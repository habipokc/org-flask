import json

import pytest

from app import create_app
from app.models import services_data


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# Test 1: Hizmetleri listeleme endpoint'inin doğru çalışıp çalışmadığını test et.
def test_get_services(client):
    """GET /api/v1/services testi"""
    response = client.get("/api/v1/services")
    expected_count = len(services_data)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == expected_count


# Test 2: Başarılı bir rezervasyon talebi oluşturmayı test et (Happy Path).
def test_create_booking_success(client):
    """POST /api/v1/bookings için başarılı senaryo testi"""
    payload = {
        "service_ids": [1, 3],
        "event_date": "2026-01-15",
        "notes": "Test notu",
    }
    response = client.post(
        "/api/v1/bookings", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 201
    response_data = response.get_json()
    assert "message" in response_data
    assert "booking_id" in response_data


# Test 3: Geçersiz bir hizmet ID'si gönderildiğinde hata alınmasını test et.
def test_create_booking_invalid_service_id(client):
    """POST /api/v1/bookings için geçersiz service_id testi"""
    payload = {"service_ids": [1, 99], "event_date": "2026-01-15"}
    response = client.post(
        "/api/v1/bookings", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    response_data = response.get_json()
    assert "Geçersiz hizmet ID'si: 99" in response_data["details"]["service_ids"]


# Test 4: Geçmiş bir tarih gönderildiğinde hata alınmasını test et.
def test_create_booking_past_date(client):
    """POST /api/v1/bookings için geçmiş tarih testi"""
    payload = {"service_ids": [1], "event_date": "2020-01-01"}
    response = client.post(
        "/api/v1/bookings", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    response_data = response.get_json()
    assert "Tarih geçmiş bir tarih olamaz" in response_data["details"]["event_date"]


# Test 5: Tekrarlanan hizmet ID'si gönderildiğinde hata alınmasını test et.
def test_create_booking_duplicate_service_ids(client):
    """POST /api/v1/bookings için tekrarlanan service_id testi"""
    payload = {"service_ids": [2, 2], "event_date": "2026-01-15"}
    response = client.post(
        "/api/v1/bookings", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    response_data = response.get_json()
    assert "birden fazla eklenemez" in response_data["details"]["service_ids"]
