from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
import requests
import logging
import base64
import os
from app import db
from app.models import (
    User, Farm, Crop, Activity, Consultation, WeatherData,
    Sensor, SensorReading, WaterTank, Device, DeviceOperation,
    Alert, AlertConfig, DailySummary, Conversation, FireReport
)
from app.forms import (
    LoginForm, RegistrationForm, FarmForm, CropForm, ActivityForm,
    ConsultationForm, SensorForm, DeviceForm, AlertConfigForm,
    ProfileForm, WaterTankForm, ChangePasswordForm, ResetPasswordForm
)

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

# ANHANGÁ configuration
ANHANGA_URL = os.getenv('ANHANGA_URL', 'http://localhost:5000')

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista em memória para notificações externas do ANHANGÁ
anhanga_notifications = []

# ============================================
# Página Inicial / Landing
# ============================================

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

# ============================================
# Autenticação
# ============================================

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Aceitar username ou CPF
        user = User.query.filter(
            (User.username == form.username.data) | 
            (User.cpf == form.username.data)
        ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Criar configuração de alertas se não existir
            if not AlertConfig.query.filter_by(user_id=user.id).first():
                alert_config = AlertConfig(user_id=user.id)
                db.session.add(alert_config)
                db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Usuário ou senha inválidos', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema', 'info')
    return redirect(url_for('main.index'))

@main.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Buscar usuário por email e CPF
        user = User.query.filter_by(email=form.email.data, cpf=form.cpf.data).first()
        if user:
            # Redefinir senha
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Senha redefinida com sucesso! Faça login com sua nova senha.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Email e CPF não correspondem ao mesmo usuário.', 'danger')
    return render_template('reset_password.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Criar usuário
            user = User(
                username=form.username.data,
                email=form.email.data,
                cpf=form.cpf.data,
                full_name=form.full_name.data,
                user_type=form.user_type.data,
                phone=form.phone.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()  # Para obter o user.id
            
            # Criar fazenda do usuário
            farm = Farm(
                name=form.farm_name.data,
                location=form.farm_location.data,
                city=form.farm_location.data,
                state=form.farm_state.data,
                user_id=user.id
            )
            db.session.add(farm)
            
            # Criar configuração de alertas
            alert_config = AlertConfig(user_id=user.id)
            db.session.add(alert_config)
            
            db.session.commit()
            flash(f'Cadastro realizado com sucesso! Fazenda "{farm.name}" criada.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
    else:
        # Mostrar erros do formulário
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'warning')
    return render_template('register.html', form=form)

# ============================================
# Dashboard - Visão Geral
# ============================================

@main.route('/dashboard')
@login_required
def dashboard():
    from datetime import date
    import os
    import requests
    
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    farm_ids = [f.id for f in farms]
    
    # Buscar todos os plantios do usuário
    crops = Crop.query.filter(Crop.farm_id.in_(farm_ids)).all()
    
    # Dados do monitoramento em tempo real
    sensors_online = 0
    sensors_offline = 0
    for farm in farms:
        for sensor in farm.sensors:
            if sensor.is_active:
                sensors_online += 1
            else:
                sensors_offline += 1
    
    # Alertas não lidos
    unread_alerts = Alert.query.join(Farm).filter(
        Farm.user_id == current_user.id,
        Alert.is_read == False
    ).count()
    
    # Resumo diário do último dia
    latest_summary = DailySummary.query.join(Farm).filter(
        Farm.user_id == current_user.id
    ).order_by(DailySummary.date.desc()).first()
    
    # Buscar notícias de agricultura via API
    news = []
    try:
        news_api_key = os.environ.get('NEWS_API_KEY')
        if news_api_key:
            response = requests.get(
                f'https://newsapi.org/v2/everything',
                params={
                    'q': 'agricultura OR agricultor OR plantio OR colheita',
                    'language': 'pt',
                    'sortBy': 'publishedAt',
                    'pageSize': 10,
                    'apiKey': news_api_key
                },
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                news = data.get('articles', [])
    except Exception as e:
        print(f'Erro ao buscar notícias: {e}')
    
    # Se não conseguir notícias da API, usar notícias fictícias
    if not news:
        news = [
            {
                'title': 'Tecnologia agrícola impulsiona produtividade no Brasil',
                'description': 'Novas tecnologias e técnicas de cultivo estão aumentando a produção de grãos no país.',
                'url': '#',
                'urlToImage': None,
                'publishedAt': '2024-01-15T10:00:00Z',
                'source': {'name': 'AgroNews'}
            },
            {
                'title': 'Previsão de chuva otimista para região agrícola',
                'description': 'Meteorologistas preveem chuvas regulares nos próximos meses, beneficiando as plantações.',
                'url': '#',
                'urlToImage': None,
                'publishedAt': '2024-01-14T15:30:00Z',
                'source': {'name': 'Clima Rural'}
            },
            {
                'title': 'Sustentabilidade no campo ganha força',
                'description': 'Produtores adotam práticas sustentáveis para reduzir impacto ambiental.',
                'url': '#',
                'urlToImage': None,
                'publishedAt': '2024-01-13T09:00:00Z',
                'source': {'name': 'AgroSustentável'}
            }
        ]
    
    return render_template('dashboard.html', 
                         farms=farms,
                         crops=crops,
                         sensors_online=sensors_online,
                         sensors_offline=sensors_offline,
                         unread_alerts=unread_alerts,
                         summary=latest_summary,
                         news=news,
                         now=date.today())

# ============================================
# Monitor - Dados em Tempo Real
# ============================================

@main.route('/monitor')
@login_required
def monitor():
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    
    # Coletar todos os sensores ativos
    all_sensors = []
    for farm in farms:
        for sensor in farm.sensors:
            latest_reading = sensor.get_latest_reading()
            all_sensors.append({
                'sensor': sensor,
                'reading': latest_reading,
                'farm': farm
            })
    
    # Coletar dispositivos
    devices = []
    for farm in farms:
        for device in farm.devices:
            devices.append({
                'device': device,
                'farm': farm
            })
    
    # Reservatórios
    tanks = []
    for farm in farms:
        for tank in farm.water_tanks:
            tanks.append({
                'tank': tank,
                'level': tank.get_current_level(),
                'farm': farm
            })
    
    # Buscar dados do tempo usando helper function
    weather_data = get_weather_data()
    
    return render_template('monitor.html',
                         sensors=all_sensors,
                         devices=devices,
                         tanks=tanks,
                         weather_data=weather_data)

@main.route('/sensor/<int:sensor_id>')
@login_required
def sensor_detail(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    # Verificar se o sensor pertence ao usuário
    if sensor.farm.user_id != current_user.id:
        flash('Acesso negado', 'danger')
        return redirect(url_for('main.monitor'))
    
    # Histórico das últimas 24 horas
    since = datetime.utcnow() - timedelta(hours=24)
    readings = SensorReading.query.filter(
        SensorReading.sensor_id == sensor_id,
        SensorReading.timestamp >= since
    ).order_by(SensorReading.timestamp.desc()).all()
    
    return render_template('sensor_detail.html', sensor=sensor, readings=readings)

# ============================================
# Plantios
# ============================================

@main.route('/plantios/<int:crop_id>')
@login_required
def plantio_details(crop_id):
    from datetime import date
    crop = Crop.query.get_or_404(crop_id)
    # Verificar se pertence ao usuário
    if crop.farm.user_id != current_user.id:
        flash('Acesso negado', 'danger')
        return redirect(url_for('main.plantios'))
    
    progress = crop.get_progress()
    
    # Buscar histórico de conversas
    conversations = Conversation.query.filter_by(crop_id=crop_id).order_by(Conversation.timestamp.asc()).all()
    
    return render_template('plantios_detail.html', crop=crop, progress=progress, now=date.today(), conversations=conversations)

@main.route('/plantios/<int:crop_id>/delete', methods=['POST'])
@login_required
def delete_plantio(crop_id):
    """Excluir plantio"""
    crop = Crop.query.get_or_404(crop_id)
    # Verificar se pertence ao usuário
    if crop.farm.user_id != current_user.id:
        flash('Acesso negado', 'danger')
        return redirect(url_for('main.plantios'))
    
    crop_name = crop.name
    db.session.delete(crop)
    db.session.commit()
    flash(f'Plantio "{crop_name}" excluído com sucesso!', 'success')
    return redirect(url_for('main.plantios'))

@main.route('/plantios/<int:crop_id>/irrigate', methods=['POST'])
@login_required
def irrigate_plantio(crop_id):
    """Registrar irrigação no plantio"""
    crop = Crop.query.get_or_404(crop_id)
    if crop.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    count = crop.irrigate()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'irrigation_count': count,
        'last_irrigation': crop.last_irrigation_date.strftime('%d/%m/%Y %H:%M') if crop.last_irrigation_date else None,
        'next_irrigation': crop.next_irrigation_date.strftime('%d/%m/%Y %H:%M') if crop.next_irrigation_date else None
    })

@main.route('/plantios/<int:crop_id>/toggle-led', methods=['POST'])
@login_required
def toggle_led(crop_id):
    """Alternar estado do LED"""
    crop = Crop.query.get_or_404(crop_id)
    if crop.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    new_status = crop.toggle_led()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'led_status': new_status
    })

