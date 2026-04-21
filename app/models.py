from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    password_hash = db.Column(db.String(256))
    full_name = db.Column(db.String(150))
    user_type = db.Column(db.String(20), default='farmer')  # farmer, technician, admin
    phone = db.Column(db.String(20))
    profile_image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Configurações de alerta
    alert_email = db.Column(db.Boolean, default=True)
    alert_sms = db.Column(db.Boolean, default=False)
    alert_push = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    farms = db.relationship('Farm', backref='owner', lazy=True)
    consultations = db.relationship('Consultation', backref='user', lazy=True)
    alert_configs = db.relationship('AlertConfig', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_active_sensors_count(self):
        count = 0
        for farm in self.farms:
            for sensor in farm.sensors:
                if sensor.is_active:
                    count += 1
        return count
    
    def get_unread_alerts_count(self):
        from app.models import Alert, Farm
        return Alert.query.join(Farm).filter(
            Farm.user_id == self.id,
            Alert.is_read == False,
            Alert.is_resolved == False
        ).count()
    
    def __repr__(self):
        return f'<User {self.username}>'

class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    size_hectares = db.Column(db.Float)
    soil_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Coordenadas geográficas
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    crops = db.relationship('Crop', backref='farm', lazy=True)
    sensors = db.relationship('Sensor', backref='farm', lazy=True)
    water_tanks = db.relationship('WaterTank', backref='farm', lazy=True)
    alerts = db.relationship('Alert', backref='farm', lazy=True)
    devices = db.relationship('Device', backref='farm', lazy=True)
    daily_summaries = db.relationship('DailySummary', backref='farm', lazy=True)
    
    def __repr__(self):
        return f'<Farm {self.name}>'

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(50))  # milho, soja, arroz, etc.
    variety = db.Column(db.String(100))
    planting_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    estimated_harvest_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='planted')  # planted, growing, harvested
    area_hectares = db.Column(db.Float)
    expected_yield = db.Column(db.Float)
    notes = db.Column(db.Text)
    
    # Irrigação
    irrigation_count = db.Column(db.Integer, default=0)
    last_irrigation_date = db.Column(db.DateTime)
    needs_irrigation = db.Column(db.Boolean, default=False)
    next_irrigation_date = db.Column(db.DateTime)
    
    # Controle de dispositivos
    led_status = db.Column(db.Boolean, default=False)
    pump_status = db.Column(db.Boolean, default=False)
    
    # Necessidades específicas
    ideal_soil_moisture_min = db.Column(db.Float, default=45.0)
    ideal_soil_moisture_max = db.Column(db.Float, default=70.0)
    ideal_temperature_min = db.Column(db.Float, default=20.0)
    ideal_temperature_max = db.Column(db.Float, default=30.0)
    
    # Chave estrangeira
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    
    # Relacionamentos
    activities = db.relationship('Activity', backref='crop', lazy=True)
    sensor_zones = db.relationship('SensorZone', backref='crop', lazy=True)
    
    def __repr__(self):
        return f'<Crop {self.name}>'
    
    def get_progress(self):
        """Calcula o progresso do cultivo em porcentagem"""
        from datetime import date
        if not self.planting_date:
            return 0
        if not self.estimated_harvest_date:
            return 50  # Default se não tiver data de colheita
        
        today = date.today()
        total_days = (self.estimated_harvest_date - self.planting_date).days
        if total_days <= 0:
            return 100
        
        days_elapsed = (today - self.planting_date).days
        if days_elapsed <= 0:
            return 0
        if days_elapsed >= total_days:
            return 100
        
        return min(100, int((days_elapsed / total_days) * 100))
    
    def irrigate(self):
        """Registra uma irrigação"""
        from datetime import datetime
        self.irrigation_count += 1
        self.last_irrigation_date = datetime.utcnow()
        self.needs_irrigation = False
        # Próxima irrigação em 3 dias (ajustável)
        from datetime import timedelta
        self.next_irrigation_date = datetime.utcnow() + timedelta(days=3)
        return self.irrigation_count
    
    def toggle_led(self):
        """Alterna estado do LED"""
        self.led_status = not self.led_status
        return self.led_status
    
    def toggle_pump(self):
        """Alterna estado da bomba"""
        self.pump_status = not self.pump_status
        return self.pump_status

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # planting, fertilizing, irrigation, pest_control, harvest, uv_exposure
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    cost = db.Column(db.Float)
    duration_minutes = db.Column(db.Integer)
    
    # Para irrigação
    water_volume_liters = db.Column(db.Float)
    
    # Para UV LED
    uv_duration_minutes = db.Column(db.Integer)
    uv_intensity = db.Column(db.Float)
    
    # Chave estrangeira
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    
    def __repr__(self):
        return f'<Activity {self.type}>'

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_id = db.Column(db.String(50), unique=True, nullable=False)  # ESP32/Arduino ID
    sensor_type = db.Column(db.String(50), nullable=False)  # soil_moisture, air_temperature, air_humidity, ultrasonic_water, flow, uv_sensor
    location_description = db.Column(db.String(200))
    sector = db.Column(db.String(50))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_reading_at = db.Column(db.DateTime)
    battery_level = db.Column(db.Float)  # Percentual 0-100
    signal_strength = db.Column(db.Float)  # dBm
    
    # Firmware
    firmware_version = db.Column(db.String(20))
    protocol = db.Column(db.String(20), default='LoRaWAN')  # LoRaWAN, WiFi, Bluetooth
    mac_address = db.Column(db.String(17))
    
    # Configurações
    reading_interval_minutes = db.Column(db.Integer, default=5)
    
    # Chave estrangeira
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    
    # Relacionamentos
    readings = db.relationship('SensorReading', backref='sensor', lazy=True, order_by='SensorReading.timestamp.desc()')
    
    def get_latest_reading(self):
        return SensorReading.query.filter_by(sensor_id=self.id).order_by(SensorReading.timestamp.desc()).first()
    
    def __repr__(self):
        return f'<Sensor {self.device_id}>'

