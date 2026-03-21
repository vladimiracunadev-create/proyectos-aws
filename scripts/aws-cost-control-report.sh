#!/bin/bash
set -u

REGIONS=("us-east-2" "us-east-1" "sa-east-1")
BILLING_REGION="us-east-1"
PROFILE=""
OUTPUT_PATH=""

if date -d "+1 day" +%F >/dev/null 2>&1; then
  START_DATE="$(date +%Y-%m-01)"
  END_DATE="$(date -d "+1 day" +%Y-%m-%d)"
elif date -v+1d +%F >/dev/null 2>&1; then
  START_DATE="$(date +%Y-%m-01)"
  END_DATE="$(date -v+1d +%Y-%m-%d)"
else
  START_DATE="$(python -c "from datetime import date; print(date.today().replace(day=1))")"
  END_DATE="$(python -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")"
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --regions)
      IFS=',' read -r -a REGIONS <<< "$2"
      shift 2
      ;;
    --billing-region)
      BILLING_REGION="$2"
      shift 2
      ;;
    --start-date)
      START_DATE="$2"
      shift 2
      ;;
    --end-date)
      END_DATE="$2"
      shift 2
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --output-path)
      OUTPUT_PATH="$2"
      shift 2
      ;;
    --help|-h)
      cat <<'EOF'
Usage: ./scripts/aws-cost-control-report.sh [options]

Options:
  --regions us-east-2,us-east-1,sa-east-1
  --billing-region us-east-1
  --start-date YYYY-MM-DD
  --end-date YYYY-MM-DD
  --profile PROFILE
  --output-path ./finops-report.txt
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$OUTPUT_PATH" ]]; then
  if date +%Y%m%d-%H%M%S >/dev/null 2>&1; then
    TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
  else
    TIMESTAMP="$(python -c "from datetime import datetime; print(datetime.now().strftime('%Y%m%d-%H%M%S'))")"
  fi
  OUTPUT_PATH="./.tmp/skill-output/finops-report-$TIMESTAMP.txt"
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"
exec > >(tee "$OUTPUT_PATH") 2>&1

AWS_ARGS=()
if [[ -n "$PROFILE" ]]; then
  AWS_ARGS+=(--profile "$PROFILE")
fi

section() {
  local title="$1"
  echo
  printf '=%.0s' {1..88}
  echo
  echo "$title"
  printf '=%.0s' {1..88}
  echo
}

run_cmd() {
  local label="$1"
  shift
  echo
  echo "- $label"
  if ! aws "${AWS_ARGS[@]}" "$@"; then
    echo "No disponible"
  fi
}

get_text() {
  aws "${AWS_ARGS[@]}" "$@" 2>/dev/null || true
}

section "AWS Cost Control Report"
echo "Workload regions : ${REGIONS[*]}"
echo "Billing region   : $BILLING_REGION"
echo "Cost window      : $START_DATE -> $END_DATE (End is exclusive in Cost Explorer)"
echo "Report path      : $OUTPUT_PATH"

PRIMARY_REGION="${REGIONS[0]}"
ACCOUNT_ID="$(get_text sts get-caller-identity --region "$PRIMARY_REGION" --query Account --output text)"

section "Identity And Account"
run_cmd "Caller identity" \
  sts get-caller-identity \
  --region "$PRIMARY_REGION" \
  --output table

run_cmd "Account plan and remaining credits" \
  freetier get-account-plan-state \
  --region "$BILLING_REGION" \
  --output table

run_cmd "Free Tier usage for repository services" \
  freetier get-free-tier-usage \
  --region "$BILLING_REGION" \
  --query "freeTierUsages[?contains(service, 'Lambda') || contains(service, 'DynamoDB') || contains(service, 'CloudWatch') || contains(service, 'Simple Queue Service') || contains(service, 'Simple Notification Service') || contains(service, 'X-Ray') || contains(service, 'API Gateway') || contains(service, 'Cognito')].[service,freeTierType,usageType,currentUsage.amount,currentUsage.unit,limit.amount,limit.unit]" \
  --output table

