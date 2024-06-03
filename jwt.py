import json
import base64
import hmac
import hashlib
import time

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data):
    padding = 4 - len(data) % 4
    return base64.urlsafe_b64decode(data + "=" * padding)

def generate_jwt(payload, secret, algorithm='HS256'):
    if algorithm != 'HS256':
        raise ValueError("Unsupported algorithm. Only 'HS256' is supported.")

    header = {
        "alg": algorithm,
        "typ": "JWT"
    }

    payload['exp'] = int(time.time()) + 3600  # token expires in 1 hour

    encoded_header = base64url_encode(json.dumps(header).encode('utf-8'))
    encoded_payload = base64url_encode(json.dumps(payload).encode('utf-8'))

    signature = hmac.new(
        key=secret.encode('utf-8'),
        msg=f"{encoded_header}.{encoded_payload}".encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()

    encoded_signature = base64url_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def decode_jwt(token, secret, algorithms=['HS256']):
    if 'HS256' not in algorithms:
        raise ValueError("Unsupported algorithm. Only 'HS256' is supported.")

    try:
        encoded_header, encoded_payload, encoded_signature = token.split('.')

        header = json.loads(base64url_decode(encoded_header))
        if header['alg'] != 'HS256':
            return "Invalid token: Unsupported algorithm"

        payload = json.loads(base64url_decode(encoded_payload))
        if payload['exp'] < int(time.time()):
            return "Token has expired"

        signature = hmac.new(
            key=secret.encode('utf-8'),
            msg=f"{encoded_header}.{encoded_payload}".encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()

        valid_signature = base64url_encode(signature)

        if valid_signature != encoded_signature:
            return "Invalid token: Signature verification failed"

        return payload
    except Exception as e:
        return f"Invalid token: {e}"

    

user_data = {
    "user_id": 123,
    "username": "test_user"
}

SECRET_KEY = "srEre32WWww2"

token = generate_jwt(user_data, SECRET_KEY)
print("Generated JWT Token:", token)

decoded_data = decode_jwt(token, SECRET_KEY)
print("Decoded JWT Data:", decoded_data)