from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SelectField, TextAreaField,
    FloatField, DateField, SubmitField, IntegerField, FileField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User

# ============================================
# Autenticação
# ============================================

class LoginForm(FlaskForm):
    username = StringField('E-mail ou CPF', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(max=14)])
    full_name = StringField('Nome Completo', validators=[DataRequired(), Length(max=150)])
    user_type = SelectField('Tipo de Usuário', 
                           choices=[('farmer', 'Agricultor'), 
                                   ('technician', 'Técnico Agrícola'),
                                   ('admin', 'Administrador')])
    phone = StringField('Telefone', validators=[Length(max=20)])
    # Dados da fazenda (será criada automaticamente no cadastro)
    farm_name = StringField('Nome da Fazenda', validators=[DataRequired(), Length(max=150)])
    farm_location = StringField('Cidade/Localidade', validators=[DataRequired(), Length(max=200)])
    farm_state = SelectField('Estado',
                       choices=[('', 'Selecione...'),
                               ('AC', 'Acre'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
                               ('PA', 'Pará'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
                               ('TO', 'Tocantins'), ('MT', 'Mato Grosso'),
                               ('MA', 'Maranhão'), ('PI', 'Piauí'), ('CE', 'Ceará'),
                               ('RN', 'Rio Grande do Norte'), ('PB', 'Paraíba'),
                               ('PE', 'Pernambuco'), ('AL', 'Alagoas'), ('SE', 'Sergipe'),
                               ('BA', 'Bahia'), ('GO', 'Goiás'), ('DF', 'Distrito Federal'),
                               ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                               ('ES', 'Espírito Santo'), ('RJ', 'Rio de Janeiro'),
                               ('SP', 'São Paulo'), ('PR', 'Paraná'),
                               ('SC', 'Santa Catarina'), ('RS', 'Rio Grande do Sul')],
                       validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está cadastrado.')
    
    def validate_cpf(self, cpf):
        user = User.query.filter_by(cpf=cpf.data).first()
        if user:
            raise ValidationError('Este CPF já está cadastrado.')

# ============================================
# Fazendas
# ============================================

class FarmForm(FlaskForm):
    name = StringField('Nome da Fazenda', validators=[DataRequired(), Length(max=150)])
    location = StringField('Endereço', validators=[Length(max=200)])
    city = StringField('Cidade', validators=[Length(max=100)])
    state = SelectField('Estado',
                       choices=[('', 'Selecione...'),
                               ('AC', 'Acre'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
                               ('PA', 'Pará'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
                               ('TO', 'Tocantins'), ('MT', 'Mato Grosso'),
                               ('MA', 'Maranhão'), ('PI', 'Piauí'), ('CE', 'Ceará'),
                               ('RN', 'Rio Grande do Norte'), ('PB', 'Paraíba'),
                               ('PE', 'Pernambuco'), ('AL', 'Alagoas'), ('SE', 'Sergipe'),
                               ('BA', 'Bahia'), ('GO', 'Goiás'), ('DF', 'Distrito Federal'),
                               ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                               ('ES', 'Espírito Santo'), ('RJ', 'Rio de Janeiro'),
                               ('SP', 'São Paulo'), ('PR', 'Paraná'),
                               ('SC', 'Santa Catarina'), ('RS', 'Rio Grande do Sul')])
    size_hectares = FloatField('Tamanho (hectares)', validators=[Optional()])
    soil_type = SelectField('Tipo de Solo',
                           choices=[('', 'Selecione...'),
                                   ('clay', 'Argiloso'),
                                   ('sandy', 'Arenoso'),
                                   ('silty', 'Silte'),
                                   ('loamy', 'Franco'),
                                   ('peat', 'Terra de turfa'),
                                   ('amazon', 'Solo amazônico'),
                                   ('varzea', 'Várzea'),
                                   ('terra_preta', 'Terra Preta de Índio')])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Salvar')

# ============================================
# Culturas
# ============================================

class CropForm(FlaskForm):
    name = StringField('Nome do Plantio', validators=[DataRequired(), Length(max=100)])
    crop_type = SelectField('Tipo de Cultura', 
                           choices=[('', 'Selecione...'),
                                   ('milho', 'Milho'),
                                   ('soja', 'Soja'),
                                   ('arroz', 'Arroz'),
                                   ('trigo', 'Trigo'),
                                   ('cafe', 'Café'),
                                   ('cana', 'Cana-de-Açúcar'),
                                   ('feijao', 'Feijão'),
                                   ('mandioca', 'Mandioca'),
                                   ('outro', 'Outro')],
                           validators=[DataRequired()])
    # Dados da fazenda - somente exibição, backend usa a fazenda do usuário
    farm_name = StringField('Nome da Fazenda/Local', validators=[Optional(), Length(max=150)])
    farm_location = StringField('Localidade/Cidade', validators=[Optional(), Length(max=200)])
    farm_state = SelectField('Estado',
                       choices=[('', 'Selecione...'),
                               ('AC', 'Acre'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
                               ('PA', 'Pará'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
                               ('TO', 'Tocantins'), ('MT', 'Mato Grosso'),
                               ('MA', 'Maranhão'), ('PI', 'Piauí'), ('CE', 'Ceará'),
                               ('RN', 'Rio Grande do Norte'), ('PB', 'Paraíba'),
                               ('PE', 'Pernambuco'), ('AL', 'Alagoas'), ('SE', 'Sergipe'),
                               ('BA', 'Bahia'), ('GO', 'Goiás'), ('DF', 'Distrito Federal'),
                               ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                               ('ES', 'Espírito Santo'), ('RJ', 'Rio de Janeiro'),
                               ('SP', 'São Paulo'), ('PR', 'Paraná'),
                               ('SC', 'Santa Catarina'), ('RS', 'Rio Grande do Sul')],
                       validators=[Optional()])
    planting_date = DateField('Data do Plantio', format='%Y-%m-%d', validators=[DataRequired()])
    estimated_harvest_date = DateField('Previsão de Colheita', format='%Y-%m-%d', validators=[Optional()])
    area_hectares = FloatField('Área (hectares)', validators=[Optional()])
    expected_yield_kg = FloatField('Produção Esperada (kg)', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Length(max=500)])
    
    submit = SubmitField('Salvar Plantio')

# ============================================
# Atividades
# ============================================

class ActivityForm(FlaskForm):
    type = SelectField('Tipo de Atividade',
                      choices=[('planting', 'Plantio'),
                              ('fertilizing', 'Adubação'),
                              ('irrigation', 'Irrigação'),
                              ('pest_control', 'Controle de Pragas'),
                              ('harvest', 'Colheita'),
                              ('uv_exposure', 'Exposição UV LED'),
                              ('soil_analysis', 'Análise do Solo'),
                              ('pruning', 'Poda'),
                              ('weeding', 'Capina')])
    date = DateField('Data', validators=[DataRequired()], format='%Y-%m-%d')
    description = TextAreaField('Descrição')
    cost = FloatField('Custo (R$)', validators=[Optional()])
    duration_minutes = IntegerField('Duração (minutos)', validators=[Optional()])
    
    # Campos específicos
    water_volume_liters = FloatField('Volume de Água (litros)', validators=[Optional()])
    uv_duration_minutes = IntegerField('Duração UV (minutos)', validators=[Optional()])
    uv_intensity = FloatField('Intensidade UV (%)', validators=[Optional()])
    
    submit = SubmitField('Salvar')

# ============================================
# Sensores IoT
# ============================================

class SensorForm(FlaskForm):
    name = StringField('Nome do Sensor', validators=[DataRequired(), Length(max=100)])
    device_id = StringField('ID do Dispositivo (ESP32/Arduino)', validators=[DataRequired(), Length(max=50)])
    sensor_type = SelectField('Tipo de Sensor',
                             choices=[('soil_moisture', 'Umidade do Solo'),
                                     ('air_temperature', 'Temperatura do Ar'),
                                     ('air_humidity', 'Umidade do Ar'),
                                     ('ultrasonic_water', 'Nível de Água (Ultrassônico)'),
                                     ('flow', 'Fluxo de Água'),
                                     ('uv_sensor', 'Sensor UV'),
                                     ('rain', 'Pluviômetro'),
                                     ('wind', 'Anemômetro'),
                                     ('pressure', 'Pressão Atmosférica'),
                                     ('light', 'Luminosidade')])
    location_description = StringField('Descrição da Localização', validators=[Length(max=200)])
    sector = StringField('Setor/Área', validators=[Length(max=50)])
    farm_id = SelectField('Fazenda', coerce=int, validators=[DataRequired()])
    protocol = SelectField('Protocolo de Comunicação',
                          choices=[('LoRaWAN', 'LoRaWAN'),
                                  ('WiFi', 'WiFi'),
                                  ('Bluetooth', 'Bluetooth'),
                                  ('MQTT', 'MQTT'),
                                  ('HTTP', 'HTTP')])
    reading_interval_minutes = IntegerField('Intervalo de Leitura (minutos)', default=5)
    submit = SubmitField('Salvar')

# ============================================
# Dispositivos (Bombas, LEDs)
# ============================================

class DeviceForm(FlaskForm):
    name = StringField('Nome do Dispositivo', validators=[DataRequired(), Length(max=100)])
    device_id = StringField('ID do Dispositivo', validators=[DataRequired(), Length(max=50)])
    device_type = SelectField('Tipo de Dispositivo',
                             choices=[('water_pump', 'Bomba de Água'),
                                     ('uv_led', 'LED UV'),
                                     ('solenoid_valve', 'Válvula Solenoide'),
                                     ('fan', 'Ventilador'),
                                     ('shade', 'Controle de Sombra')])
    location = StringField('Localização', validators=[Length(max=200)])
    farm_id = SelectField('Fazenda', coerce=int, validators=[DataRequired()])
    power_watts = FloatField('Potência (Watts)', validators=[Optional()])
    submit = SubmitField('Salvar')

# ============================================
# Reservatórios
# ============================================

class WaterTankForm(FlaskForm):
    name = StringField('Nome do Reservatório', validators=[DataRequired(), Length(max=100)])
    tank_type = SelectField('Tipo',
                          choices=[('reservoir', 'Reservatório Principal'),
                                  ('irrigation_tank', 'Tanque de Irrigação'),
                                  ('river_monitoring', 'Monitoramento de Rio')])
    capacity_liters = FloatField('Capacidade (litros)', validators=[Optional()])
    height_cm = FloatField('Altura Total (cm)', validators=[Optional()])
    critical_level_percent = FloatField('Nível Crítico (%)', default=15.0)
    low_level_percent = FloatField('Nível de Alerta (%)', default=30.0)
    farm_id = SelectField('Fazenda', coerce=int, validators=[DataRequired()])
    sensor_id = SelectField('Sensor de Nível', coerce=int, validators=[Optional()])
    submit = SubmitField('Salvar')

# ============================================
# Configurações de Alertas
# ============================================

class AlertConfigForm(FlaskForm):
    # Limites de umidade do solo
    soil_moisture_critical_low = FloatField('Umidade Crítica Baixa (%)', default=20.0)
    soil_moisture_ideal_min = FloatField('Umidade Ideal Mínima (%)', default=45.0)
    soil_moisture_ideal_max = FloatField('Umidade Ideal Máxima (%)', default=70.0)
    soil_moisture_warning_high = FloatField('Umidade Alerta Alta (%)', default=85.0)
    
    # Limites de nível de água
    water_level_critical = FloatField('Nível Crítico (%)', default=15.0)
    water_level_alert = FloatField('Nível de Alerta (%)', default=30.0)
    
    # Limites de temperatura
    temperature_critical_high = FloatField('Temperatura Crítica (°C)', default=40.0)
    temperature_warning_high = FloatField('Temperatura Alerta (°C)', default=35.0)
    
    # Riscos amazônicos
    flood_risk_level_cm = FloatField('Nível de Risco de Cheia (cm)', default=300.0)
    battery_critical = FloatField('Bateria Crítica (%)', default=10.0)
    
    # Notificações
    notify_email = BooleanField('Notificar por Email', default=True)
    notify_sms = BooleanField('Notificar por SMS')
    notify_push = BooleanField('Notificações Push', default=True)
    
    # Horário silencioso
    quiet_hours_start = IntegerField('Início (hora)', default=22)
    quiet_hours_end = IntegerField('Fim (hora)', default=6)
    
    submit = SubmitField('Salvar Configurações')

# ============================================
# Consultas Técnicas
# ============================================

class ConsultationForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    question = TextAreaField('Pergunta/Descrição', validators=[DataRequired()])
    category = SelectField('Categoria',
                          choices=[('irrigation', 'Irrigação'),
                                  ('pest', 'Pragas e Doenças'),
                                  ('soil', 'Solo e Adubação'),
                                  ('climate', 'Clima e Estação'),
                                  ('harvest', 'Colheita'),
                                  ('general', 'Dúvidas Gerais')])
    priority = SelectField('Prioridade',
                          choices=[('low', 'Baixa'),
                                  ('normal', 'Normal'),
                                  ('high', 'Alta'),
                                  ('urgent', 'Urgente')],
                          default='normal')
    submit = SubmitField('Enviar Consulta')

# ============================================
# Perfil do Usuário
# ============================================

class ProfileForm(FlaskForm):
    full_name = StringField('Nome Completo', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefone', validators=[Length(max=20)])
    profile_image = FileField('Foto de Perfil')
    
    # Preferências de notificação
    alert_email = BooleanField('Receber alertas por email')
    alert_sms = BooleanField('Receber alertas por SMS')
    alert_push = BooleanField('Receber notificações push')
    
    submit = SubmitField('Salvar')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('new_password', message='As senhas não coincidem')])
    submit = SubmitField('Alterar Senha')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(max=14)])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('new_password', message='As senhas não coincidem')])
    submit = SubmitField('Redefinir Senha')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email não encontrado.')

    def validate_cpf(self, cpf):
        user = User.query.filter_by(cpf=cpf.data).first()
        if not user:
            raise ValidationError('CPF não encontrado.')

    def validate(self, extra_validators=None):
        # Chamar validação do pai
        if not super().validate(extra_validators):
            return False

        # Verificar se email e CPF pertencem ao mesmo usuário
        user = User.query.filter_by(email=self.email.data, cpf=self.cpf.data).first()
        if not user:
            self.cpf.errors.append('Email e CPF não correspondem ao mesmo usuário.')
            return False

        return True