@main.route('/plantios/<int:crop_id>/toggle-pump', methods=['POST'])
@login_required
def toggle_pump(crop_id):
    """Alternar estado da bomba"""
    crop = Crop.query.get_or_404(crop_id)
    if crop.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    new_status = crop.toggle_pump()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'pump_status': new_status
    })

@main.route('/plantios/<int:crop_id>/chat', methods=['POST'])
@login_required
def chat_with_plantio(crop_id):
    """Chatbot com Groq especializado na cultura específica do plantio"""
    import os
    from groq import Groq
    
    crop = Crop.query.get_or_404(crop_id)
    if crop.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Mensagem vazia'}), 400
    
    # Salvar mensagem do usuário
    user_conv = Conversation(crop_id=crop_id, role='user', message=user_message)
    db.session.add(user_conv)
    db.session.commit()
    
    # Buscar histórico de conversas
    conversations = Conversation.query.filter_by(crop_id=crop_id).order_by(Conversation.timestamp).all()
    
    # Preparar contexto do plantio com especialização na cultura
    crop_type = crop.crop_type.lower() if crop.crop_type else 'cultura'
    culture_name = crop.crop_type.capitalize() if crop.crop_type else 'Cultura'
    
    # Especialistas por cultura
    specialist_contexts = {
        'café': f"""Você é um agrônomo especialista em CAFÉ com 20 anos de experiência no cultivo de café arábica e canéfora no Brasil.
Você é especialista em manejo de solos para café, nutrição, controle de pragas (bicho-mineiro, broca-do-café), doenças (ferrugem, cercospora), e colheita.
Conhece profundamente as necessidades hídricas, pH ideal (5.0-5.5), épocas de adubação, e práticas de sustentabilidade para cafeicultura.""",
        'milho': f"""Você é um agrônomo especialista em MILHO com 20 anos de experiência no cultivo de milho no Brasil.
Você é especialista em híbridos, manejo de pragas (lagarta-do-cartucho, percevejo), doenças (ferrugem comum, griselada), e épocas de plantio/safra.
Conhece profundamente as necessidades nutricionais, densidade de semeadura, irrigação por aspersão/gotejamento, e manejo de pós-colheita.""",
        'soja': f"""Você é um agrônomo especialista em SOJA com 20 anos de experiência no cultivo de soja no Brasil.
Você é especialista em fixação biológica de nitrogênio, cultivares, manejo de pragas (percevejo, lagarta), doenças (ferrugem asiática, mofo-branco), e rotação de culturas.
Conhece profundamente as necessidades de luz, temperatura, umidade, e práticas de manejo integrado para sojicultura.""",
        'arroz': f"""Você é um agrônomo especialista em ARROZ com 20 anos de experiência no cultivo de arroz no Brasil.
Você é especialista em sistemas irrigados e de terras altas, manejo de água, pragas (bicheira-da-raiz, percevejo-do-grão), e doenças (brusone, mancha-parda).
Conhece profundamente as necessidades de inundação, adubação nitrogenada, e práticas de colheita e armazenamento de arroz.""",
    }
    
    specialist_prompt = specialist_contexts.get(crop_type, f"""Você é um agrônomo especialista em {culture_name} com 20 anos de experiência no cultivo de {culture_name} no Brasil.
Você é especialista em manejo de solos, nutrição, controle de pragas e doenças específicas de {culture_name}, irrigação e colheita.
Conhece profundamente as necessidades específicas dessa cultura e as melhores práticas agrícolas.""")
    
    context = f"""{specialist_prompt}

DADOS ATUAIS DO PLANTIO DE {culture_name.upper()}:
- Nome do plantio: {crop.name}
- Tipo de cultura: {crop.crop_type}
- Data de plantio: {crop.planting_date.strftime('%d/%m/%Y') if crop.planting_date else 'Não informado'}
- Previsão de colheita: {crop.estimated_harvest_date.strftime('%d/%m/%Y') if crop.estimated_harvest_date else 'Não informado'}
- Área: {crop.area_hectares or 0} hectares
- Produção esperada: {crop.expected_yield or 0} kg
- Irrigações realizadas: {crop.irrigation_count}
- Última irrigação: {crop.last_irrigation_date.strftime('%d/%m/%Y %H:%M') if crop.last_irrigation_date else 'Nunca'}
- Precisa irrigar: {'Sim' if crop.needs_irrigation else 'Não'}
- Progresso atual: {crop.get_progress()}%
- Localização: {crop.farm.name if crop.farm else 'Não informado'}

INSTRUÇÕES:
- Responda como um especialista em {culture_name}
- Dê dicas específicas para essa cultura
- Considere o progresso atual do plantio ({crop.get_progress()}%)
- Seja prático e direto, focado em agricultura brasileira
- Quando sugerir algo, explique por que é importante para {culture_name}
- Use linguagem técnica mas acessível para agricultores"""
    
    messages = [{'role': 'system', 'content': context}]
    
    # Adicionar histórico (últimas 10 mensagens)
    for conv in conversations[-10:]:
        messages.append({'role': conv.role, 'content': conv.message})
    
    try:
        groq_api_key = os.environ.get('GROQ_API_KEY')
        if not groq_api_key:
            ai_response = f"Desculpe, o serviço de IA não está configurado. Mas posso te ajudar com informações básicas sobre {culture_name}: acompanhe a umidade do solo e regue quando necessário. Para {crop_type}, mantenha o pH entre 5.0 e 6.0."
        else:
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )
            
            ai_response = completion.choices[0].message.content.strip()
    except Exception as e:
        ai_response = f"Erro ao consultar a IA: {str(e)}"
    
    # Salvar resposta da IA
    ai_conv = Conversation(crop_id=crop_id, role='assistant', message=ai_response)
    db.session.add(ai_conv)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'response': ai_response,
        'timestamp': ai_conv.timestamp.isoformat()
    })

