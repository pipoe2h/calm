nsx_admin = '@@{nsx_admin}@@'
nsx_password = '@@{nsx_password}@@'
nsx_ip = '@@{nsx_mgr_ip}@@'
tenant_uuid = '@@{TENANT_UUID}@@'
nsx_dfw_rulename = '@@{nsx_dfw_rulename}@@'
nsx_dfw_sourcegroup = '@@{nsx_dfw_sourcegroup}@@'
nsx_dfw_destinationgroup = '@@{nsx_dfw_destinationgroup}@@'
nsx_dfw_action = '@@{nsx_dfw_action}@@'
nsx_dfw_logging = '@@{nsx_dfw_logging}@@'
nsx_dfw_direction = '@@{nsx_dfw_direction}@@'
nsx_dfw_ipversion = '@@{nsx_dfw_ipversion}@@'
nsx_dfw_sequence = '@@{nsx_dfw_sequence}@@'
nsx_dfw_sourcesexcluded = '@@{nsx_dfw_sourcesexcluded}@@'
nsx_dfw_destinationsexcluded = '@@{nsx_dfw_destinationsexcluded}@@'
nsx_dfw_services = '@@{nsx_dfw_services}@@'
nsx_dfw_profiles = '@@{nsx_dfw_profiles}@@'
nsx_dfw_disabled = '@@{nsx_dfw_disabled}@@'
nsx_dfw_notes = '@@{nsx_dfw_notes}@@'

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
                 "resource_type": "ChildSecurityPolicy",
                 "marked_for_delete": "false",
                 "SecurityPolicy":{
                    "resource_type": "SecurityPolicy",
                    "category": "Application",
                    "marked_for_delete": "false",
                    "id": "{}-POLICY".format(tenant_uuid),
                    "display_name": "{}-POLICY".format(tenant_uuid),
                    "tags": [
                        {"scope": "calm", "tag": "{}".format(tenant_uuid)}
                    ],
                    "rules": [
                        {
                            "sequence_number": int(nsx_dfw_sequence),
                            "sources_excluded": "{}".format(nsx_dfw_sourcesexcluded),
                            "destinations_excluded": "{}".format(nsx_dfw_destinationsexcluded),
                            "source_groups": [
                              "/infra/domains/default/groups/{}-{}".format(tenant_uuid,nsx_dfw_sourcegroup)
                            ],
                            "destination_groups": [
                              "/infra/domains/default/groups/{}-{}".format(tenant_uuid,nsx_dfw_destinationgroup)
                            ],
                            "services": [
                              "{}".format(nsx_dfw_services)
                            ],
                            "profiles": [
                              "{}".format(nsx_dfw_profiles)
                            ],
                            "action": "{}".format(nsx_dfw_action),
                            "logged": "{}".format(nsx_dfw_logging),
                            "scope": [
                              "/infra/domains/default/groups/{}-TENANT".format(tenant_uuid)
                            ],
                            "disabled": "{}".format(nsx_dfw_disabled),
                            "notes": "{}".format(nsx_dfw_notes),
                            "direction": "{}".format(nsx_dfw_direction),
                            "tags": [
                                {
                                    "scope": "calm",
                                    "tag": "{}".format(tenant_uuid)
                                }
                            ],
                            "ip_protocol": "{}".format(nsx_dfw_ipversion),
                            "resource_type": "Rule",
                            "id": "{}-{}-{}".format(tenant_uuid,nsx_dfw_action,nsx_dfw_rulename),
                            "display_name": "{}-{}-{}".format(tenant_uuid,nsx_dfw_action,nsx_dfw_rulename),
                            "marked_for_delete": "false"
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
    print("Request successful")
    exit(0)
else:
    print "Post request failed", r.content
    exit(1)