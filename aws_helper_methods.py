from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from mypy_boto3_ssm import SSMClient
import boto3
import json


class SecretNotFound(Exception):
    pass

class SSM():
    def __init__(self, ssm_client = boto3.client("ssm", "us-east-1")):
        self.ssm_client = ssm_client
        
    def write_str_secret(self, secret_name: str, secret: str):
        return self.ssm_client.put_param(secret_name, "", secret)

    def write_dict_secret(self, secret_name: str, secret: dict):
        return self.ssm_client.put_param(secret_name, "", json.dumps(secret))
    
    def read_document(self, secret_name: str) -> str:
        return self.ssm_client.get_document(Name=secret_name)

    def read_str_secret(self, secret_name: str) -> str:
        try:
            return self.ssm_client.get_parameter(
                Name=secret_name,
                WithDecryption=True,
            )["Parameter"]["Value"]
        except (self.ssm_client.exceptions.ParameterNotFound):
            raise SecretNotFound(f"Secret '{secret_name}' not found")

    def read_dict_secret(self, secret_name: str) -> str:
        try:
            return json.loads(self.ssm_client.get_parameter(
                Name=secret_name,
                WithDecryption=True,
            )["Parameter"]["Value"])
        except (self.ssm_client.exceptions.ParameterNotFound):
            raise SecretNotFound(f"Secret '{secret_name}' not found")

    def get_secret(self, param_name: str) -> str:
        return self.ssm_client.get_param(param_name)["Parameter"]["Value"]

    def get_secrets(self, param_names: List[str]) -> List[str]:
        return [self.ssm_client.get_secret(param_name) for param_name in param_names]

    def delete_param(self, param_name: str):
        return self.ssm_client.delete_parameter(Name=param_name)