class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Valores do sensor
    value = db.Column(db.Float, nullable=False)
    value_secondary = db.Column(db.Float)  # Para sensores com 2 valores (ex: temp e umidade)
    unit = db.Column(db.String(20))  # %, C, cm, L, etc.
    
    # Qualidade do dado
    is_valid = db.Column(db.Boolean, default=True)
    error_code = db.Column(db.String(20))
    
    # Chave estrangeira
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    
    def __repr__(self):
        return f'<SensorReading {self.sensor_id} {self.timestamp}>'

class WaterTank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tank_type = db.Column(db.String(50))  # reservoir, irrigation_tank, river_monitoring
    capacity_liters = db.Column(db.Float)
    height_cm = db.Column(db.Float)
    
    # Níveis de alerta
    critical_level_percent = db.Column(db.Float, default=15.0)
    low_level_percent = db.Column(db.Float, default=30.0)
    
    # Sensor associado (ultrassônico)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    
    # Chave estrangeira
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    
    # Relacionamentos
    sensor = db.relationship('Sensor', foreign_keys=[sensor_id])
    
    def get_current_level(self):
        if self.sensor:
            latest = SensorReading.query.filter_by(sensor_id=self.sensor.id).order_by(SensorReading.timestamp.desc()).first()
            if latest:
                # Converte distância em % de volume
                distance_cm = latest.value
                fill_percent = ((self.height_cm - distance_cm) / self.height_cm) * 100
                return max(0, min(100, fill_percent))
        return None
    
    def __repr__(self):
        return f'<WaterTank {self.name}>'

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_id = db.Column(db.String(50), unique=True, nullable=False)
    device_type = db.Column(db.String(50), nullable=False)  # water_pump, uv_led, solenoid_valve
    location = db.Column(db.String(200))
    
    # Status
    is_online = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    last_activated_at = db.Column(db.DateTime)
    total_runtime_hours = db.Column(db.Float, default=0.0)
    
    # Controle
    can_remote_control = db.Column(db.Boolean, default=True)
    auto_mode = db.Column(db.Boolean, default=False)
    
    # Configurações
    power_watts = db.Column(db.Float)
    
    # Chave estrangeira
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'))
    
    # Relacionamentos
    operations = db.relationship('DeviceOperation', backref='device', lazy=True)
    
    def __repr__(self):
        return f'<Device {self.device_id}>'

class DeviceOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(50), nullable=False)  # on, off, auto_start, manual_override
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration_minutes = db.Column(db.Integer)
    triggered_by = db.Column(db.String(50))  # user, automation, schedule, alert
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Dados da operação
    water_volume_liters = db.Column(db.Float)
    energy_consumed_kwh = db.Column(db.Float)
    
    # Chave estrangeira
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    
    def __repr__(self):
        return f'<DeviceOperation {self.device_id} {self.operation_type}>'

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # critical, warning, info, success
    category = db.Column(db.String(50))  # flood_risk, drought_risk, soil_moisture, temperature, device_offline, battery_low
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Dados relacionados
    sensor_value = db.Column(db.Float)
    threshold_value = db.Column(db.Float)
    
    # Ações recomendadas
    recommended_action = db.Column(db.Text)
    action_taken = db.Column(db.Text)
    
    # Chaves estrangeiras
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    
    def __repr__(self):
        return f'<Alert {self.title}>'

class AlertConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Limites para alertas
    soil_moisture_critical_low = db.Column(db.Float, default=20.0)
    soil_moisture_ideal_min = db.Column(db.Float, default=45.0)
    soil_moisture_ideal_max = db.Column(db.Float, default=70.0)
    soil_moisture_warning_high = db.Column(db.Float, default=85.0)
    
    water_level_critical = db.Column(db.Float, default=15.0)
    water_level_alert = db.Column(db.Float, default=30.0)
    
    temperature_critical_high = db.Column(db.Float, default=40.0)
    temperature_warning_high = db.Column(db.Float, default=35.0)
    
    flood_risk_level_cm = db.Column(db.Float, default=300.0)  # Nível do rio em cm
    
    battery_critical = db.Column(db.Float, default=10.0)
    
    # Notificações
    notify_email = db.Column(db.Boolean, default=True)
    notify_sms = db.Column(db.Boolean, default=False)
    notify_push = db.Column(db.Boolean, default=True)
    
    # Horário para alertas automáticos (evitar notificações à noite)
    quiet_hours_start = db.Column(db.Integer, default=22)
    quiet_hours_end = db.Column(db.Integer, default=6)
    
    # Chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<AlertConfig user={self.user_id}>'

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, answered, closed
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    answered_at = db.Column(db.DateTime)
    
    # Tipo de consulta
    category = db.Column(db.String(50))  # irrigation, pest, soil, climate, harvest, general
    
    # Chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Consultation {self.title}>'

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Dados meteorológicos
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    precipitation_probability = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    pressure = db.Column(db.Float)
    uv_index = db.Column(db.Float)
    weather_condition = db.Column(db.String(50))
    
    # Dados específicos da Amazônia
    river_level = db.Column(db.Float)  # Nível do rio em cm
    drought_alert = db.Column(db.Boolean, default=False)
    flood_alert = db.Column(db.Boolean, default=False)
    
    # Fonte dos dados
    data_source = db.Column(db.String(50), default='API')  # API, sensor, prediction
    
    def __repr__(self):
        return f'<WeatherData {self.location} {self.date}>'

class SensorZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    sector = db.Column(db.String(50))
    
    # Chaves estrangeiras
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    
    # Relacionamentos
    sensor = db.relationship('Sensor')
    
    def __repr__(self):
        return f'<SensorZone {self.name}>'

class DailySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    
    # Médias do dia
    avg_soil_moisture = db.Column(db.Float)
    avg_temperature = db.Column(db.Float)
    avg_humidity = db.Column(db.Float)
    avg_water_level = db.Column(db.Float)
    
    # Totais
    total_irrigation_liters = db.Column(db.Float)
    total_uv_hours = db.Column(db.Float)
    
    # Eficiência
    irrigation_efficiency = db.Column(db.Float)
    water_saved_percent = db.Column(db.Float)
    
    # Alertas
    alerts_count = db.Column(db.Integer, default=0)
    critical_alerts = db.Column(db.Integer, default=0)
    
    # Resumo gerado
    summary_text = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    
    def __repr__(self):
        return f'<DailySummary {self.date} farm={self.farm_id}>'

class FireReport(db.Model):
    """Reportes de queimada enviados por usuários"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255))
    status = db.Column(db.String(20), default='alerta')  # alerta, suspeito, confirmado
    vote_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='fire_reports')
    
    def __repr__(self):
        return f'<FireReport {self.id} lat={self.lat} lon={self.lon}>'

class Conversation(db.Model):
    """Histórico de conversas do chatbot por plantio"""
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # 'user' ou 'assistant'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    crop = db.relationship('Crop', backref=db.backref('conversations', lazy='dynamic', order_by='Conversation.timestamp.asc()'))
    
    def __repr__(self):
        return f'<Conversation {self.role} crop={self.crop_id}>'
