#!/bin/bash
REGIONS=("us-east-1" "us-east-2" "sa-east-1")

for r in "${REGIONS[@]}"; do
    echo -e "\n==================== $r ===================="
    
    echo -e "\nEC2 Instancias (running/stopped):"
    aws ec2 describe-instances --region "$r" \
        --filters Name=instance-state-name,Values=running,stopped \
        --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' \
        --output table

    echo -e "\nEBS Volúmenes:"
    aws ec2 describe-volumes --region "$r" \
        --query 'Volumes[].[VolumeId,State,Size,VolumeType,Attachments[0].InstanceId]' \
        --output table

    echo -e "\nElastic IPs (EIP) y a qué están pegadas:"
    aws ec2 describe-addresses --region "$r" \
        --query 'Addresses[].[PublicIp,AllocationId,AssociationId,InstanceId,NetworkInterfaceId]' \
        --output table

    echo -e "\nNAT Gateways (MUY caro si queda uno):"
    aws ec2 describe-nat-gateways --region "$r" \
        --filter Name=state,Values=available,pending \
        --query 'NatGateways[].[NatGatewayId,State,SubnetId,NatGatewayAddresses[0].PublicIp]' \
        --output table

    echo -e "\nLoad Balancers (ALB/NLB):"
    aws elbv2 describe-load-balancers --region "$r" \
        --query 'LoadBalancers[].[LoadBalancerName,Type,Scheme,State.Code,DNSName]' \
        --output table

    echo -e "\nEKS Clusters:"
    aws eks list-clusters --region "$r" --output table

    echo -e "\nECS Clusters:"
    aws ecs list-clusters --region "$r" --output table

    echo -e "\nRDS DB Instances:"
    aws rds describe-db-instances --region "$r" \
        --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass]' \
        --output table
done
