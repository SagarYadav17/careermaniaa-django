import requests
import base64
from Cryptodome.Cipher import AES
from os import environ
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://app.infisical.com"
SECRET_TOKEN = environ.get("SECRET_TOKEN")


def decrypt(ciphertext, iv, tag, secret):
    secret = bytes(secret, "utf-8")
    iv = base64.standard_b64decode(iv)
    tag = base64.standard_b64decode(tag)
    ciphertext = base64.standard_b64decode(ciphertext)

    cipher = AES.new(secret, AES.MODE_GCM, iv)
    cipher.update(tag)
    cleartext = cipher.decrypt(ciphertext).decode("utf-8")
    return cleartext


def get_secrets():
    service_token_secret = SECRET_TOKEN[SECRET_TOKEN.rindex(".") + 1 :]  # noqa E203

    # 1. Get your Infisical Token data
    service_token_data = requests.get(
        f"{BASE_URL}/api/v2/service-token",
        headers={"Authorization": f"Bearer {SECRET_TOKEN}"},
    ).json()

    # 2. Get secrets for your project and environment
    data = requests.get(
        f"{BASE_URL}/api/v3/secrets",
        params={"environment": "dev", "workspaceId": service_token_data["workspace"]},
        headers={"Authorization": f"Bearer {SECRET_TOKEN}"},
    ).json()

    encrypted_secrets = data["secrets"]

    # 3. Decrypt the (encrypted) project key with the key from your Infisical Token
    project_key = decrypt(
        ciphertext=service_token_data["encryptedKey"],
        iv=service_token_data["iv"],
        tag=service_token_data["tag"],
        secret=service_token_secret,
    )

    # 4. Decrypt the (encrypted) secrets
    secrets = {}
    for secret in encrypted_secrets:
        secret_key = decrypt(
            ciphertext=secret["secretKeyCiphertext"],
            iv=secret["secretKeyIV"],
            tag=secret["secretKeyTag"],
            secret=project_key,
        )

        secret_value = decrypt(
            ciphertext=secret["secretValueCiphertext"],
            iv=secret["secretValueIV"],
            tag=secret["secretValueTag"],
            secret=project_key,
        )

        secrets[secret_key] = secret_value

    return secrets
