from app import app, db  # Importa la app y db desde tu archivo principal

# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente")