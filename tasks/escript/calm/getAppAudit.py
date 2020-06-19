api_url = 'https://localhost:9440/api/nutanix/v3/apps/@@{calm_application_uuid}@@/app_runlogs/list'
headers = {'Content-Type': 'application/json'}

username = '@@{Cred_PC.username}@@'
password = '@@{Cred_PC.secret}@@'

payload = {"filter":"application_reference==@@{calm_application_uuid}@@;(type==action_runlog)"}

r = urlreq(api_url, verb='POST', auth='BASIC', user=username, passwd=password, params=json.dumps(payload), headers=headers)

if r.ok:
    resp = json.loads(r.content)
    
    headers = {'Accept-Encoding': 'gzip, deflate, br'}
    api_url = 'https://localhost:9440/api/nutanix/v3/apps/@@{calm_application_uuid}@@/app_runlogs/{}/output/download'.format(resp['entities'][0]['metadata']['uuid'])
    
    r = urlreq(api_url, verb='GET', auth='BASIC', user=username, passwd=password, headers=headers)
    if r.ok:
        base64_file = base64.b64encode(r.content)
        """base64_file contains an encoded ZIP file"""

    else:
        print("Post request failed", r.content)
        exit(1)    
    
else:
    print("Post request failed", r.content)
    exit(1)