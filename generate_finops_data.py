import boto3
import json
import datetime
import os

# Configuración
REGION = "us-east-2"
BUDGET_NAME = "Vladimir-Monthly-Alert"
OUTPUT_FILE = "caso-l-finops-optimization/app/public/costs.json"

def get_costs():
    """Obtiene los costos acumulados del mes actual."""
    ce = boto3.client('ce', region_name=REGION)
    
    # Rango de fechas: Primer día del mes hasta hoy
    today = datetime.date.today()
    start_date = today.replace(day=1).isoformat()
    end_date = today.isoformat()
    
    # Si es el primer día del mes, end_date debe ser mañana para que funcione la API
    if start_date == end_date:
        end_date = (today + datetime.timedelta(days=1)).isoformat()

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )
        amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        return round(float(amount), 2)
    except Exception as e:
        print(f"Error obteniendo costos: {e}")
        return 0.00

def get_forecast():
    """Obtiene la proyección de costos para fin de mes."""
    ce = boto3.client('ce', region_name=REGION)
    
    today = datetime.date.today()
    start_date = (today + datetime.timedelta(days=1)).isoformat()
    
    # Primer día del próximo mes
    if today.month == 12:
        end_date = datetime.date(today.year + 1, 1, 1).isoformat()
    else:
        end_date = datetime.date(today.year, today.month + 1, 1).isoformat()

    try:
        response = ce.get_cost_forecast(
            TimePeriod={'Start': start_date, 'End': end_date},
            Metric='UNBLENDED_COST',
            Granularity='MONTHLY'
        )
        amount = response['Total']['Amount']
        return round(float(amount), 2)
    except Exception as e:
        print(f"Error obteniendo proyección (posiblemente falta de datos históricos): {e}")
        return 0.00

def get_budget_status():
    """Obtiene el estado de la alerta de presupuesto."""
    budgets = boto3.client('budgets', region_name="us-east-1") # Budgets es global pero endpoint en us-east-1
    account_id = boto3.client('sts').get_caller_identity().get('Account')

    try:
        response = budgets.describe_budget(
            AccountId=account_id,
            BudgetName=BUDGET_NAME
        )
        limit = float(response['Budget']['BudgetLimit']['Amount'])
        actual = float(response['Budget']['CalculatedSpend']['ActualSpend']['Amount'])
        
        status = "OK"
        if actual > limit:
            status = "EXCEDIDO"
        elif actual > (limit * 0.85):
            status = "ALERTA"
            
        return limit, status
    except Exception as e:
        print(f"Error obteniendo budget: {e}")
        return 5.00, "DESCONOCIDO"

def generate_json():
    print("Consultando AWS Cost Explorer y Budgets...")
    
    current_cost = get_costs()
    forecast_cost = get_forecast()
    limit, status = get_budget_status()
    
    # Manejo de caso borde: si no hay forecast, usar costo actual
    if forecast_cost == 0:
        forecast_cost = current_cost

    data = {
        "ultima_actualizacion": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
        "gasto_mes_real": abs(current_cost),
        "proyeccion_fin_mes": abs(forecast_cost),
        "presupuesto_mensual": limit,
        "estado_presupuesto": status,
        "region_activa": REGION,
        "moneda": "USD"
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Datos generados exitosamente en: {OUTPUT_FILE}")
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    generate_json()
