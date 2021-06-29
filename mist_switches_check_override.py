"""
Script written by Frederic Maladri
Last update on 06-28-2021

this script search and list switches in a Mist organization which have overrides
"""
import time
import json
import requests
import argparse

def find_switchs_with_overrides(configs):
    org_id = configs['api']['org_id']
    token = configs['api']['token']
    mist_url = configs['api']['mist_url']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(token)}

    api_url = '{0}orgs/{1}/inventory?type=switch'.format(mist_url, org_id)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        switches = json.loads(response.content.decode('utf-8'))

        print('\n** Listing switches which contains overrides\n')
        print('----------')
        for switch in switches:
            print('Switch Name : {}'.format(switch['name']))
            print('Switch ID : {}'.format(switch['id']))
            print('Switch Site ID : {}'.format(switch['site_id']))
            api_url = '{0}sites/{1}/devices/{2}'.format(mist_url, switch['site_id'], switch['id'])
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                switch_config = json.loads(response.content.decode('utf-8'))
                NbrOfOverrides = 0
                parameters = ['networks', 'ntp_servers', 'dns_servers', 'dns_suffix', 'port_config', 'port_usages',
                              'extra_routes', 'router_id', 'ospf_config', 'dhcpd_config', 'dhcp_snooping', 'vrrp_config',
                              'vrf_config', 'radius_config', 'additional_config_cmds']
                overrides = {}
                for parameter,value in switch_config.items():
                   for item in parameters:
                       if item == parameter and value:
                           if (str(value) == "['']"):
                               IsOverrided = False
                           else:
                               if value is not None:
                                   NbrOfOverrides = NbrOfOverrides + 1
                                   IsOverrided = True
                                   overrides[parameter] = value

                if (NbrOfOverrides > 0) or (IsOverrided):
                   print('\nThe configuration of this switch has been overrided with {} override(s)'.format(NbrOfOverrides))
                   print(overrides)
                else:
                   print('\nThe configuration of this switch has NOT been overrided')
                print('----------\n')

def main():
    parser = argparse.ArgumentParser(description='Check and list the switches containing overrides in a specific Mist Organization')
    parser.add_argument('config', metavar='config_file.json', type=argparse.FileType('r'), help='file containing all the configuration information (Mist Org ID, API Token & Mist URL API)')
    args = parser.parse_args()
    configs = json.load(args.config)

    find_switchs_with_overrides(configs)


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))
