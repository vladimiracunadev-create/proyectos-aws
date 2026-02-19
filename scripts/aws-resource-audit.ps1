$regions = @("us-east-1","us-east-2","sa-east-1")

foreach ($r in $regions) {
  Write-Host "`n==================== $r ====================" -ForegroundColor Cyan

  Write-Host "`nEC2 Instancias (running/stopped):"
  aws ec2 describe-instances --region $r `
    --filters Name=instance-state-name,Values=running,stopped `
    --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' `
    --output table

  Write-Host "`nEBS Volúmenes:"
  aws ec2 describe-volumes --region $r `
    --query 'Volumes[].[VolumeId,State,Size,VolumeType,Attachments[0].InstanceId]' `
    --output table

  Write-Host "`nElastic IPs (EIP) y a qué están pegadas:"
  aws ec2 describe-addresses --region $r `
    --query 'Addresses[].[PublicIp,AllocationId,AssociationId,InstanceId,NetworkInterfaceId]' `
    --output table

  Write-Host "`nNAT Gateways (MUY caro si queda uno):"
  aws ec2 describe-nat-gateways --region $r `
    --filter Name=state,Values=available,pending `
    --query 'NatGateways[].[NatGatewayId,State,SubnetId,NatGatewayAddresses[0].PublicIp]' `
    --output table

  Write-Host "`nLoad Balancers (ALB/NLB):"
  aws elbv2 describe-load-balancers --region $r `
    --query 'LoadBalancers[].[LoadBalancerName,Type,Scheme,State.Code,DNSName]' `
    --output table

  Write-Host "`nEKS Clusters:"
  aws eks list-clusters --region $r --output table

  Write-Host "`nECS Clusters:"
  aws ecs list-clusters --region $r --output table

  Write-Host "`nRDS DB Instances:"
  aws rds describe-db-instances --region $r `
    --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]' `
    --output table
}
