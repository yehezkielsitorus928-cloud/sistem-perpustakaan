from flask import Flask
from database.config import Config
from database.models import db
from backend.main_routes import main_bp

def create_app():
    # Menunjuk langsung ke folder frontend untuk templates dan static
    app = Flask(__name__, 
                template_folder='frontend/templates', 
                static_folder='frontend/static')
    
    app.config.from_object(Config)

    # TAMBAHKAN BARIS INI:
    app.config['SECRET_KEY'] = 'kunci-rahasia-super-aman-bebas'

    # Inisialisasi database
    db.init_app(app)

    # Daftarkan Blueprint backend rute
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)