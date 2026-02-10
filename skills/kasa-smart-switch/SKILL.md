---
name: kasa-smart-switch
description: Control TP-Link Kasa smart devices (switches, plugs, bulbs). Use when user wants to control smart home devices, turn lights/switches on/off, check device status, monitor energy usage, or discover/manage Kasa smart devices on the network. Supports device discovery, power control, status checking, energy monitoring, and brightness/color control for compatible bulbs.
---

# Kasa Smart Switch Control

Control TP-Link Kasa smart home devices (smart switches, plugs, bulbs, dimmers, light strips) via local network.

## Quick Start

All control operations use the `kasa_control.py` script in the `scripts/` directory.

### Discover Devices

```bash
python3 scripts/kasa_control.py list
```

This scans the network and shows all available devices with their names, IP addresses, and current states.

### Control Devices

```bash
# Turn on a device by name
python3 scripts/kasa_control.py --device "Living Room Light" on

# Turn off by IP address
python3 scripts/kasa_control.py --host 192.168.1.100 off

# Toggle a device
python3 scripts/kasa_control.py --device "Kitchen Outlet" toggle
```

### Check Status

```bash
# Get device status (includes energy usage if supported)
python3 scripts/kasa_control.py --device "Bedroom Lamp" status

# Get JSON output for parsing
python3 scripts/kasa_control.py --device "Kitchen Outlet" status --json
```

## Features

### Device Discovery
- Auto-discovers all Kasa devices on the local network
- No manual IP configuration needed
- Finds devices by broadcast discovery

### Power Control
- **Turn on/off** - Direct power control
- **Toggle** - Flip current state
- **Status check** - Get current on/off state

### Energy Monitoring
For devices with energy monitoring capability (smart plugs with emeter):
- Real-time power consumption (watts)
- Voltage and current readings
- Total energy usage (kWh)

### Smart Bulb Features
For Kasa smart bulbs:
- Brightness control
- Color temperature adjustment
- HSV color control (for color bulbs)

## Device Identification

Use either method:
- **By name**: `--device "Living Room Light"` (case-insensitive)
- **By IP**: `--host 192.168.1.100` (direct connection)

Device names match the aliases configured in the Kasa app.

## Technical Details

### Requirements
- `python-kasa` library (install with: `pip3 install python-kasa`)
- Python 3.8+
- Local network access to devices
- Devices must be on the same network/VLAN

### Network Discovery
Uses UDP broadcast (255.255.255.255) to discover devices. If devices aren't found:
- Ensure devices are on the same network
- Check firewall rules allow UDP broadcast
- Try increasing timeout: `--timeout 10`
- Use direct IP connection: `--host <ip>`

### Device Types Supported
- Smart Plugs (HS100, HS103, HS105, KP115, etc.)
- Smart Switches (HS200, HS210, KS200, KS230, etc.)
- Smart Bulbs (KL110, KL120, KL125, KL130, etc.)
- Smart Dimmers (HS220, KS220, etc.)
- Smart Light Strips (KL400, KL430, etc.)
- Power Strips (HS300, KP400, etc.)

## Common Workflows

### Morning Routine
```bash
# Turn on multiple lights
python3 scripts/kasa_control.py --device "Kitchen Light" on
python3 scripts/kasa_control.py --device "Living Room" on
```

### Check Energy Usage
```bash
# Monitor high-power devices
python3 scripts/kasa_control.py --device "Heater Outlet" status --json | jq '.emeter'
```

### Evening Automation
```bash
# Turn off all devices (requires device list)
python3 scripts/kasa_control.py list --json | \
  jq -r '.[].alias' | \
  while read device; do
    python3 scripts/kasa_control.py --device "$device" off
  done
```

### Quick Toggle
```bash
# Toggle without knowing current state
python3 scripts/kasa_control.py --device "Desk Lamp" toggle
```

## Troubleshooting

**No devices found?**
- Devices must be on the same network
- Increase discovery timeout: `--timeout 15`
- Try connecting by IP: `--host 192.168.1.X`
- Check if devices are powered on
- Verify firewall allows local network discovery

**Device not responding?**
- Check device is online in Kasa app
- Verify IP address hasn't changed
- Try power cycling the device
- Ensure no network isolation between host and device

**Energy data not available?**
- Not all devices support energy monitoring
- Check `has_emeter: true` in status output
- Only certain plug models have this feature

## Future Enhancements

Possible additions based on user needs:
- Scheduling and automation rules
- Scene/preset management
- Bulk device operations
- Integration with other smart home systems
- Historical energy usage tracking
- Voice command integration

## Reference

See `references/api_guide.md` for detailed API information and advanced usage patterns.
