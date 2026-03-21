param(
  [string[]]$Regions = @("us-east-2", "us-east-1", "sa-east-1"),
  [string]$BillingRegion = "us-east-1",
  [string]$StartDate = (Get-Date -Day 1).ToString("yyyy-MM-dd"),
  [string]$EndDate = (Get-Date).AddDays(1).ToString("yyyy-MM-dd"),
  [string]$Profile,
  [string]$OutputPath
)

$ErrorActionPreference = "Stop"

if ($Regions.Count -eq 1 -and $Regions[0] -match ",") {
  $Regions = $Regions[0].Split(",").Trim()
}

if ($OutputPath) {
  $outputDirectory = Split-Path -Path $OutputPath -Parent
  if ($outputDirectory) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
  }
  Start-Transcript -Path $OutputPath -Force | Out-Null
}

function Write-Section {
  param([string]$Title)
  Write-Host ""
  Write-Host ("=" * 88) -ForegroundColor Cyan
  Write-Host $Title -ForegroundColor Cyan
  Write-Host ("=" * 88) -ForegroundColor Cyan
}

function Invoke-AwsCommand {
  param([string[]]$Arguments)

  $fullArgs = @()
  if ($Profile) {
    $fullArgs += @("--profile", $Profile)
  }
  $fullArgs += $Arguments

  $output = & aws @fullArgs 2>&1
  if ($LASTEXITCODE -ne 0) {
    Write-Host ("No disponible: " + ($output -join " ")) -ForegroundColor Yellow
    return
  }

  if ($output) {
    $output
  } else {
    Write-Host "(sin datos)"
  }
}

function Get-AwsText {
  param([string[]]$Arguments)

  $fullArgs = @()
  if ($Profile) {
    $fullArgs += @("--profile", $Profile)
  }
  $fullArgs += $Arguments

  $output = & aws @fullArgs 2>$null
  if ($LASTEXITCODE -ne 0) {
    return $null
  }

  if ($output -is [System.Array]) {
    return ($output -join " ").Trim()
  }

  return [string]$output
}

function Show-Table {
  param(
    [string]$Label,
    [string[]]$Arguments
  )

  Write-Host ""
  Write-Host ("- " + $Label) -ForegroundColor Green
  Invoke-AwsCommand -Arguments $Arguments
}

Write-Section "AWS Cost Control Report"
Write-Host "Workload regions : $($Regions -join ', ')" -ForegroundColor Gray
Write-Host "Billing region   : $BillingRegion" -ForegroundColor Gray
Write-Host "Cost window      : $StartDate -> $EndDate (End is exclusive in Cost Explorer)" -ForegroundColor Gray

$primaryRegion = $Regions[0]
$accountId = Get-AwsText -Arguments @("sts", "get-caller-identity", "--region", $primaryRegion, "--query", "Account", "--output", "text")

Write-Section "Identity And Account"
Show-Table -Label "Caller identity" -Arguments @(
  "sts", "get-caller-identity",
  "--region", $primaryRegion,
  "--output", "table"
)
Show-Table -Label "Account plan and remaining credits" -Arguments @(
  "freetier", "get-account-plan-state",
  "--region", $BillingRegion,
  "--output", "table"
)
Show-Table -Label "Free Tier usage for repository services" -Arguments @(
  "freetier", "get-free-tier-usage",
  "--region", $BillingRegion,
  "--query", "freeTierUsages[?contains(service, 'Lambda') || contains(service, 'DynamoDB') || contains(service, 'CloudWatch') || contains(service, 'Simple Queue Service') || contains(service, 'Simple Notification Service') || contains(service, 'X-Ray') || contains(service, 'API Gateway') || contains(service, 'Cognito')].[service,freeTierType,usageType,currentUsage.amount,currentUsage.unit,limit.amount,limit.unit]",
  "--output", "table"
)
Show-Table -Label "Month-to-date cost by service" -Arguments @(
  "ce", "get-cost-and-usage",
  "--region", $BillingRegion,
  "--time-period", "Start=$StartDate,End=$EndDate",
  "--granularity", "MONTHLY",
  "--metrics", "UnblendedCost",
  "--group-by", "Type=DIMENSION,Key=SERVICE",
  "--query", "ResultsByTime[0].Groups[].[Keys[0],Metrics.UnblendedCost.Amount,Metrics.UnblendedCost.Unit]",
  "--output", "table"
)

if ($accountId) {
  Show-Table -Label "Budgets for this account" -Arguments @(
    "budgets", "describe-budgets",
    "--region", $BillingRegion,
    "--account-id", $accountId,
    "--query", "Budgets[].[BudgetName,BudgetType,TimeUnit,BudgetLimit.Amount,BudgetLimit.Unit,CalculatedSpend.ActualSpend.Amount]",
    "--output", "table"
  )
}