# ============================================
# Helper Functions
# ============================================

def get_weather_data():
    """Busca dados do tempo para Manaus, AM com dados históricos"""
    import requests
    from datetime import datetime, timedelta
    
    weather_data = None
    try:
        # Usar Open-Meteo API (gratuita, sem necessidade de API key)
        weather_response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': -3.1190,  # Manaus
                'longitude': -60.0217,
                'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,surface_pressure',
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code',
                'timezone': 'America/Manaus',
                'forecast_days': 7
            },
            timeout=10
        )
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
    except Exception as e:
        print(f'Erro ao buscar dados do tempo: {e}')
    
    return weather_data

# ============================================
# Alertas
# ============================================

@main.route('/alerts')
@login_required
def alerts():
    """Lista de alertas com integração de APIs"""
    import os
    
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    farm_ids = [f.id for f in farms]
    
    # Alertas ativos (não resolvidos)
    active_alerts = Alert.query.filter(
        Alert.farm_id.in_(farm_ids),
        Alert.is_resolved == False
    ).order_by(Alert.created_at.desc()).all()
    
    # Histórico de alertas resolvidos (sinistros)
    resolved_alerts = Alert.query.filter(
        Alert.farm_id.in_(farm_ids),
        Alert.is_resolved == True
    ).order_by(Alert.resolved_at.desc()).limit(20).all()
    
    # Buscar dados do tempo usando helper function
    weather_data = get_weather_data()
    
    rain_forecast = None
    if weather_data:
        # Verificar se vai chover nos próximos 3 dias
        precipitation_data = weather_data.get('daily', {}).get('precipitation_sum', [])
        rain_forecast = any(precip > 10 for precip in precipitation_data[:3])
    
    # Buscar nível do Rio Negro (ANA - Agência Nacional de Águas)
    river_level = None
    river_average = None
    try:
        # API do HIDROWEB (ANA) para dados do Rio Negro em Manaus
        river_response = requests.get(
            'https://snirh.snirh.gov.br/snirh/api/v1/telemetria/estacoes',
            params={
                'codigo': '14020000',  # Estação do Rio Negro em Manaus
                'tipoDados': 'NIVEL'
            },
            timeout=10
        )
        if river_response.status_code == 200:
            river_data = river_response.json()
            if river_data and len(river_data) > 0:
                river_level = river_data[0].get('valor')
    except Exception as e:
        print(f'Erro ao buscar nível do rio: {e}')
    
    # Se não conseguir dados da ANA, usar valores fictícios baseados em médias históricas
    if not river_level:
        river_level = 18.5  # Nível médio do Rio Negro (metros)
        river_average = 18.0  # Média histórica anual
    
    return render_template('alerts.html',
                         active_alerts=active_alerts,
                         resolved_alerts=resolved_alerts,
                         weather_data=weather_data,
                         rain_forecast=rain_forecast,
                         river_level=river_level,
                         river_average=river_average)