run_cmd "Month-to-date cost by service" \
  ce get-cost-and-usage \
  --region "$BILLING_REGION" \
  --time-period "Start=$START_DATE,End=$END_DATE" \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query "ResultsByTime[0].Groups[].[Keys[0],Metrics.UnblendedCost.Amount,Metrics.UnblendedCost.Unit]" \
  --output table

if [[ -n "$ACCOUNT_ID" && "$ACCOUNT_ID" != "None" ]]; then
  run_cmd "Budgets for this account" \
    budgets describe-budgets \
    --region "$BILLING_REGION" \
    --account-id "$ACCOUNT_ID" \
    --query "Budgets[].[BudgetName,BudgetType,TimeUnit,BudgetLimit.Amount,BudgetLimit.Unit,CalculatedSpend.ActualSpend.Amount]" \
    --output table
fi

run_cmd "IAM OpenID Connect providers" \
  iam list-open-id-connect-providers \
  --query "OpenIDConnectProviderList[].[Arn]" \
  --output table

section "Global Or Shared Resources"
run_cmd "S3 buckets" \
  s3api list-buckets \
  --query "Buckets[].[Name,CreationDate]" \
  --output table

run_cmd "CloudFront distributions" \
  cloudfront list-distributions \
  --query "DistributionList.Items[].[Id,DomainName,Enabled,Origins.Quantity]" \
  --output table

run_cmd "Route 53 hosted zones" \
  route53 list-hosted-zones \
  --query "HostedZones[].[Name,ResourceRecordSetCount,Config.PrivateZone]" \
  --output table

