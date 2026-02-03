from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from datetime import datetime
from app.extensions import db

# Importamos los modelos NUEVOS
from app.modules.rrhh.models.funcionarios import Persona
from app.modules.rrhh.models.contratos import ContratoHonorario, Programa
# Nota: Si aún no migramos 'CuentaPresupuestaria' o 'EscalaViaticos', 
# comentaremos esas líneas temporalmente para que no falle.

core_bp = Blueprint('core', __name__)

@core_bp.route('/')
@core_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        # 1. KPIs Básicos
        total_funcionarios = Persona.query.count()
        
        # 2. KPIs Contratos (Si la tabla existe)
        try:
            total_contratos = ContratoHonorario.query.count()
        except:
            total_contratos = 0
            
        try:
            total_programas = Programa.query.count()
        except:
            total_programas = 0
        
        # 3. KPI Financiero (Simulado por ahora hasta migrar Billetera)
        saldo_total_global = 0 
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        return render_template('dashboard.html',
                               total_funcionarios=total_funcionarios,
                               total_contratos=total_contratos,
                               total_programas=total_programas,
                               saldo_total_global=saldo_total_global,
                               fecha_actual=fecha_actual)

    except Exception as e:
        print(f"Error Dashboard: {e}")
        return render_template('dashboard.html', 
                               total_funcionarios=0, 
                               total_contratos=0, 
                               saldo_total_global=0,
                               fecha_actual=datetime.now().strftime("%d/%m/%Y"))