@main.route('/alerts/<int:alert_id>/resolve', methods=['POST'])
@login_required
def resolve_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    if alert.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    alert.is_resolved = True
    alert.resolved_at = datetime.utcnow()
    alert.action_taken = request.form.get('action_taken', 'Resolvido pelo usuário')
    db.session.commit()
    
    flash('Alerta marcado como resolvido', 'success')
    return redirect(url_for('main.alerts'))

@main.route('/alerts/config', methods=['GET', 'POST'])
@login_required
def alert_config():
    config = AlertConfig.query.filter_by(user_id=current_user.id).first()
    if not config:
        config = AlertConfig(user_id=current_user.id)
        db.session.add(config)
        db.session.commit()
    
    form = AlertConfigForm(obj=config)
    if form.validate_on_submit():
        form.populate_obj(config)
        db.session.commit()
        flash('Configurações de alertas salvas com sucesso!', 'success')
        return redirect(url_for('main.alerts'))
    
    return render_template('alert_config.html', form=form)

# ============================================
# Histórico de Dados
# ============================================

@main.route('/historic')
@login_required
def historic():
    from datetime import date
    import os
    import requests
    
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    farm_ids = [f.id for f in farms]
    
    # Buscar todos os plantios do usuário
    crops = Crop.query.filter(Crop.farm_id.in_(farm_ids)).all()
    
    # Buscar todos os sensores do usuário
    sensors = Sensor.query.filter(Sensor.farm_id.in_(farm_ids)).all()
    
    # Buscar notícias de agricultura via API
    news = []
    try:
        news_api_key = os.environ.get('NEWS_API_KEY')
        if news_api_key:
            response = requests.get(
                f'https://newsapi.org/v2/everything',
                params={
                    'q': 'agricultura OR agricultor OR plantio OR colheita',
                    'language': 'pt',
                    'sortBy': 'publishedAt',
                    'pageSize': 10,
                    'apiKey': news_api_key
                },
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                news = data.get('articles', [])
    except Exception as e:
        print(f'Erro ao buscar notícias: {e}')
    
    # Se não conseguir notícias da API, usar notícias fictícias
    if not news:
        news = [
            {
                'title': 'Tecnologia agrícola impulsiona produtividade no Brasil',
                'description': 'Novas tecnologias e técnicas de cultivo estão aumentando a produção de grãos no país.',
                'url': '#',
                'urlToImage': None,
                'publishedAt': '2024-01-15T10:00:00Z',
                'source': {'name': 'AgroNews'}
            },
            {
                'title': 'Previsão de chuva otimista para região agrícola',
                'description': 'Meteorologistas preveem chuvas regulares nos próximos meses, beneficiando as plantações.',
                'url': '#',
                'urlToImage': None,
                'publishedAt': '2024-01-14T15:30:00Z',
                'source': {'name': 'Clima Rural'}
            },
            {
                'title': 'Sustentabilidade no campo ganha força',
                'description': 'Produtores adotam práticas sustentáveis para reduzir impacto ambiental.',
                'url': '#',
                'urlToImage': None,
                'publishedAt': '2024-01-13T09:00:00Z',
                'source': {'name': 'AgroSustentável'}
            }
        ]
    
    # Período selecionado (padrão: últimos 7 dias)
    period = request.args.get('period', 'week')
    if period == 'day':
        since = datetime.utcnow() - timedelta(days=1)
    elif period == 'week':
        since = datetime.utcnow() - timedelta(days=7)
    elif period == 'month':
        since = datetime.utcnow() - timedelta(days=30)
    else:
        since = datetime.utcnow() - timedelta(days=7)
    
    # Resumos diários
    summaries = DailySummary.query.filter(
        DailySummary.farm_id.in_(farm_ids),
        DailySummary.date >= since.date()
    ).order_by(DailySummary.date.desc()).all()
    
    # Médias calculadas
    avg_soil_moisture = db.session.query(func.avg(DailySummary.avg_soil_moisture)).filter(
        DailySummary.farm_id.in_(farm_ids),
        DailySummary.date >= since.date()
    ).scalar() or 0
    
    avg_temperature = db.session.query(func.avg(DailySummary.avg_temperature)).filter(
        DailySummary.farm_id.in_(farm_ids),
        DailySummary.date >= since.date()
    ).scalar() or 0
    
    return render_template('historic.html',
                         farms=farms,
                         crops=crops,
                         sensors=sensors,
                         news=news,
                         summaries=summaries,
                         period=period,
                         avg_soil_moisture=avg_soil_moisture,
                         avg_temperature=avg_temperature,
                         now=date.today())

# ============================================
# Perfil do Usuário
# ============================================

@main.route('/profile')
@login_required
def profile():
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    
    # Estatísticas
    total_sensors = sum(len(f.sensors) for f in farms)
    total_crops = sum(len(f.crops) for f in farms)
    
    return render_template('profile.html',
                         user=current_user,
                         farms_count=len(farms),
                         sensors_count=total_sensors,
                         crops_count=total_crops)

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Handle profile image upload
        if form.profile_image.data:
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'profile_images')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(form.profile_image.data.filename)
            unique_filename = f"{current_user.id}_{filename}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Save file
            form.profile_image.data.save(file_path)
            
            # Store relative path in database
            current_user.profile_image = f"/static/uploads/profile_images/{unique_filename}"
        
        # Populate other fields (excluding profile_image which we already handled)
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.alert_email = form.alert_email.data
        current_user.alert_sms = form.alert_sms.data
        current_user.alert_push = form.alert_push.data
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile_edit.html', form=form)