for region in "${REGIONS[@]}"; do
  section "Regional Audit - $region"

  run_cmd "Amplify apps" \
    amplify list-apps \
    --region "$region" \
    --query "apps[].[name,platform,defaultDomain]" \
    --output table

  run_cmd "ACM certificates" \
    acm list-certificates \
    --region "$region" \
    --query "CertificateSummaryList[].[DomainName,Status]" \
    --output table

  run_cmd "CloudFormation stacks" \
    cloudformation list-stacks \
    --region "$region" \
    --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE UPDATE_ROLLBACK_COMPLETE \
    --query "StackSummaries[].[StackName,StackStatus]" \
    --output table

  run_cmd "HTTP APIs (API Gateway v2)" \
    apigatewayv2 get-apis \
    --region "$region" \
    --query "Items[].[Name,ProtocolType,ApiEndpoint]" \
    --output table

  run_cmd "REST APIs (API Gateway v1)" \
    apigateway get-rest-apis \
    --region "$region" \
    --query "items[].[name,id]" \
    --output table

  run_cmd "Lambda functions" \
    lambda list-functions \
    --region "$region" \
    --query "Functions[].[FunctionName,Runtime,LastModified]" \
    --output table

  run_cmd "DynamoDB tables" \
    dynamodb list-tables \
    --region "$region" \
    --output table

  run_cmd "Cognito user pools" \
    cognito-idp list-user-pools \
    --region "$region" \
    --max-results 60 \
    --query "UserPools[].[Name,Id]" \
    --output table

  run_cmd "WAF web ACLs" \
    wafv2 list-web-acls \
    --scope REGIONAL \
    --region "$region" \
    --query "WebACLs[].[Name,Id]" \
    --output table

  run_cmd "CloudWatch dashboards" \
    cloudwatch list-dashboards \
    --region "$region" \
    --query "DashboardEntries[].[DashboardName,LastModified]" \
    --output table

  run_cmd "CloudWatch alarms" \
    cloudwatch describe-alarms \
    --region "$region" \
    --query "MetricAlarms[].[AlarmName,StateValue,Namespace]" \
    --output table

  run_cmd "CloudWatch log groups" \
    logs describe-log-groups \
    --region "$region" \
    --query "logGroups[].[logGroupName,retentionInDays,storedBytes]" \
    --output table

  run_cmd "EventBridge buses" \
    events list-event-buses \
    --region "$region" \
    --query "EventBuses[].[Name,Arn]" \
    --output table

  CUSTOM_BUSES="$(get_text events list-event-buses --region "$region" --query "EventBuses[?Name!=\`default\`].Name" --output text)"
  if [[ -n "$CUSTOM_BUSES" && "$CUSTOM_BUSES" != "None" ]]; then
    for bus in $CUSTOM_BUSES; do
      run_cmd "EventBridge rules for bus $bus" \
        events list-rules \
        --region "$region" \
        --event-bus-name "$bus" \
        --query "Rules[].[Name,State]" \
        --output table
    done
  fi

  run_cmd "SQS queues" \
    sqs list-queues \
    --region "$region" \
    --output table

  run_cmd "SNS topics" \
    sns list-topics \
    --region "$region" \
    --query "Topics[].[TopicArn]" \
    --output table

  run_cmd "ECR repositories" \
    ecr describe-repositories \
    --region "$region" \
    --query "repositories[].[repositoryName,repositoryUri,imageScanningConfiguration.scanOnPush]" \
    --output table

  run_cmd "ECS clusters" \
    ecs list-clusters \
    --region "$region" \
    --output table

  run_cmd "EKS clusters" \
    eks list-clusters \
    --region "$region" \
    --output table

  run_cmd "Load balancers" \
    elbv2 describe-load-balancers \
    --region "$region" \
    --query "LoadBalancers[].[LoadBalancerName,Type,Scheme,State.Code]" \
    --output table

  run_cmd "EC2 instances (running and stopped)" \
    ec2 describe-instances \
    --region "$region" \
    --filters Name=instance-state-name,Values=running,stopped \
    --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==\`Name\`].Value|[0]]" \
    --output table

  run_cmd "EBS volumes" \
    ec2 describe-volumes \
    --region "$region" \
    --query "Volumes[].[VolumeId,State,Size,VolumeType,Attachments[0].InstanceId]" \
    --output table

  run_cmd "Elastic IPs" \
    ec2 describe-addresses \
    --region "$region" \
    --query "Addresses[].[PublicIp,AllocationId,AssociationId,InstanceId,NetworkInterfaceId]" \
    --output table

  run_cmd "NAT gateways" \
    ec2 describe-nat-gateways \
    --region "$region" \
    --filter Name=state,Values=available,pending \
    --query "NatGateways[].[NatGatewayId,State,SubnetId,NatGatewayAddresses[0].PublicIp]" \
    --output table

  run_cmd "RDS instances" \
    rds describe-db-instances \
    --region "$region" \
    --query "DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]" \
    --output table

  WAF_COUNT="$(get_text wafv2 list-web-acls --scope REGIONAL --region "$region" --query "length(WebACLs)" --output text)"
  DASH_COUNT="$(get_text cloudwatch list-dashboards --region "$region" --query "length(DashboardEntries)" --output text)"
  EKS_COUNT="$(get_text eks list-clusters --region "$region" --query "length(clusters)" --output text)"
  ALB_COUNT="$(get_text elbv2 describe-load-balancers --region "$region" --query "length(LoadBalancers)" --output text)"
  NAT_COUNT="$(get_text ec2 describe-nat-gateways --region "$region" --filter Name=state,Values=available,pending --query "length(NatGateways)" --output text)"
  EC2_RUNNING_COUNT="$(get_text ec2 describe-instances --region "$region" --filters Name=instance-state-name,Values=running --query "length(Reservations[].Instances[])" --output text)"
  RDS_COUNT="$(get_text rds describe-db-instances --region "$region" --query "length(DBInstances)" --output text)"

  echo
  echo "Risk summary for $region"
  echo "  WAF web ACLs        : ${WAF_COUNT:-n/a}"
  echo "  Dashboards          : ${DASH_COUNT:-n/a}"
  echo "  EKS clusters        : ${EKS_COUNT:-n/a}"
  echo "  Load balancers      : ${ALB_COUNT:-n/a}"
  echo "  NAT gateways        : ${NAT_COUNT:-n/a}"
  echo "  EC2 running         : ${EC2_RUNNING_COUNT:-n/a}"
  echo "  RDS instances       : ${RDS_COUNT:-n/a}"
done

section "Recommended Reading Order"
echo "1. docs/FINOPS_COSTOS.md"
echo "2. docs/FINOPS_MANUAL.md"
echo "3. docs/COST_CONTROL_COMMAND_CENTER.md"
