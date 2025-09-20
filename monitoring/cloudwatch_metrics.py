import boto3
import time
import random

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

def publish_metric(metric_name, value, unit="Count"):
    """Publish a custom metric to CloudWatch"""
    response = cloudwatch.put_metric_data(
        Namespace="OrderSystem", 
        MetricData=[
            {
                "MetricName": metric_name,
                "Value": value,
                "Unit": unit
            }
        ]
    )
    print(f"[CloudWatch] Published {metric_name}={value} {unit}")
    return response


if __name__ == "__main__":
    # Example: simulate metrics
    while True:
        # Simulate order count
        orders = random.randint(1, 10)
        publish_metric("OrdersProcessed", orders)

        # Simulate failures
        failures = random.randint(0, 2)
        publish_metric("Failures", failures)

        time.sleep(60)  
