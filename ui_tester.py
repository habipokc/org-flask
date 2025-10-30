import json

import gradio as gr
import requests

API_URL = "http://127.0.0.1:5000"


def get_available_services():
    """
    Uygulama başlarken API'den mevcut hizmetleri çeker ve
    Gradio'da göstermek için Markdown formatında bir metin oluşturur.
    """
    try:
        response = requests.get(f"{API_URL}/api/v1/services")
        if response.status_code == 200:
            services = response.json()
            markdown_text = "### Mevcut Hizmetler\n"
            markdown_text += "| ID | İsim | Kategori | Fiyat |\n"
            markdown_text += "|----|------|----------|-------|\n"
            for service in services:
                markdown_text += f"| {service['id']} | {service['name']} | {service['category']} | {service['price']} |\n"
            return markdown_text
        else:
            return "Hizmetler alınamadı. API sunucusunun çalıştığından emin olun."
    except requests.exceptions.ConnectionError:
        return "**HATA:** API sunucusuna bağlanılamıyor. Lütfen önce `python run.py` komutuyla sunucuyu başlattığınızdan emin olun."


def create_booking_request(service_ids_str, event_date, notes):
    """
    Gradio arayüzünden gelen girdileri alıp API'ye POST isteği gönderir.
    """
    try:

        service_ids = (
            [int(s.strip()) for s in service_ids_str.split(",")]
            if service_ids_str.strip()
            else []
        )
    except ValueError:
        return {
            "hata": "Hizmet ID'leri sadece rakamlardan ve virgüllerden oluşmalıdır."
        }

    payload = {"service_ids": service_ids, "event_date": event_date, "notes": notes}

    try:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(
            f"{API_URL}/api/v1/bookings", json=payload, headers=headers
        )

        return response.json()

    except requests.exceptions.ConnectionError:
        return {"hata": "API sunucusuna bağlanılamıyor. Sunucu çalışıyor mu?"}
    except json.JSONDecodeError:
        return {
            "hata": "API'den geçerli bir JSON yanıtı alınamadı.",
            "gelen_yanit": response.text,
        }


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Mini Org-Flask API Test Arayüzü")
    gr.Markdown(
        "Bu arayüzü kullanarak Flask API'sinin `/bookings` endpoint'ine kolayca istek gönderebilirsiniz."
    )

    gr.Markdown(get_available_services())

    with gr.Row():
        with gr.Column():
            service_ids_input = gr.Textbox(
                label="Hizmet ID'leri",
                placeholder="Lütfen yukarıdaki tablodan istediğiniz hizmetlerin ID'lerini virgülle ayırarak girin. Örn: 1, 3",
            )
            date_input = gr.Textbox(
                label="Etkinlik Tarihi",
                placeholder="Lütfen YYYY-MM-DD formatında girin. Örn: 2025-12-24",
            )
            notes_input = gr.Textbox(
                label="Notlar (İsteğe Bağlı)",
                placeholder="Rezervasyonunuzla ilgili ek notlar...",
            )
            submit_button = gr.Button("Rezervasyon Talebi Gönder", variant="primary")

        with gr.Column():
            api_response_output = gr.JSON(label="API Yanıtı")

    submit_button.click(
        fn=create_booking_request,
        inputs=[service_ids_input, date_input, notes_input],
        outputs=api_response_output,
    )

if __name__ == "__main__":
    demo.launch()