Show-Table -Label "IAM OpenID Connect providers" -Arguments @(
  "iam", "list-open-id-connect-providers",
  "--query", "OpenIDConnectProviderList[].[Arn]",
  "--output", "table"
)

Write-Section "Global Or Shared Resources"
Show-Table -Label "S3 buckets" -Arguments @(
  "s3api", "list-buckets",
  "--query", "Buckets[].[Name,CreationDate]",
  "--output", "table"
)
Show-Table -Label "CloudFront distributions" -Arguments @(
  "cloudfront", "list-distributions",
  "--query", "DistributionList.Items[].[Id,DomainName,Enabled,Origins.Quantity]",
  "--output", "table"
)
Show-Table -Label "Route 53 hosted zones" -Arguments @(
  "route53", "list-hosted-zones",
  "--query", "HostedZones[].[Name,ResourceRecordSetCount,Config.PrivateZone]",
  "--output", "table"
)

foreach ($region in $Regions) {
  Write-Section "Regional Audit - $region"

  Show-Table -Label "Amplify apps" -Arguments @(
    "amplify", "list-apps",
    "--region", $region,
    "--query", "apps[].[name,platform,defaultDomain]",
    "--output", "table"
  )
  Show-Table -Label "ACM certificates" -Arguments @(
    "acm", "list-certificates",
    "--region", $region,
    "--query", "CertificateSummaryList[].[DomainName,Status]",
    "--output", "table"
  )
  Show-Table -Label "CloudFormation stacks" -Arguments @(
    "cloudformation", "list-stacks",
    "--region", $region,
    "--stack-status-filter", "CREATE_COMPLETE", "UPDATE_COMPLETE", "UPDATE_ROLLBACK_COMPLETE",
    "--query", "StackSummaries[].[StackName,StackStatus]",
    "--output", "table"
  )
  Show-Table -Label "HTTP APIs (API Gateway v2)" -Arguments @(
    "apigatewayv2", "get-apis",
    "--region", $region,
    "--query", "Items[].[Name,ProtocolType,ApiEndpoint]",
    "--output", "table"
  )
  Show-Table -Label "REST APIs (API Gateway v1)" -Arguments @(
    "apigateway", "get-rest-apis",
    "--region", $region,
    "--query", "items[].[name,id]",
    "--output", "table"
  )
  Show-Table -Label "Lambda functions" -Arguments @(
    "lambda", "list-functions",
    "--region", $region,
    "--query", "Functions[].[FunctionName,Runtime,LastModified]",
    "--output", "table"
  )
  Show-Table -Label "DynamoDB tables" -Arguments @(
    "dynamodb", "list-tables",
    "--region", $region,
    "--output", "table"
  )
  Show-Table -Label "Cognito user pools" -Arguments @(
    "cognito-idp", "list-user-pools",
    "--region", $region,
    "--max-results", "60",
    "--query", "UserPools[].[Name,Id]",
    "--output", "table"
  )
  Show-Table -Label "WAF web ACLs" -Arguments @(
    "wafv2", "list-web-acls",
    "--scope", "REGIONAL",
    "--region", $region,
    "--query", "WebACLs[].[Name,Id]",
    "--output", "table"
  )
  Show-Table -Label "CloudWatch dashboards" -Arguments @(
    "cloudwatch", "list-dashboards",
    "--region", $region,
    "--query", "DashboardEntries[].[DashboardName,LastModified]",
    "--output", "table"
  )
  Show-Table -Label "CloudWatch alarms" -Arguments @(
    "cloudwatch", "describe-alarms",
    "--region", $region,
    "--query", "MetricAlarms[].[AlarmName,StateValue,Namespace]",
    "--output", "table"
  )
  Show-Table -Label "CloudWatch log groups" -Arguments @(
    "logs", "describe-log-groups",
    "--region", $region,
    "--query", "logGroups[].[logGroupName,retentionInDays,storedBytes]",
    "--output", "table"
  )
  Show-Table -Label "EventBridge buses" -Arguments @(
    "events", "list-event-buses",
    "--region", $region,
    "--query", "EventBuses[].[Name,Arn]",
    "--output", "table"
  )

  $customBuses = Get-AwsText -Arguments @(
    "events", "list-event-buses",
    "--region", $region,
    "--query", "EventBuses[?Name!=`default`].Name",
    "--output", "text"
  )
  if ($customBuses) {
    foreach ($bus in ($customBuses -split "\s+" | Where-Object { $_ })) {
      Show-Table -Label "EventBridge rules for bus $bus" -Arguments @(
        "events", "list-rules",
        "--region", $region,
        "--event-bus-name", $bus,
        "--query", "Rules[].[Name,State]",
        "--output", "table"
      )
    }
  }

  Show-Table -Label "SQS queues" -Arguments @(
    "sqs", "list-queues",
    "--region", $region,
    "--output", "table"
  )
  Show-Table -Label "SNS topics" -Arguments @(
    "sns", "list-topics",
    "--region", $region,
    "--query", "Topics[].[TopicArn]",
    "--output", "table"
  )
  Show-Table -Label "ECR repositories" -Arguments @(
    "ecr", "describe-repositories",
    "--region", $region,
    "--query", "repositories[].[repositoryName,repositoryUri,imageScanningConfiguration.scanOnPush]",
    "--output", "table"
  )
  Show-Table -Label "ECS clusters" -Arguments @(
    "ecs", "list-clusters",
    "--region", $region,
    "--output", "table"
  )
  Show-Table -Label "EKS clusters" -Arguments @(
    "eks", "list-clusters",
    "--region", $region,
    "--output", "table"
  )
  Show-Table -Label "Load balancers" -Arguments @(
    "elbv2", "describe-load-balancers",
    "--region", $region,
    "--query", "LoadBalancers[].[LoadBalancerName,Type,Scheme,State.Code]",
    "--output", "table"
  )
  Show-Table -Label "EC2 instances (running and stopped)" -Arguments @(
    "ec2", "describe-instances",
    "--region", $region,
    "--filters", "Name=instance-state-name,Values=running,stopped",
    "--query", "Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]",
    "--output", "table"
  )
  Show-Table -Label "EBS volumes" -Arguments @(
    "ec2", "describe-volumes",
    "--region", $region,
    "--query", "Volumes[].[VolumeId,State,Size,VolumeType,Attachments[0].InstanceId]",
    "--output", "table"
  )
  Show-Table -Label "Elastic IPs" -Arguments @(
    "ec2", "describe-addresses",
    "--region", $region,
    "--query", "Addresses[].[PublicIp,AllocationId,AssociationId,InstanceId,NetworkInterfaceId]",
    "--output", "table"
  )
  Show-Table -Label "NAT gateways" -Arguments @(
    "ec2", "describe-nat-gateways",
    "--region", $region,
    "--filter", "Name=state,Values=available,pending",
    "--query", "NatGateways[].[NatGatewayId,State,SubnetId,NatGatewayAddresses[0].PublicIp]",
    "--output", "table"
  )
  Show-Table -Label "RDS instances" -Arguments @(
    "rds", "describe-db-instances",
    "--region", $region,
    "--query", "DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]",
    "--output", "table"
  )

  $wafCount = Get-AwsText -Arguments @("wafv2", "list-web-acls", "--scope", "REGIONAL", "--region", $region, "--query", "length(WebACLs)", "--output", "text")
  $dashCount = Get-AwsText -Arguments @("cloudwatch", "list-dashboards", "--region", $region, "--query", "length(DashboardEntries)", "--output", "text")
  $eksCount = Get-AwsText -Arguments @("eks", "list-clusters", "--region", $region, "--query", "length(clusters)", "--output", "text")
  $albCount = Get-AwsText -Arguments @("elbv2", "describe-load-balancers", "--region", $region, "--query", "length(LoadBalancers)", "--output", "text")
  $natCount = Get-AwsText -Arguments @("ec2", "describe-nat-gateways", "--region", $region, "--filter", "Name=state,Values=available,pending", "--query", "length(NatGateways)", "--output", "text")
  $runningEc2Count = Get-AwsText -Arguments @("ec2", "describe-instances", "--region", $region, "--filters", "Name=instance-state-name,Values=running", "--query", "length(Reservations[].Instances[])", "--output", "text")
  $rdsCount = Get-AwsText -Arguments @("rds", "describe-db-instances", "--region", $region, "--query", "length(DBInstances)", "--output", "text")

  Write-Host ""
  Write-Host "Risk summary for $region" -ForegroundColor Magenta
  Write-Host ("  WAF web ACLs        : " + $(if ($wafCount) { $wafCount } else { "n/a" }))
  Write-Host ("  Dashboards          : " + $(if ($dashCount) { $dashCount } else { "n/a" }))
  Write-Host ("  EKS clusters        : " + $(if ($eksCount) { $eksCount } else { "n/a" }))
  Write-Host ("  Load balancers      : " + $(if ($albCount) { $albCount } else { "n/a" }))
  Write-Host ("  NAT gateways        : " + $(if ($natCount) { $natCount } else { "n/a" }))
  Write-Host ("  EC2 running         : " + $(if ($runningEc2Count) { $runningEc2Count } else { "n/a" }))
  Write-Host ("  RDS instances       : " + $(if ($rdsCount) { $rdsCount } else { "n/a" }))
}

Write-Section "Recommended Reading Order"
Write-Host "1. docs/FINOPS_COSTOS.md"
Write-Host "2. docs/FINOPS_MANUAL.md"
Write-Host "3. docs/COST_CONTROL_COMMAND_CENTER.md"

if ($OutputPath) {
  Stop-Transcript | Out-Null
}
