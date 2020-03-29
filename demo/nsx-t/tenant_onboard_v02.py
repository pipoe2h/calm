nsx_admin = '@@{cred_nsx_api.username}@@'
nsx_password = '@@{cred_nsx_api.secret}@@'
nsx_ip = '@@{nsx_mgr_ip}@@'
nsx_dhcp = '@@{NSX_DHCP_SERVER}@@'
nsx_tier0_id = '@@{t0Id}@@'
tenant_uuid = '@@{TENANT_UUID}@@'
nsx_edge_cluster_uuid = '@@{ecUuid}@@'
nsx_ipam_gw = '@@{defaultGwIp}@@'
nsx_ipam_range = '@@{dhcp_range}@@'
nsx_ipam_cidr = '@@{network_cidr}@@'
nsx_tz_uuid = '@@{tzUuid}@@'

headers = {'Content-Type': 'application/json',  'Accept':'application/json'}

payload = {
    "resource_type": "Infra",
    "id": "infra",
    "children": [
      {
        "Tier1": {
          "tier0_path": "/infra/tier-0s/{}".format(nsx_tier0_id),
          "failover_mode": "NON_PREEMPTIVE",
          "dhcp_config_paths": [
              "/infra/dhcp-server-configs/{}".format(nsx_dhcp)
          ],
          "force_whitelisting": "false",
          "default_rule_logging": "false",
          "disable_firewall": "false",
          "resource_type": "Tier1",
          "id": "{}-tier-1-gw".format(tenant_uuid),
          "description": "{}-tier-1-gw".format(tenant_uuid),
          "display_name": "{}-tier-1-gw".format(tenant_uuid),
          "route_advertisement_types": [
              "TIER1_CONNECTED",
              "TIER1_STATIC_ROUTES"
          ],
          "tags": [
            {"scope": "calm", "tag": "{}".format(tenant_uuid)}
          ],
          "children": [
            { 
                "resource_type": "ChildLocaleServices",
                "LocaleServices":{ 
                   "resource_type": "LocaleServices",
                   "id": "default",
                   "edge_cluster_path": "/infra/sites/default/enforcement-points/default/edge-clusters/{}".format(nsx_edge_cluster_uuid)
                }
             },
            {
                "Segment": {
                  "subnets": [
                    {
                      "gateway_address": "{}".format(nsx_ipam_gw),
                      "dhcp_ranges": [
                          "{}".format(nsx_ipam_range)
                      ],
                      "network": "{}".format(nsx_ipam_cidr)
                    }
                  ],
                  "resource_type": "Segment",
                  "id": "{}-segment-default".format(tenant_uuid),
                  "description": "{}-segment-default".format(tenant_uuid),
                  "display_name": "{}-segment-default".format(tenant_uuid),
                  "transport_zone_path": "/infra/sites/default/enforcement-points/default/transport-zones/{}".format(nsx_tz_uuid),
                  "tags": [
                    {"scope": "calm", "tag": "{}".format(tenant_uuid)}
                  ],
                  "marked_for_delete": "false"
                },
                "resource_type": "ChildSegment",
                "marked_for_delete": "false"
            }
          ],
          "marked_for_delete": "false"
        },
        "resource_type": "ChildTier1",
        "marked_for_delete": "false"
      },
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
                    "id": "{}-TENANT".format(tenant_uuid),
                    "display_name": "{}-TENANT".format(tenant_uuid),
                    "tags": [
                        {"scope": "calm", "tag": "{}".format(tenant_uuid)}
                    ],
                    "expression": [
                        {
                          "member_type": "VirtualMachine",
                          "key": "Name",
                          "operator": "STARTSWITH",
                          "value": "{}".format(tenant_uuid),
                          "resource_type": "Condition",
                          "marked_for_delete": "false"
                        },
                        {
                          "conjunction_operator": "OR",
                          "resource_type": "ConjunctionOperator",
                          "marked_for_delete": "false"
                        },
                        {
                          "member_type": "LogicalSwitch",
                          "key": "Tag",
                          "operator": "EQUALS",
                          "value": "calm|{}".format(tenant_uuid),
                          "resource_type": "Condition",
                          "marked_for_delete": "false"
                        }
                    ]
                 }
              },
              {
                 "resource_type": "ChildSecurityPolicy",
                 "marked_for_delete": "false",
                 "SecurityPolicy":{
                    "resource_type": "SecurityPolicy",
                    "category": "Environment",
                    "marked_for_delete": "false",
                    "id": "{}-POLICY".format(tenant_uuid),
                    "display_name": "{}-POLICY".format(tenant_uuid),
                    "tags": [
                        {"scope": "calm", "tag": "{}".format(tenant_uuid)}
                    ],
                    "rules": [
                        {
                            "sequence_number": 10,
                            "sources_excluded": "false",
                            "destinations_excluded": "false",
                            "source_groups": [
                              "/infra/domains/default/groups/{}-TENANT".format(tenant_uuid)
                            ],
                            "destination_groups": [
                              "ANY"
                            ],
                            "services": [
                              "ANY"
                            ],
                            "profiles": [
                              "ANY"
                            ],
                            "action": "ALLOW",
                            "logged": "false",
                            "scope": [
                              "/infra/domains/default/groups/{}-TENANT".format(tenant_uuid)
                            ],
                            "disabled": "false",
                            "notes": "",
                            "direction": "IN_OUT",
                            "tags": [
                                {
                                    "scope": "calm",
                                    "tag": "{}".format(tenant_uuid)
                                }
                            ],
                            "ip_protocol": "IPV4_IPV6",
                            "resource_type": "Rule",
                            "id": "{}-ALLOW-OUT".format(tenant_uuid),
                            "display_name": "{}-ALLOW-OUT".format(tenant_uuid),
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
    exit(0)
else:
    print "Post request failed", r.content
    exit(1)