# UniFi API Tool – Python Scripts

This project uses the UniFi Network API (via the UDM local interface) to query device and client information, including real-time bandwidth usage.

---

## Features

### 1. Device Details Script

- Lists all sites
- Retrieves all devices per site
- Fetches:
  - Device metadata (model, IP, MAC, firmware, port status)
  - Device statistics (uptime, CPU, memory, load averages)
  - Interfaces (ports and radios)
- Fetches all connected clientss
- Retrieves full client details (MAC, IP, connection time, uplink device)

### 2. Live Bandwidth Script

- Every X seconds:
  - Retrieves TX/RX bandwidth per device (in Mbps)
  - Displays results in a clean, formatted table

---

## API Endpoints Used

- `GET /proxy/network/integration/v1/sites`
- `GET /proxy/network/integration/v1/sites/{siteId}/devices`
- `GET /proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}`
- `GET /proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}/statistics/latest`
- `GET /proxy/network/integration/v1/sites/{siteId}/clients`
- `GET /proxy/network/integration/v1/sites/{siteId}/clients/{clientId}`

All requests use the `X-API-KEY` header for authentication and run against a local UniFi UDM IP (`https://IPADDRESS` by default).

---

## How to Get Required IDs

### Site ID

- Call: `GET /proxy/network/integration/v1/sites`
- Use the `id` field from the first `data[]` object

### Device ID

- Call: `GET /proxy/network/integration/v1/sites/{siteId}/devices`
- Use each device’s `id` value

### Client ID

- Call: `GET /proxy/network/integration/v1/sites/{siteId}/clients`
- Use each client's `id` value

---

## Configuration

Create a `config.json` file in the same directory as the scripts:

```json
{
  "api_key": "YOUR_API_KEY",
  "udm_url": "https://IPADDRESS"
}
```

---

## Running

### Device + Client Details Script

```bash
python device_details.py
```

### Live Bandwidth Monitor (2s refresh)

```bash
python bandwidth_monitor.py
```
