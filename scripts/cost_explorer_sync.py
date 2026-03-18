#!/usr/bin/env python3
"""
cost_explorer_sync.py
Obtiene costos reales desde AWS Cost Explorer usando OIDC (Caso L)
y actualiza apps/cost-calculator/costs.json.

Variables de entorno requeridas (configurar en GitLab CI/CD > Variables):
  GITLAB_OIDC_TOKEN  — inyectado automaticamente por GitLab cuando se usa id_tokens
  AWS_ROLE_ARN       — ej: arn:aws:iam::123456789012:role/gitlab-oidc-role
  AWS_REGION         — por defecto us-east-1
"""

import boto3
import json
import os
import sys
from datetime import date, datetime


COSTS_JSON_PATH = "apps/cost-calculator/costs.json"

CASE_TAGS = {
    "caso-a": "caso-a",
    "caso-b": "caso-b",
    "caso-c": "caso-c",
    "caso-d": "caso-d",
    "caso-e": "caso-e",
    "caso-f": "caso-f",
    "caso-g": "caso-g",
    "caso-h": "caso-h",
    "caso-j": "caso-j",
    "caso-k": "caso-k",
    "caso-l": "caso-l",
}


def assume_role_with_oidc():
    oidc_token = os.environ.get("GITLAB_OIDC_TOKEN")
    role_arn = os.environ.get("AWS_ROLE_ARN")
    region = os.environ.get("AWS_REGION", "us-east-1")

    if not oidc_token or not role_arn:
        print("ERROR: GITLAB_OIDC_TOKEN y AWS_ROLE_ARN son requeridos.")
        sys.exit(1)

    sts = boto3.client("sts", region_name=region)
    response = sts.assume_role_with_web_identity(
        RoleArn=role_arn,
        RoleSessionName="gitlab-cost-explorer-sync",
        WebIdentityToken=oidc_token,
    )
    return response["Credentials"]


def get_cost_by_tag(creds, start_date, end_date):
    """Obtiene costos agrupados por tag 'Project'."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    ce = boto3.client(
        "ce",
        region_name=region,
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start_date, "End": end_date},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "TAG", "Key": "Project"}],
    )
    return response


def get_total_cost(creds, start_date, end_date):
    """Obtiene el costo total de la cuenta en el periodo."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    ce = boto3.client(
        "ce",
        region_name=region,
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start_date, "End": end_date},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )
    return response


def load_existing_costs():
    try:
        with open(COSTS_JSON_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def build_costs_json(tag_costs, total_cost_usd, start_date, existing):
    today = date.today()
    stacks = existing.get("stacks", {})

    # Mapear costos por tag a cada caso
    cost_by_case = {}
    for result in tag_costs.get("ResultsByTime", []):
        for group in result.get("Groups", []):
            tag_value = group["Keys"][0]  # "Project$caso-j" o similar
            # Normalizar: el tag puede ser "caso-j" o "Project$caso-j"
            normalized = tag_value.replace("Project$", "").lower().strip()
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
            if normalized in CASE_TAGS:
                cost_by_case[normalized] = round(amount, 4)

    # Actualizar costos en stacks existentes, preservar status
    for case_id in CASE_TAGS:
        if case_id not in stacks:
            stacks[case_id] = {
                "status": "unknown",
                "cost_mtd": 0.00,
                "description": case_id,
            }
        stacks[case_id]["cost_mtd"] = cost_by_case.get(case_id, 0.00)
        stacks[case_id]["last_sync"] = today.isoformat()

    return {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "month": today.strftime("%Y-%m"),
        "source": "aws-cost-explorer",
        "note": "Generado automaticamente por el job cost-explorer-sync de GitLab CI.",
        "total_mtd_usd": round(total_cost_usd, 4),
        "stacks": stacks,
    }


def main():
    today = date.today()
    start_date = today.replace(day=1).isoformat()
    end_date = today.isoformat()

    if start_date == end_date:
        # Si es dia 1 del mes, Cost Explorer necesita al menos 1 dia de rango
        print("Dia 1 del mes — sin datos de Cost Explorer aun. Saliendo sin cambios.")
        sys.exit(0)

    print(f"Obteniendo costos del {start_date} al {end_date}...")
    creds = assume_role_with_oidc()

    tag_costs = get_cost_by_tag(creds, start_date, end_date)
    total_resp = get_total_cost(creds, start_date, end_date)

    total_cost = 0.0
    for result in total_resp.get("ResultsByTime", []):
        total_cost += float(result["Total"]["UnblendedCost"]["Amount"])

    existing = load_existing_costs()
    costs_data = build_costs_json(tag_costs, total_cost, start_date, existing)

    with open(COSTS_JSON_PATH, "w") as f:
        json.dump(costs_data, f, indent=2)

    print(f"costs.json actualizado — total MTD: ${total_cost:.4f} USD")
    print(f"Costos por caso: {json.dumps({k: v['cost_mtd'] for k, v in costs_data['stacks'].items()}, indent=2)}")


if __name__ == "__main__":
    main()
