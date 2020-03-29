nsx_admin = '@@{nsx_admin}@@'
nsx_password = '@@{nsx_password}@@'
nsx_ip = '@@{nsx_mgr_ip}@@'
tenant_uuid = '@@{TENANT_UUID}@@'
group_name = '@@{nsgroup_name}@@'

headers = {'Content-Type': 'application/json',  'Accept':'application/json'}

payload = {
    "resource_type": "Infra",
    "id": "infra",
    "children": [
      { 
        "resource_type": "ChildDomain",
        "marked_for_delete": "false",
        "Domain":{ 
           "id": "default",
           "resource_type": "Domain",
           "marked_for_delete": "false",
           "children":[ 
              { 
                 "resource_type": "ChildGroup",
                 "Group":{ 
                    "resource_type": "Group",
                    "marked_for_delete": "false",
                    "id": "{}-{}".format(tenant_uuid, group_name),
                    "display_name": "{}-{}".format(tenant_uuid, group_name),
                    "tags": [
                        {"scope": "calm", "tag": "{}".format(tenant_uuid)}
                    ],
                      "expression": [
                        {
                          "expressions": [
                            {
                              "member_type": "VirtualMachine",
                              "key": "Tag",
                              "operator": "EQUALS",
                              "value": "{}|{}".format(tenant_uuid, group_name),
                              "resource_type": "Condition",
                              "marked_for_delete": "false"
                            },
                            {
                              "conjunction_operator": "AND",
                              "resource_type": "ConjunctionOperator",
                              "marked_for_delete": "false",
                            },
                            {
                              "member_type": "VirtualMachine",
                              "key": "Tag",
                              "operator": "EQUALS",
                              "value": "calm|{}".format(tenant_uuid),
                              "resource_type": "Condition",
                              "marked_for_delete": "false",
                            }
                          ],
                          "resource_type": "NestedExpression",
                          "marked_for_delete": "false",
                        }
                      ]
                 }
              }
           ]
        }
      }
    ],
    "marked_for_delete": "false",
    "connectivity_strategy": "WHITELIST"
}

api_action = '/policy/api/v1/infra'
url = 'https://{}{}'.format(
    nsx_ip,
    api_action
)

r = urlreq(
    url,
    verb='PATCH',
    auth='BASIC', 
    user=nsx_admin, 
    passwd=nsx_password, 
    params=json.dumps(payload),
    headers=headers,
    verify=False
)

if r.ok:
    exit(0)
else:
    print "Post request failed", r.content
    exit(1)