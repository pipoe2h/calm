#script
jwt = '@@{calm_jwt}@@'
runlogUuid = '@@{TASK_ID}@@'
appUuid = '@@{POSH_APP_UUID}@@'

payload = {}
api_url = 'https://localhost:9440/api/nutanix/v3/apps/%s/app_runlogs/%s' % (appUuid, runlogUuid)
headers = {'Content-Type': 'application/json',  'Accept':'application/json', 'Authorization': 'Bearer {}'.format(jwt)}

state = 'SUCCESS'

# Monitor the operation
for x in range(20):
  r = urlreq(api_url, verb='GET', params=json.dumps(payload), headers=headers, verify=False)
  
  print json.loads(r.content)
  
  # If complete, break out of loop
  if json.loads(r.content)['status']['state'] == state:
    print "Task finished."
    break
  
  print "Sleeping for 45 seconds."
  print "Status: {0}".format(json.loads(r.content)['status']['state'])
  sleep(45)  
  
# If the operation did not complete within 20 minutes, assume it's not successful and error out
if json.loads(r.content)['status']['state'] != state:
  print "Stopping timed out", json.dumps(json.loads(r.content), indent=4)
  exit(1)
