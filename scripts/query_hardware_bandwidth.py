import json
import requests
import urllib3
import os
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_config():
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
        return json.load(f)

def get_sites(udm, headers):
    url = f"{udm}/proxy/network/integration/v1/sites"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()['data']

def get_devices(udm, site_id, headers):
    url = f"{udm}/proxy/network/integration/v1/sites/{site_id}/devices"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()['data']

def get_device_stats(udm, site_id, device_id, headers):
    url = f"{udm}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/statistics/latest"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()

def format_mbps(bps):
    return f"{bps / 1_000_000:.2f} Mbps"

def print_bandwidth_table(device_stats):
    print(f"{'Device':<32} {'TX':>10} {'RX':>10}")
    print("-" * 54)
    for name, stats in device_stats:
        uplink = stats.get('uplink', {})
        tx = format_mbps(uplink.get('txRateBps', 0))
        rx = format_mbps(uplink.get('rxRateBps', 0))
        print(f"{name:<32} {tx:>10} {rx:>10}")

if __name__ == '__main__':
    try:
        config = load_config()
        UDM = config['udm_url']
        API_KEY = config['api_key']

        headers = {
            'X-API-KEY': API_KEY,
            'Accept': 'application/json',
        }

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            device_stats = []

            sites = get_sites(UDM, headers)
            for site in sites:
                site_id = site['id']
                devices = get_devices(UDM, site_id, headers)
                for device in devices:
                    try:
                        stats = get_device_stats(UDM, site_id, device['id'], headers)
                        device_stats.append((device['name'], stats))
                    except requests.exceptions.HTTPError:
                        pass

            print_bandwidth_table(device_stats)
            time.sleep(2)

    except Exception as e:
        print(f"[!] Fatal error: {e}")
