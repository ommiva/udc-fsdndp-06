from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

import json

AUTH0_DOMAIN = 'omv-fsnd-casting.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagency'


# AuthError Exception

class AuthError(Exception):
    """
    AuthError Exception
    Standarized way to communicate auth falure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Authorization header
def get_token_auth_header():
    """
    Authorization header validation
    - if no header is present raises AuthError
    - From request header
        - split bearer and header
        - if header malformed raises AuthError
        - if no bearer raises AuthError
    Returns token part of header
    """
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    auth_header = request.headers['Authorization']
    parts = auth_header.split(' ')

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header is expected.'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header MUST be bearer token.'
        }, 401)

    return parts[1]


def check_permission(permission, payload):
    """
    Validates permission to execute route
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permission not in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 403)

    return True


def verify_decode_jwt(token):
    """
    Validates JWT token
    """
    url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    jsonUrl = urlopen(url)

    jwks = json.loads(jsonUrl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            description = 'Incorrect claims.'
            + 'Please, check the audience and user.'
            raise AuthError({
                'code': 'token_claims',
                'description': description
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse atuhentication token.'
            }, 401)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropiate key.'
    }, 401)


def requires_auth(permission=''):
    """
    Implements @requires_auth(permission) decorator.

    - Uses get_token_auth_header method to get the token
    - Uses verify_decode_jwt to decode jwt
    - Uses check_permission to validate claims anc check
      requested permissions
    Return  decoded payload
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # print("--- Wrapper")
            token = get_token_auth_header()
            # print("--- Token ", token)
            payload = verify_decode_jwt(token)
            # print("--- Payload ", payload)
            # print("--- Permission ", permission)
            check_permission(permission, payload)

            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
