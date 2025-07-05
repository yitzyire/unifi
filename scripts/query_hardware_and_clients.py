import json
import requests
import urllib3
import os

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

def get_device_details(udm, site_id, device_id, headers):
    url = f"{udm}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()

def get_device_stats(udm, site_id, device_id, headers):
    url = f"{udm}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/statistics/latest"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()

def get_clients(udm, site_id, headers):
    url = f"{udm}/proxy/network/integration/v1/sites/{site_id}/clients"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()['data']

def get_client_details(udm, site_id, client_id, headers):
    url = f"{udm}/proxy/network/integration/v1/sites/{site_id}/clients/{client_id}"
    r = requests.get(url, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()

def print_device_info(device):
    print(f"\n[Device] {device['name']} ({device['model']})")
    print(f"     IP Address: {device.get('ipAddress', 'N/A')}")
    print(f"     MAC Address: {device.get('macAddress', 'N/A')}")
    print(f"     State: {device.get('state', 'unknown')}")
    print(f"     Firmware: {device.get('firmwareVersion', 'N/A')}")
    print(f"     Uptime: {device.get('uptime', 'N/A')} seconds")

    ports = device.get('interfaces', {}).get('ports', [])
    if ports:
        print("     Ports:")
        for p in ports:
            idx = p.get('idx', 'N/A')
            state = p.get('state', 'N/A')
            speed = p.get('speedMbps', 'N/A')
            poe = p.get('poe', {}).get('state', 'off')
            print(f"      - Port {idx}: {state} | Speed: {speed} Mbps | PoE: {poe}")

    radios = device.get('interfaces', {}).get('radios', [])
    if radios:
        print("     Radios:")
        for r in radios:
            freq = r.get('frequencyGHz', '?')
            std = r.get('wlanStandard', '?')
            ch = r.get('channel', '?')
            width = r.get('channelWidthMHz', '?')
            print(f"      - {std} @ {freq} GHz | Channel {ch} | Width {width} MHz")

def print_device_stats(stats):
    print(f"     Uptime: {stats.get('uptimeSec', 0)} seconds")
    print(f"     CPU Usage: {stats.get('cpuUtilizationPct', 0)}%")
    print(f"     Memory Usage: {stats.get('memoryUtilizationPct', 0)}%")
    print(f"     Load Average: {stats.get('loadAverage1Min')}, {stats.get('loadAverage5Min')}, {stats.get('loadAverage15Min')}")
    uplink = stats.get('uplink', {})
    print(f"     Uplink TX: {uplink.get('txRateBps', 0)} bps | RX: {uplink.get('rxRateBps', 0)} bps")

    radios = stats.get('interfaces', {}).get('radios', [])
    if radios:
        print("     Radios:")
        for r in radios:
            freq = r.get('frequencyGHz')
            retries = r.get('txRetriesPct', 0)
            print(f"      - Frequency: {freq} GHz | TX Retries: {retries}%")

def print_client_details(client):
    print(f"\n[Client] {client.get('name', 'Unnamed')} ({client.get('type')})")
    print(f"     MAC Address: {client.get('macAddress')}")
    print(f"     IP Address: {client.get('ipAddress')}")
    print(f"     Connected At: {client.get('connectedAt')}")
    print(f"     Access Type: {client.get('access', {}).get('type', 'N/A')}")
    print(f"     Uplink Device ID: {client.get('uplinkDeviceId', 'N/A')}")

if __name__ == '__main__':
    try:
        config = load_config()
        UDM = config['udm_url']
        API_KEY = config['api_key']

        headers = {
            'X-API-KEY': API_KEY,
            'Accept': 'application/json',
        }

        sites = get_sites(UDM, headers)

        for site in sites:
            site_id = site['id']
            devices = get_devices(UDM, site_id, headers)
            for device in devices:
                try:
                    details = get_device_details(UDM, site_id, device['id'], headers)
                    print_device_info(details)

                    try:
                        stats = get_device_stats(UDM, site_id, device['id'], headers)
                        print_device_stats(stats)
                    except requests.exceptions.HTTPError:
                        pass
                except requests.exceptions.HTTPError:
                    pass

            clients = get_clients(UDM, site_id, headers)
            for client in clients:
                try:
                    details = get_client_details(UDM, site_id, client['id'], headers)
                    print_client_details(details)
                except requests.exceptions.HTTPError:
                    pass

    except Exception as e:
        print(f"[!] Fatal error: {e}")