@main.route('/change-password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return jsonify({'success': True, 'message': 'Senha alterada com sucesso!'})
        else:
            return jsonify({'success': False, 'message': 'Senha atual incorreta!'})
    return jsonify({'success': False, 'message': 'Por favor, corrija os erros no formulário.'})

@main.route('/reportar-queimada', methods=['GET', 'POST'])
def reportar_queimada():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'Nenhum arquivo enviado'}), 400

            file = request.files['file']
            lat = request.form.get('lat', type=float)
            lon = request.form.get('lon', type=float)

            if not file or not lat or not lon:
                return jsonify({'error': 'Dados incompletos'}), 400

            # Save image
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app

            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'fire_reports')
            os.makedirs(upload_dir, exist_ok=True)

            filename = secure_filename(file.filename)
            user_id = current_user.id if current_user.is_authenticated else 'anonymous'
            unique_filename = f"{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)

            image_path = f"/static/uploads/fire_reports/{unique_filename}"

            # Create new report
            new_report = FireReport(
                user_id=current_user.id if current_user.is_authenticated else None,
                lat=lat,
                lon=lon,
                image_path=image_path,
                status='enviado'
            )

            db.session.add(new_report)
            db.session.commit()

            # Enviar para ANHANGÁ
            enviar_reporte_anhanga(
                tipo='queimada',
                latitude=lat,
                longitude=lon,
                imagem_path=image_path,
                username=current_user.username if current_user.is_authenticated else None
            )

            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return render_template('reportar_queimada.html')

@main.route('/reportar-queimadas/todos', methods=['GET'])
@login_required
def listar_queimadas():
    reports = FireReport.query.order_by(FireReport.created_at.desc()).limit(50).all()
    
    result = []
    for report in reports:
        result.append({
            'id': report.id,
            'lat': report.lat,
            'lon': report.lon,
            'status': report.status,
            'vote_count': report.vote_count,
            'created_at': report.created_at.isoformat()
        })
    
    return jsonify(result)

@main.route('/gerenciar-sensores')
@login_required
def manage_sensors():
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    all_sensors = []
    for farm in farms:
        for sensor in farm.sensors:
            all_sensors.append({
                'sensor': sensor,
                'farm': farm
            })
    return render_template('manage_sensors.html', sensors=all_sensors, farms=farms)

# ============================================
# Dispositivos (Bomba, LED UV)
# ============================================

@main.route('/devices')
@login_required
def devices():
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    all_devices = []
    for farm in farms:
        for device in farm.devices:
            all_devices.append({
                'device': device,
                'farm': farm
            })
    return render_template('devices.html', devices=all_devices)

@main.route('/device/<int:device_id>/toggle', methods=['POST'])
@login_required
def toggle_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    # Alternar estado
    device.is_active = not device.is_active
    if device.is_active:
        device.last_activated_at = datetime.utcnow()
    
    # Registrar operação
    operation = DeviceOperation(
        device_id=device.id,
        operation_type='on' if device.is_active else 'off',
        triggered_by='user',
        user_id=current_user.id
    )
    db.session.add(operation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_active': device.is_active,
        'message': f'{device.name} {"ligado" if device.is_active else "desligado"}'
    })

