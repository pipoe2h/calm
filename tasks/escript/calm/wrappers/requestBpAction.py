#script
jwt = '@@{calm_jwt}@@'
appUuid = '@@{POSH_APP_UUID}@@'

payload = {
    "name": "AZ Deploy VM",
    "args": [
        {
            "name": "AC_AZURE_LOCATION_NAME",
            "value": "@@{AC_AZURE_LOCATION_NAME}@@"
        },
        {
            "name": "AC_AZURE_VM_USER_PASSWORD",
            "value": "@@{CRED.secret}@@"
        },
        {
            "name": "AC_AZURE_VM_USERNAME",
            "value": "@@{CRED.username}@@"
        },
        {
            "name": "AC_AZURE_VM_IMAGE",
            "value": "@@{AC_AZURE_VM_IMAGE}@@"
        },
        {
            "name": "AC_AZURE_VM_NAME",
            "value": "@@{AC_AZURE_VM_NAME}@@"
        },
        {
            "name": "AC_AZURE_RG_NAME",
            "value": "@@{AC_AZURE_RG_NAME}@@"
        }
    ]
}

api_url = 'https://localhost:9440/api/nutanix/v3/apps/%s/actions/run' % appUuid
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

r = urlreq(api_url, verb='POST', params=json.dumps(payload), headers=headers, verify=False)

if r.ok:
    print "TASK_ID={0}".format(json.loads(r.content)['runlog_uuid'])
    exit(0)
else:
    print "Post request failed", r.content
    exit(1)
