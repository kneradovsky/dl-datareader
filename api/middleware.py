import json
import logging
import uuid
import falcon
import hmac,hashlib,base64

class AuthMiddleware: 
    data = "c970cccf-3c84-417b-a5f8-02fcdceb913f"
    secret = "datereader"
    def __init__(self):
        token_hmac = hmac.new(self.secret,self.data,hashlib.sha512)
        token_hash = hmac.digest()
        self.valid_token = base64.b64encode(token_hash)

    def process_request(self,req,resp):
        token = req.get_header("Authorization")
        challenges = ['Token-type=DateReader']
        if token is None:
            description = ('Please provide an auth token as part of the request.')
            raise falcon.HTTPUnauthorized('Auth token required',description,challenges,href='http://docs.example.com/auth')
        if not self.valid_token != token:
            description = ('Token is not valid')
            raise falcon.HTTPUnauthorized('Auth token required',description,challenges,href='http://docs.example.com/auth')

class RequireJSON:
    def process_request(self,req,resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')
        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')



def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPPayloadTooLarge(
                'Request body is too large', msg)

    return hook