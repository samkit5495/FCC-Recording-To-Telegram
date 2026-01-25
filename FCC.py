import requests
import urllib
from dotenv import dotenv_values

class FCC:

    base_url = 'https://www.freeconferencecall.com/api/'

    def call(self, req_type, url, data={}):
        if req_type =='post':
            return requests.post(self.base_url+url,data=data, headers={
                'Authorization':'Bearer '+self.access_token
            }).json()
        elif req_type=='get':
            return requests.get(self.base_url+url+'?'+urllib.parse.urlencode(data), headers={
                'Authorization':'Bearer '+self.access_token
            }).json()
        elif req_type=='delete':
            return requests.delete(self.base_url+url, headers={
                'Authorization':'Bearer '+self.access_token
            }).json()

    def __init__(self, client_id, client_secret, username, password, auto_renew=True):
        self.username = username
        self.password = password
        self.auto_renew = auto_renew
        
        resp = requests.post(self.base_url+'v4/token',{
            'grant_type':'password',
            'client_id':client_id,
            'client_secret':client_secret,
            'username':username,
            'password':password
        }).json()
        print(resp)
        
        # Check for invalid credentials
        if 'error' in resp and resp['error'] == 'invalid_client' and self.auto_renew:
            print("Invalid credentials detected. Attempting to renew...")
            
            try:
                from renew_credentials import FCCCredentialRenewer
                renewer = FCCCredentialRenewer()
                renewal_success = renewer.renew_credentials()
                
                if renewal_success:
                    print("Credentials renewed successfully. Retrying authentication...")
                    
                    # Reload config with new credentials
                    config = dotenv_values(".env")
                    client_id = config['client_id']
                    client_secret = config['client_secret']
                    
                    # Retry authentication with new credentials
                    resp = requests.post(self.base_url+'v4/token',{
                        'grant_type':'password',
                        'client_id':client_id,
                        'client_secret':client_secret,
                        'username':username,
                        'password':password
                    }).json()
                    print("Authentication retry response:", resp)
                else:
                    raise Exception("Credential renewal failed")
            except Exception as e:
                raise Exception(f"Failed to renew credentials: {str(e)}")
        
        if 'access_token' not in resp:
            raise Exception(f"Authentication failed: {resp}")
        
        self.access_token = resp['access_token']

    def getConferences(self):
        resp = self.call('get', 'v4/conferences', {
            'has_recordings':'true',
            'order_by':'start_date',
            'order':'DESC'
        })
        return resp['conferences']
    
    def deleteConference(self, id):
        resp = self.call('delete', 'v4/conferences/{0}'.format(id))
        return resp
