import requests

try:
    import json
except ImportError:
    pass


class ApiManager():

    # Initialise the options
    def __init__(self, ip_addr, port, username, password, ssl=True):
        self.ip_addr = ip_addr
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl
        self.rest_params_init()

    # Initialise REST API parameters
    def rest_params_init(self, sub_url='', method='',
                         body=None, content_type='application/json'):
        self.sub_url = sub_url
        self.method = method
        self.body = body
        self.content_type = content_type

    # Create a REST client session.
    def rest_call(self):
        if self.ssl is True:
            base_url = 'https://{}:{}/{}'.format(
                self.ip_addr, self.port, self.sub_url)
        else:
            base_url = 'http://{}:{}/{}'.format(
                self.ip_addr, self.port, self.sub_url)

        if self.body and self.content_type == 'application/json':
            self.body = json.dumps(self.body)

        req = requests.Request(url=base_url, data=self.body)
        req.auth = (self.username, self.password)
        req.headers = ({'Content-Type': '{}'.format(self.content_type),
                        'Accept': '{}'.format(self.content_type)})
        req.method = self.method
        r = req.prepare()

        s = requests.Session()
        try:
            resp = s.send(r, verify=False)
            if resp.ok:
                return json.loads(resp.content)
            else:
                return resp.raise_for_status()
        except requests.HTTPError as e:
            return 'Error: {}'.format(e.args)
        except Exception as e:
            return 'Error: {}'.format(e.args)

    def head(self, sub_url=''):
        self.rest_params_init(sub_url=sub_url, method='HEAD')
        return self.rest_call()

    def get(self, sub_url=''):
        self.rest_params_init(sub_url=sub_url, method='GET')
        return self.rest_call()

    def post(self, sub_url='', body=None):
        self.rest_params_init(sub_url=sub_url, method='POST', body=body)
        return self.rest_call()

    def put(self, sub_url='', body=None):
        self.rest_params_init(sub_url=sub_url, method='PUT', body=body)
        return self.rest_call()

    def patch(self, sub_url='', body=None):
        self.rest_params_init(sub_url=sub_url, method='PATCH', body=body)
        return self.rest_call()

    def delete(self, sub_url=''):
        self.rest_params_init(sub_url=sub_url, method='DELETE')
        return self.rest_call()

# payload = {'kind': 'vm'}

# pc = ApiManager("192.168.2.50","9440","karbon@ukdemo.local","Nutanix123!")
# print(root.post(sub_url='api/nutanix/v3/vms/list', body=payload))
# print(pc.get(sub_url='api/nutanix/v3/vms/d6cae3d8-fe92-4eb1-88f5-ee5bbfe6f6ca'))

# awx = ApiManager("awx.ukdemo.local","80","admin","Nutanix13!",False)
# print(awx.get(sub_url='api/v2/settings/'))