#script
# Search VM IP address within the Calm application logs

jwt = '@@{calm_jwt}@@'
appUuid = '@@{POSH_APP_UUID}@@'
api_url = 'https://localhost:9440/api/nutanix/v3/apps/%s/app_runlogs/' % appUuid
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

actionParentReference = ''
actionData = ''

payload = {
    "filter": "application_reference==@@{POSH_APP_UUID}@@;(type==action_runlog,type==audit_runlog)"
}

r = urlreq(api_url + 'list', verb='POST', params=json.dumps(payload), headers=headers, verify=False)

entities = json.loads(r.content)['entities']

if r.ok:

    for entity in entities:
    
        if entity['metadata']['uuid'] == '@@{TASK_ID}@@':
    
            actionName = entity['status']['action_reference']['name'] 
        
            if actionName == 'AZ Deploy VM':
        
                actionParentReference = entity['metadata']['uuid']
                actionData = '{{"filter": "root_reference=={0}"}}'.format(actionParentReference)
            
                r = urlreq(api_url + 'list', verb='POST', params=actionData, headers=headers, verify=False)
            
                entities = json.loads(r.content)['entities']
                
                for entity in entities:
                    
                    if 'task_reference' in entity['status']:
                        
                        taskName = entity['status']['task_reference']['name']
                        taskUuid = entity['metadata']['uuid']
                    
                        r = urlreq(api_url + taskUuid + '/output', verb='GET', headers=headers, verify=False)
                        
                        outputList = json.loads(r.content)['status']['output_list']
                        output = outputList[0]['output']
                        print "VM_IP={0}".format(output.rstrip())
    exit(0)
else:
    print "Post request failed", r.content
    exit(1)