@main.route('/devices/new', methods=['GET', 'POST'])
@login_required
def new_device():
    form = DeviceForm()
    # Preencher opções de fazendas
    form.farm_id.choices = [(f.id, f.name) for f in Farm.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        device = Device(
            name=form.name.data,
            device_id=form.device_id.data,
            device_type=form.device_type.data,
            location=form.location.data,
            farm_id=form.farm_id.data,
            power_watts=form.power_watts.data,
            can_remote_control=True
        )
        db.session.add(device)
        db.session.commit()
        flash('Dispositivo cadastrado com sucesso!', 'success')
        return redirect(url_for('main.devices'))
    
    return render_template('devices_form.html', form=form, title='Novo Dispositivo')

# ============================================
# Sensores
# ============================================

@main.route('/sensors/new', methods=['GET', 'POST'])
@login_required
def new_sensor():
    form = SensorForm()
    # Preencher opções de fazendas
    form.farm_id.choices = [(f.id, f.name) for f in Farm.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        sensor = Sensor(
            name=form.name.data,
            device_id=form.device_id.data,
            sensor_type=form.sensor_type.data,
            location_description=form.location_description.data,
            sector=form.sector.data,
            farm_id=form.farm_id.data,
            protocol=form.protocol.data,
            reading_interval_minutes=form.reading_interval_minutes.data
        )
        db.session.add(sensor)
        db.session.commit()
        flash('Sensor cadastrado com sucesso!', 'success')
        return redirect(url_for('main.manage_sensors'))
    
    return render_template('sensors_form.html', form=form, title='Novo Sensor')

# ============================================
# Fazendas
# ============================================

@main.route('/farms')
@login_required
def farms():
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    return render_template('farms/list.html', farms=farms)

@main.route('/farms/new', methods=['GET', 'POST'])
@login_required
def new_farm():
    form = FarmForm()
    if form.validate_on_submit():
        farm = Farm(
            name=form.name.data,
            location=form.location.data,
            city=form.city.data,
            state=form.state.data,
            size_hectares=form.size_hectares.data,
            soil_type=form.soil_type.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            user_id=current_user.id
        )
        db.session.add(farm)
        db.session.commit()
        flash('Fazenda cadastrada com sucesso!', 'success')
        return redirect(url_for('main.farms'))
    return render_template('farms/form.html', form=form, title='Nova Fazenda')

@main.route('/farms/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_farm(id):
    farm = Farm.query.get_or_404(id)
    if farm.user_id != current_user.id:
        flash('Você não tem permissão para editar esta fazenda', 'danger')
        return redirect(url_for('main.farms'))
    form = FarmForm(obj=farm)
    if form.validate_on_submit():
        form.populate_obj(farm)
        db.session.commit()
        flash('Fazenda atualizada com sucesso!', 'success')
        return redirect(url_for('main.farms'))
    return render_template('farms/form.html', form=form, title='Editar Fazenda')

@main.route('/farms/<int:id>/delete', methods=['POST'])
@login_required
def delete_farm(id):
    farm = Farm.query.get_or_404(id)
    if farm.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta fazenda', 'danger')
        return redirect(url_for('main.farms'))
    db.session.delete(farm)
    db.session.commit()
    flash('Fazenda excluída com sucesso!', 'success')
    return redirect(url_for('main.farms'))

# ============================================
# Culturas
# ============================================

@main.route('/farms/<int:farm_id>/crops')
@login_required
def crops(farm_id):
    farm = Farm.query.get_or_404(farm_id)
    if farm.user_id != current_user.id:
        flash('Você não tem permissão para ver as culturas desta fazenda', 'danger')
        return redirect(url_for('main.farms'))
    crops = Crop.query.filter_by(farm_id=farm_id).all()
    return render_template('crops/list.html', farm=farm, crops=crops)

@main.route('/farms/<int:farm_id>/crops/new', methods=['GET', 'POST'])
@login_required
def new_crop(farm_id):
    farm = Farm.query.get_or_404(farm_id)
    if farm.user_id != current_user.id:
        flash('Você não tem permissão para adicionar culturas nesta fazenda', 'danger')
        return redirect(url_for('main.farms'))
    form = CropForm()
    if form.validate_on_submit():
        crop = Crop(
            name=form.name.data,
            variety=form.variety.data,
            planting_date=form.planting_date.data,
            harvest_date=form.harvest_date.data,
            area_hectares=form.area_hectares.data,
            expected_yield=form.expected_yield.data,
            ideal_soil_moisture_min=form.ideal_soil_moisture_min.data or 45.0,
            ideal_soil_moisture_max=form.ideal_soil_moisture_max.data or 70.0,
            ideal_temperature_min=form.ideal_temperature_min.data or 20.0,
            ideal_temperature_max=form.ideal_temperature_max.data or 30.0,
            farm_id=farm_id
        )
        db.session.add(crop)
        db.session.commit()
        flash('Cultura cadastrada com sucesso!', 'success')
        return redirect(url_for('main.crops', farm_id=farm_id))
    return render_template('crops/form.html', form=form, farm=farm, title='Nova Cultura')

# ============================================
# Atividades
# ============================================

@main.route('/crop/<int:crop_id>/activity/new', methods=['GET', 'POST'])
@login_required
def new_activity(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    if crop.farm.user_id != current_user.id:
        flash('Acesso negado', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(
            type=form.type.data,
            description=form.description.data,
            cost=form.cost.data,
            duration_minutes=form.duration_minutes.data,
            water_volume_liters=form.water_volume_liters.data,
            uv_duration_minutes=form.uv_duration_minutes.data,
            uv_intensity=form.uv_intensity.data,
            crop_id=crop_id
        )
        db.session.add(activity)
        db.session.commit()
        flash('Atividade registrada com sucesso!', 'success')
        return redirect(url_for('main.crops', farm_id=crop.farm_id))
    
    return render_template('activity_form.html', form=form, crop=crop)

# ============================================
# Consultas Técnicas
# ============================================

@main.route('/consultations')
@login_required
def consultations():
    consultations = Consultation.query.filter_by(user_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    return render_template('consultations/list.html', consultations=consultations)

@main.route('/consultations/new', methods=['GET', 'POST'])
@login_required
def new_consultation():
    form = ConsultationForm()
    if form.validate_on_submit():
        consultation = Consultation(
            title=form.title.data,
            question=form.question.data,
            category=form.category.data,
            priority=form.priority.data,
            user_id=current_user.id
        )
        db.session.add(consultation)
        db.session.commit()
        flash('Consulta enviada com sucesso!', 'success')
        return redirect(url_for('main.consultations'))
    return render_template('consultations/form.html', form=form)

# ============================================
# API - Dados em Tempo Real para AJAX
# ============================================

@main.route('/api/sensor/<int:sensor_id>/latest')
@login_required
def api_sensor_latest(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    if sensor.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    reading = sensor.get_latest_reading()
    if reading:
        return jsonify({
            'sensor_id': sensor.id,
            'sensor_name': sensor.name,
            'sensor_type': sensor.sensor_type,
            'value': reading.value,
            'unit': reading.unit,
            'timestamp': reading.timestamp.isoformat(),
            'is_valid': reading.is_valid
        })
    return jsonify({'error': 'Sem dados'}), 404

@main.route('/api/sensor/<int:sensor_id>/history')
@login_required
def api_sensor_history(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    if sensor.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    hours = request.args.get('hours', 24, type=int)
    since = datetime.utcnow() - timedelta(hours=hours)
    
    readings = SensorReading.query.filter(
        SensorReading.sensor_id == sensor_id,
        SensorReading.timestamp >= since,
        SensorReading.is_valid == True
    ).order_by(SensorReading.timestamp.asc()).all()
    
    data = [{
        'timestamp': r.timestamp.isoformat(),
        'value': r.value,
        'value_secondary': r.value_secondary
    } for r in readings]
    
    return jsonify(data)

@main.route('/api/farms/summary')
@login_required
def api_farms_summary():
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    
    summary = []
    for farm in farms:
        sensors_data = []
        for sensor in farm.sensors:
            reading = sensor.get_latest_reading()
            if reading:
                sensors_data.append({
                    'name': sensor.name,
                    'type': sensor.sensor_type,
                    'value': reading.value,
                    'unit': reading.unit,
                    'timestamp': reading.timestamp.isoformat()
                })
        
        summary.append({
            'farm_id': farm.id,
            'farm_name': farm.name,
            'sensors': sensors_data
        })
    
    return jsonify(summary)

@main.route('/api/device/<int:device_id>/status')
@login_required
def api_device_status(device_id):
    device = Device.query.get_or_404(device_id)
    if device.farm.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    return jsonify({
        'device_id': device.id,
        'name': device.name,
        'is_active': device.is_active,
        'is_online': device.is_online,
        'last_activated': device.last_activated_at.isoformat() if device.last_activated_at else None,
        'total_runtime_hours': device.total_runtime_hours
    })

@main.route('/api/weather/amazon/<location>')
@login_required
def api_amazon_weather(location):
    """API integrada com dados da Amazônia - previsão de seca e cheia"""
    # Integração futura com APIs da ANA (Agência Nacional de Águas)
    # Por enquanto retorna dados simulados
    
    return jsonify({
        'location': location,
        'temperature': 28.5,
        'humidity': 78,
        'river_level_cm': 245,
        'precipitation_probability': 45,
        'flood_risk': 'low',  # low, medium, high, critical
        'drought_risk': 'low',
        'uv_index': 8,
        'data_source': 'Amazon API + Local Sensors'
    })

@main.route('/api/alerts/unread-count')
@login_required
def api_unread_alerts_count():
    count = Alert.query.join(Farm).filter(
        Farm.user_id == current_user.id,
        Alert.is_read == False
    ).count()
    return jsonify({'unread_count': count})

# ============================================
# Plantios
# ============================================

@main.route('/plantios')
@login_required
def plantios():
    """Lista todos os plantios do usuário"""
    from datetime import datetime
    # Buscar plantios do usuário (através das fazendas)
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    farm_ids = [f.id for f in farms]
    
    # Buscar safras/culturas ativas
    crops = Crop.query.filter(Crop.farm_id.in_(farm_ids)).all()
    
    return render_template('plantios.html', crops=crops, now=datetime.utcnow().date())

@main.route('/plantios/add', methods=['GET', 'POST'])
@login_required
def add_plantio():
    """Adicionar novo plantio - usa apenas a fazenda do usuário"""
    import os
    import requests
    from datetime import datetime, timedelta
    
    form = CropForm()
    
    # Buscar fazenda do usuário (obrigatório)
    user_farm = Farm.query.filter_by(user_id=current_user.id).first()
    if not user_farm:
        flash('Você precisa ter uma fazenda cadastrada primeiro.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    if form.validate_on_submit():
        planting_date = form.planting_date.data
        estimated_harvest_date = form.estimated_harvest_date.data
        
        # Se não informou data de colheita, calcular com IA
        if not estimated_harvest_date:
            try:
                groq_api_key = os.environ.get('GROOQ_API')
                if groq_api_key:
                    crop_type = form.crop_type.data
                    
                    prompt = f"""Você é um assistente agrícola especializado. 
                    Dado o tipo de cultura "{crop_type}" e a data de plantio "{planting_date}", 
                    qual é o tempo médio de ciclo em dias até a colheita?
                    Responda APENAS com um número inteiro representando os dias.
                    Exemplo: 120"""
                    
                    response = requests.post(
                        'https://api.groq.com/openai/v1/chat/completions',
                        headers={
                            'Authorization': f'Bearer {groq_api_key}',
                            'Content-Type': 'application/json'
                        },
                        json={
                            'model': 'llama3-8b-8192',
                            'messages': [
                                {'role': 'system', 'content': 'Você é um assistente agrícola. Responda apenas com números inteiros.'},
                                {'role': 'user', 'content': prompt}
                            ],
                            'temperature': 0.1,
                            'max_tokens': 10
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result['choices'][0]['message']['content'].strip()
                        # Extrair número da resposta
                        import re
                        days_match = re.search(r'\d+', ai_response)
                        if days_match:
                            days = int(days_match.group())
                            estimated_harvest_date = planting_date + timedelta(days=days)
                            flash(f'Data de colheita calculada pela IA: {estimated_harvest_date.strftime("%d/%m/%Y")} ({days} dias)', 'info')
                        else:
                            # Fallback: usar média padrão
                            estimated_harvest_date = planting_date + timedelta(days=120)
                            flash('Usando data padrão de 120 dias para colheita.', 'info')
                    else:
                        # Fallback se API falhar
                        estimated_harvest_date = planting_date + timedelta(days=120)
                        flash('API indisponível. Usando data padrão de 120 dias.', 'warning')
                else:
                    # Sem API key, usar padrão
                    estimated_harvest_date = planting_date + timedelta(days=120)
                    flash('Usando data padrão de 120 dias para colheita.', 'info')
            except Exception as e:
                # Em caso de erro, usar data padrão
                estimated_harvest_date = planting_date + timedelta(days=120)
                flash(f'Erro ao calcular com IA. Usando data padrão: {str(e)}', 'warning')
        
        # Criar o plantio vinculado à fazenda do usuário
        crop = Crop(
            name=form.name.data,
            crop_type=form.crop_type.data,
            farm_id=user_farm.id,
            planting_date=planting_date,
            estimated_harvest_date=estimated_harvest_date,
            area_hectares=form.area_hectares.data,
            expected_yield=form.expected_yield_kg.data,
            notes=form.notes.data
        )
        db.session.add(crop)
        db.session.commit()
        flash(f'Plantio "{crop.name}" cadastrado com sucesso!', 'success')
        return redirect(url_for('main.plantios'))
    else:
        # Mostrar erros do formulário
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'warning')
    
    # Pre-fill farm data
    form.farm_name.data = user_farm.name
    form.farm_location.data = user_farm.city or user_farm.location
    form.farm_state.data = user_farm.state
    
    return render_template('plantios_form.html', form=form, title='Novo Plantio', user_farm=user_farm)

# ============================================
# API ANHANGÁ - Integração Externa
# ============================================

@main.route('/api/notificacoes', methods=['POST'])
def receber_notificacao_anhanga():
    """
    Endpoint para receber notificações externas do ANHANGÁ
    
    Recebe JSON com:
    - tipo: tipo de notificação
    - latitude: coordenada latitude
    - longitude: coordenada longitude
    - fonte: origem da notificação
    
    Salva em memória e retorna confirmação
    """
    try:
        data = request.get_json()
        
        # Validar dados recebidos
        if not data:
            return jsonify({'error': 'Nenhum dado recebido'}), 400
        
        tipo = data.get('tipo')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        fonte = data.get('fonte')
        
        if not all([tipo, latitude, longitude, fonte]):
            return jsonify({'error': 'Dados incompletos. Campos obrigatórios: tipo, latitude, longitude, fonte'}), 400
        
        # Salvar na lista em memória
        notificacao = {
            'tipo': tipo,
            'latitude': latitude,
            'longitude': longitude,
            'fonte': fonte,
            'timestamp': datetime.utcnow().isoformat()
        }
        anhanga_notifications.append(notificacao)
        
        # Log no console
        logger.info(f"Nova queimada detectada próxima! Tipo: {tipo}, Lat: {latitude}, Lon: {longitude}, Fonte: {fonte}")
        print(f"Nova queimada detectada próxima! Tipo: {tipo}, Lat: {latitude}, Lon: {longitude}, Fonte: {fonte}")
        
        return jsonify({'status': 'recebido'}), 200
        
    except Exception as e:
        logger.error(f"Erro ao receber notificação do ANHANGÁ: {str(e)}")
        return jsonify({'error': str(e)}), 500


@main.route('/api/notificacoes', methods=['GET'])
def listar_notificacoes_anhanga():
    """
    Endpoint para listar todas as notificações recebidas do ANHANGÁ
    """
    return jsonify({
        'total': len(anhanga_notifications),
        'notificacoes': anhanga_notifications
    }), 200


def enviar_reporte_anhanga(tipo, latitude, longitude, imagem_path=None, username=None):
    """
    Função para enviar reportes para o sistema ANHANGÁ

    Parâmetros:
    - tipo: tipo de reporte
    - latitude: coordenada latitude
    - longitude: coordenada longitude
    - imagem_path: caminho da imagem (opcional)
    - username: nome do usuário (opcional)

    Envia POST para http://localhost:5000/api/reportes
    """
    try:
        url = f'{ANHANGA_URL}/api/reportes'

        payload = {
            'latitude': latitude,
            'longitude': longitude,
            'fonte': 'tupa',
            'nivel': 3
        }

        # Adicionar username para identificação
        # ANHANGÁ usa usuario como user_id e username como nome de exibição
        # Se não enviar usuario, ANHANGÁ gera username = f"tupa_{fonte}"
        # Para enviar nome personalizado, enviamos usuario como string
        if username:
            payload['usuario'] = f"tupa_{username}"

        # Converter imagem para base64 se fornecida
        if imagem_path:
            try:
                full_path = os.path.join(current_app.root_path, imagem_path.lstrip('/'))
                if os.path.exists(full_path):
                    with open(full_path, 'rb') as f:
                        payload['imagem'] = base64.b64encode(f.read()).decode('utf-8')
            except Exception as e:
                logger.warning(f"Erro ao converter imagem para base64: {e}")

        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            logger.info(f"Reporte enviado para ANHANGÁ com sucesso: {payload}")
            return True, response.json()
        else:
            logger.error(f"Erro ao enviar reporte para ANHANGÁ: {response.status_code} - {response.text}")
            return False, response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão ao enviar reporte para ANHANGÁ: {str(e)}")
        return False, {'error': str(e)}
    except Exception as e:
        logger.error(f"Erro ao enviar reporte para ANHANGÁ: {str(e)}")
        return False, {'error': str(e)}


@main.route('/api/enviar-reporte-anhanga', methods=['POST'])
@login_required
def enviar_reporte_anhanga_endpoint():
    """
    Endpoint para enviar reporte para ANHANGÁ via API interna
    """
    try:
        data = request.get_json()
        
        tipo = data.get('tipo', 'queimada')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        imagem_path = data.get('imagem_path')
        
        if not latitude or not longitude:
            return jsonify({'error': 'Latitude e Longitude são obrigatórios'}), 400
        
        success, result = enviar_reporte_anhanga(tipo, latitude, longitude, imagem_path)
        
        if success:
            return jsonify({'status': 'enviado', 'data': result}), 200
        else:
            return jsonify({'status': 'erro', 'error': result}), 500
            
    except Exception as e:
        logger.error(f"Erro no endpoint de envio para ANHANGÁ: {str(e)}")
        return jsonify({'error': str(e)}), 500

