import boto3
ssm = boto3.client('ssm')


def getApiUrl():
    parameter = ssm.get_parameter(Name='API_URL', WithDecryption=False)
    return parameter['Parameter']['Value']
