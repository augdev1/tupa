from app import create_app, db
from app.models import User, Farm, Crop, Activity, Alert, AlertConfig, Sensor, SensorReading, WaterTank, Device, DeviceOperation, WeatherData, Consultation, SensorZone, DailySummary, Conversation, FireReport

app = create_app()

with app.app_context():
    # Criar todas as tabelas
    db.create_all()
    print("✅ Banco de dados criado com sucesso!")
    print("\nTabelas criadas:")
    for table in db.metadata.tables.keys():
        print(f"  - {table}")
