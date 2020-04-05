# REST API call

# setup common variables
api_host = '@@{API_HOST}@@'
username = '@@{CREDS_API.username}@@'
password = '@@{CREDS_API.secret}@@'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
verify_ssl = False

###################### DEFINE FUNCTIONS ######################

def rest_call( url, method, payload="", username, password, headers, ssl ):

    resp = urlreq(
        url,
        verb = method,
        params = json.dumps(payload),
        auth = "BASIC",
        user = username,
        passwd = password,
        headers = headers,
        verify = ssl
        )

    if resp.ok:
        return resp
    else:
        print("Request failed")
        print("Headers: {}".format(headers))
        print("Payload: {}".format(json.dumps(payload)))
        print('Status code: {}'.format(resp.status_code))
        print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
        exit(1)

##############################################################

###################### EXAMPLES ######################

##### 1. Mock API (mocky.io) #####
base_url = 'https://{}/'.format(api_host)
endpoint = 'v2'

url = '{}/{}'.format(
    base_url,
    endpoint
)

method = 'GET'

response = rest_call(url, method, '', username, password, headers, ssl)
print response
##################################
######################################################



url = "https://{}/PrismGateway/services/rest/v2.0/protection_domains/{}/dr_snapshots?proxyClusterUuid={}".format(
    uri,
    hostname,
    cluster_uuid
)

method = 'GET'

response = rest_call(url=url,method=method)
entities = response['entities']

snapshot_list = []

# create list of all snapshot ids
for entity in entities:

    snapshot_list.append(entity['snapshot_id'])

# sort list of snaps descending
snapshot_list.sort(reverse=True)

print(','.join(snapshot_list))