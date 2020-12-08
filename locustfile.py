# locustfile.py
from locust import HttpUser, TaskSet, task
import requests
import urllib
import json


class UserBehavior(TaskSet):
    
    def on_start(self):
        self.login()
        
    def login(self):
        params_token = {
            'client_id': '',
            'client_secret': "",
            'username': '',
            'password': '',
            'auth_host': "",
        }
        
        auth_urls = ""
        client = requests.session()
        client.get(auth_urls)

        csrftoken = client.cookies['csrftoken']
        params_auth = {
            'auth-username': '',
            'auth-password': '',
            'csrfmiddlewaretoken': csrftoken,
            'custom_login_view-current_step': 'auth'
        }
        client.post(auth_urls, data=params_auth, headers={'Referer': auth_urls})

        params_code = {
            'response_type': 'code',
            'state': '' + '/',
            'client_id': params_token['client_id'],
        }
        redirect_uri ='' + '/auth/code'

        r1 = client.get(
            "" + '/o/authorize/?' + urllib.parse.urlencode(params_code) + '&redirect_uri=' + redirect_uri,
            allow_redirects=False
        )
        code = urllib.parse.parse_qs(urllib.parse.urlsplit(r1.headers.get('location')).query)
        # urllib.parse.parse_qs(r1.headers.get('location'))

        params_token = {
            'code': code['code'][0],
            'grant_type': 'authorization_code',
            'client_id': params_token['client_id'],
            'client_secret': params_token['client_secret'],
            'redirect_uri': redirect_uri
        }
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }
        response_token = requests.post("" + '/o/token/', data=urllib.parse.urlencode(params_token), headers=headers)
        headers = {
        'Authorization': f'Bearer {response_token.json()["access_token"]}'
        }
        self.client.post('', headers=headers)
        
        
    @task(1)  
    def index(self):
        self.client.get('/')
        
    @task(2)
    def another_heavy_ajax_url(self):
        # ajax GET
        self.client.post('/category/shops-sales/',
        json={})


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 9000

