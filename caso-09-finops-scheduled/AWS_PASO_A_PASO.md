# Caso 09 — Guia paso a paso: FinOps + Scheduled Workflows

> Estado: Implementacion proyectada — Q4 2026.
> Tiempo estimado: 45 minutos.

---

## Que resuelve este caso

Un workflow programado (cron) que se ejecuta el primer dia de cada mes,
extrae los costos reales de AWS Cost Explorer con boto3, y hace commit
automatico de un reporte Markdown en el repositorio.

---

## Prerrequisitos

| Requisito | Verificacion |
|:---|:---|
| Cost Explorer habilitado en la cuenta | AWS Console -> Cost Explorer -> Enable |
| Permisos `ce:GetCostAndUsage` en el rol IAM | Ver paso 1 |
| Python 3.11+ con boto3 | `pip show boto3` |

---

## Paso 1 — Permisos IAM para Cost Explorer

Añadir al rol de GitHub Actions:

```json
{
  "Effect": "Allow",
  "Action": [
    "ce:GetCostAndUsage",
    "ce:GetDimensionValues",
    "ce:GetCostForecast"
  ],
  "Resource": "*"
}
```

Cost Explorer no tiene ARN de recurso especifico — el `*` es requerido.

---

## Paso 2 — Script Python para extraer costos

```python
# scripts/get_costs.py
import boto3
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json

def get_monthly_costs():
    ce = boto3.client('ce', region_name='us-east-1')
    today = date.today()
    start = (today - relativedelta(months=1)).replace(day=1).isoformat()
    end = today.replace(day=1).isoformat()

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    results = []
    total = 0.0
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        unit = group['Metrics']['UnblendedCost']['Unit']
        if amount > 0:
            results.append({'service': service, 'amount': amount, 'unit': unit})
            total += amount

    results.sort(key=lambda x: x['amount'], reverse=True)
    return results, total, start, end

def format_markdown(results, total, start, end):
    lines = [
        f'## Costos AWS — Periodo {start} a {end}',
        '',
        f'**Total: ${total:.4f} USD**',
        '',
        '| Servicio | Costo (USD) |',
        '|:---|---:|',
    ]
    for r in results:
        lines.append(f"| {r['service']} | ${r['amount']:.4f} |")

    lines += ['', f'*Generado automaticamente el {datetime.utcnow().strftime(\"%Y-%m-%d %H:%M\")} UTC*']
    return '\n'.join(lines)

if __name__ == '__main__':
    results, total, start, end = get_monthly_costs()
    markdown = format_markdown(results, total, start, end)

    with open('docs/FINOPS_COSTOS.md', 'r') as f:
        content = f.read()

    marker = '## Historial de costos reales'
    if marker in content:
        idx = content.index(marker) + len(marker)
        new_content = content[:idx] + '\n\n' + markdown + content[idx:]
    else:
        new_content = content + '\n\n' + marker + '\n\n' + markdown

    with open('docs/FINOPS_COSTOS.md', 'w') as f:
        f.write(new_content)

    print(f'Actualizado: Total del mes = ${total:.4f} USD')
```

---

## Paso 3 — Configurar AWS Budgets con alarma

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws budgets create-budget \
  --account-id $ACCOUNT_ID \
  --budget '{
    "BudgetName": "proyectos-aws-mensual",
    "BudgetLimit": {"Amount": "10", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [{
      "SubscriptionType": "EMAIL",
      "Address": "tu-email@ejemplo.com"
    }]
  }]'
```

---

## Paso 4 — Workflow con cron y auto-commit

```yaml
name: Caso 09 — FinOps Report

on:
  schedule:
    - cron: '0 8 1 * *'    # 1 de cada mes, 08:00 UTC
  workflow_dispatch:         # permite ejecucion manual

permissions:
  contents: write            # necesario para hacer commit
  id-token: write

jobs:
  finops-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - run: pip install boto3 python-dateutil

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Generar reporte de costos
        run: python scripts/get_costs.py

      - name: Commit y push del reporte
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/FINOPS_COSTOS.md
          git diff --staged --quiet || git commit -m "chore: actualizar costos AWS $(date +%Y-%m)"
          git push
```

---

## Paso 5 — Verificacion

Ejecutar el workflow manualmente desde GitHub Actions:

```text
Actions -> Caso 09 - FinOps Report -> Run workflow -> Run workflow
```

Verificar el commit automatico:

```bash
git log --oneline -3
# abc1234 chore: actualizar costos AWS 2026-10
```

Verificar el reporte en `docs/FINOPS_COSTOS.md`:

```bash
tail -30 docs/FINOPS_COSTOS.md
```

---

## Errores comunes y soluciones

### `DataUnavailableException` en Cost Explorer

Causa: Los datos de costo del mes anterior pueden tardar 24-48 horas en estar
disponibles despues del cierre de mes.

Solucion: Ejecutar el cron el dia 2 o 3 del mes en lugar del dia 1:

```yaml
cron: '0 8 2 * *'    # dia 2 de cada mes
```

---

### El commit automatico falla por rama protegida

Causa: Si `main` tiene proteccion que requiere PR, el `git push` directo falla.

Solucion: Crear una rama temporal y abrir un PR automatico:

```bash
git checkout -b chore/finops-$(date +%Y-%m)
git commit -m "chore: actualizar costos"
git push origin chore/finops-$(date +%Y-%m)
gh pr create --title "chore: costos $(date +%Y-%m)" --body "Reporte automatico"
```

---

## Siguiente paso

-> [Caso 10 — Multi-region + DR](../caso-10-multiregion-dr/AWS_PASO_A_PASO.md): alta disponibilidad geografica real.
