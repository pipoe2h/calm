nsx_admin = '@@{nsx_admin}@@'
nsx_password = '@@{nsx_password}@@'
nsx_ip = '@@{nsx_mgr_ip}@@'
tenant_uuid = '@@{TENANT_UUID}@@'

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
                   "id": "{}".format(nsx_edge_cluster_uuid),
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
                  "id": "{}-{}".format(tenant_uuid,segment_name),
                  "description": "{}-{}".format(tenant_uuid,segment_name),
                  "display_name": "{}-{}".format(tenant_uuid,segment_name),
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