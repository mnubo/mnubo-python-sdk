import requests
import json
import base64
import datetime


def authenticate(func):
    def authenticate_and_call(*args):
        if not args[0].is_access_token_valid():
            args[0].access_token = args[0].fetch_access_token()
        return func(*args)
    return authenticate_and_call


class APIManager(object):

    def __init__(self, client_id, client_secret, hostname):
        """ Initializes the API Manager which is responsible for authenticating every request.

        :param client_id: the client id generated by mnubo
        :param client_secret: the client secret generated by mnubo
        :param hostname: the hostname to send the requests (sandbox or production)
        """

        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__hostname = hostname
        self.access_token = self.fetch_access_token()

    def fetch_access_token(self):
        """ Requests the access token necessary to communicate with the mnubo plateform
        """

        requested_at = datetime.datetime.now()

        r = requests.post(self.get_auth_url(), headers=self.get_token_authorization_header())
        json_response = json.loads(r.content)

        token = {'access_token': json_response['access_token'], 'expires_in': datetime.timedelta(0, json_response['expires_in']), 'requested_at': requested_at}

        return token

    def is_access_token_valid(self):
        """ Validates if the token is still valid

        :return: True of the token is still valid, False if it is expired
        """

        return self.access_token['requested_at'] + self.access_token['expires_in'] > datetime.datetime.now()

    def get_token_authorization_header(self):
        """ Generates the authorization header used while requesting an access token
        """

        return {'content-type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + base64.b64encode(self.__client_id + ":" + self.__client_secret)}

    def get_authorization_header(self):
        """ Generates the authorization header used to access resources via mnubo's API
        """

        return {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.access_token['access_token']}

    def get_api_url(self):
        """ Generates the general API url
        """

        return self.__hostname + '/api/v3/'

    def get_auth_url(self):
        """ Generates the url to fetch the access token
        """

        return self.__hostname + '/oauth/token?grant_type=client_credentials'

    @authenticate
    def get(self, route, params={}):
        """ Build and send a get request authenticated

        :param route: which resource to access via the REST API
        """

        url = self.get_api_url() + route
        headers = self.get_authorization_header()
        return requests.get(url, params=params, headers=headers)

    @authenticate
    def post(self, route, body={}):
        """ Build and send a post request authenticated

        :param route: which resource to access via the REST API
        :param body: body to be appended to the HTTP request
        """

        url = self.get_api_url() + route
        headers = self.get_authorization_header()
        return requests.post(url, data=body, headers=headers)

    @authenticate
    def put(self, route, body={}, json_encoded=True):
        """ Build and send a put request authenticated

        :param route: which resource to access via the REST API
        :param body: body to be appended to the HTTP request
        :param json_encoded: send the request using json body
        """

        url = self.get_api_url() + route
        headers = self.get_authorization_header()

        if json_encoded:
            return requests.put(url, json=body, headers=headers)
        else:
            return requests.put(url, data=body, headers=headers)

    @authenticate
    def delete(self, route):
        """ Build and send a delete request authenticated

        :param route: which resource to access via the REST API
        """

        url = self.get_api_url() + route
        headers = self.get_authorization_header()
        return requests.delete(url, headers=headers)
