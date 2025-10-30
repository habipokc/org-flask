import logging
import os
import sys
from logging.handlers import (
    RotatingFileHandler,
)

from flask import Flask


def create_app():
    app = Flask(__name__)

    # Flask'in varsayılan handler'ını kaldırdım  kendi ayarlarımızın geçerli olması için.
    app.logger.handlers.clear()
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Logları logs klasörüne ekle yoksa oluştur.
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        # 1 dosya max 10 kb olacak ve en fazla 10 adet dosya kayıtlı tutulacak.
        os.path.join(log_dir, "org-flask-api.log"),
        maxBytes=10240,
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Org-Flask API başlatılıyor...")
    # ----------------------------------------------------

    from .bookings import bookings_bp
    from .services import services_bp

    app.register_blueprint(services_bp)
    app.register_blueprint(bookings_bp)

    @app.route("/")
    def index():
        return "Mini Org-Flask API çalışıyor!"

    return app
