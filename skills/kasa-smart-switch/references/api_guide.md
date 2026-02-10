# Kasa API Reference Guide

Detailed technical information for working with TP-Link Kasa smart devices.

## Python-Kasa Library

The `python-kasa` library provides async Python interface to Kasa devices.

### Basic Usage Pattern

```python
import asyncio
from kasa import Discover

async def main():
    # Discover all devices
    devices = await Discover.discover()
    
    for addr, device in devices.items():
        await device.update()  # Fetch current state
        print(f"{device.alias}: {device.is_on}")
        
        # Control device
        await device.turn_on()
        await device.turn_off()
        await device.toggle()

asyncio.run(main())
```

### Device Discovery

```python
# Network-wide discovery (broadcast)
devices = await Discover.discover(timeout=10)

# Single device by IP
device = await Discover.discover_single("192.168.1.100")

# Specific network target
devices = await Discover.discover(target="192.168.1.255", timeout=5)
```

### Device Properties

All devices have these common properties:
- `alias` - Device name (string)
- `host` - IP address (string)
- `model` - Device model (string)
- `is_on` - Current state (boolean)
- `device_type` - Type enum
- `has_emeter` - Energy monitoring capability (boolean)

### Energy Monitoring

For devices with emeter capability:

```python
if device.has_emeter:
    # Real-time data
    emeter = await device.get_emeter_realtime()
    print(f"Power: {emeter['power_mw'] / 1000}W")
    print(f"Voltage: {emeter['voltage_mv'] / 1000}V")
    print(f"Current: {emeter['current_ma'] / 1000}A")
    
    # Daily stats
    daily = await device.get_emeter_daily(year=2026, month=2)
    
    # Monthly stats
    monthly = await device.get_emeter_monthly(year=2026)
```

### Smart Bulb Control

For bulbs and dimmers:

```python
# Brightness (0-100)
await device.set_brightness(75)
current = device.brightness

# Color temperature (2500-9000 Kelvin)
await device.set_color_temp(4000)

# HSV color (hue: 0-360, sat: 0-100, val: 0-100)
await device.set_hsv(120, 80, 100)  # Green
hue, sat, val = device.hsv
```

### Device Information

```python
await device.update()

# System info
info = device.sys_info
print(info)

# Hardware/firmware
print(device.hw_info)
print(device.mac)

# Time
time_info = await device.get_time()
```

## CLI Usage

The native `kasa` CLI (installed with python-kasa):

```bash
# Discover devices
kasa discover

# Get device state
kasa --host 192.168.1.100 state

# Turn on/off
kasa --host 192.168.1.100 on
kasa --host 192.168.1.100 off

# Use by alias (requires discovery)
kasa --alias "Living Room" on

# Get system info
kasa --host 192.168.1.100 sysinfo

# Energy usage
kasa --host 192.168.1.100 emeter

# Brightness
kasa --host 192.168.1.100 brightness 75

# JSON output
kasa --host 192.168.1.100 state --json
```

## Device Types

### Smart Plugs
- **Models**: HS100, HS103, HS105, KP115, EP10, EP25
- **Features**: On/Off, some have energy monitoring
- **Typical use**: Lamps, fans, heaters, appliances

### Smart Switches
- **Models**: HS200, HS210, HS220 (dimmer), KS200, KS220, KS230
- **Features**: On/Off, dimmers have brightness
- **Typical use**: Hardwired lights, fans

### Smart Bulbs
- **Models**: KL110 (dimmable), KL120 (tunable white), KL125, KL130 (color)
- **Features**: On/Off, brightness, color temp, color (model-dependent)
- **Typical use**: Lamps, ceiling fixtures

### Power Strips
- **Models**: HS300, KP400
- **Features**: Multiple individually controlled outlets
- **Typical use**: Entertainment centers, office desks

## Network Architecture

### Protocol
- Uses UDP port 9999 for discovery (broadcast)
- TCP port 9999 for device control
- Local network only (no cloud required for control)
- Encrypted proprietary protocol

### Discovery Process
1. Send broadcast UDP packet to 255.255.255.255:9999
2. Devices respond with their info
3. Library parses responses and creates device objects

### Security
- Newer devices (KLAP, AES protocols) require authentication
- Username/password can be provided: `--username user --password pass`
- Credentials can be hashed and stored
- Always use local network security (WPA2/WPA3, firewall)

## Common Patterns

### Batch Operations

```python
async def turn_off_all():
    devices = await Discover.discover()
    tasks = []
    for device in devices.values():
        await device.update()
        if device.is_on:
            tasks.append(device.turn_off())
    await asyncio.gather(*tasks)
```

### Status Monitoring

```python
async def monitor_power(device_ip, interval=5):
    device = await Discover.discover_single(device_ip)
    while True:
        await device.update()
        if device.has_emeter:
            emeter = await device.get_emeter_realtime()
            watts = emeter['power_mw'] / 1000
            print(f"Current draw: {watts:.1f}W")
        await asyncio.sleep(interval)
```

### Smart Scheduling

```python
async def scheduled_control(device_name, state, hour, minute):
    devices = await Discover.discover()
    for device in devices.values():
        await device.update()
        if device.alias == device_name:
            # Wait until scheduled time
            # Then execute
            if state == "on":
                await device.turn_on()
            else:
                await device.turn_off()
            break
```

## Error Handling

Common exceptions to handle:
- `SmartDeviceException` - Device communication error
- `TimeoutError` - Device didn't respond
- `ConnectionRefusedError` - Can't connect to device
- `OSError` - Network issues

```python
try:
    device = await Discover.discover_single(host)
    await device.update()
    await device.turn_on()
except TimeoutError:
    print("Device didn't respond")
except Exception as e:
    print(f"Error: {e}")
```

## Advanced Features

### Firmware Updates
Some devices support OTA updates via the Kasa app. The library can check update availability but doesn't perform updates.

### Scheduling
Devices have built-in scheduling. Access via:
```python
schedule = await device.get_next_schedule_rule()
```

### LED Control
Some plugs have status LEDs that can be controlled:
```python
await device.set_led(False)  # Turn off LED
```

### Time Sync
```python
# Get device time
time_info = await device.get_time()

# Set device time (not commonly needed)
await device.set_time(datetime.now())
```

## Limitations

- Devices must be on same network (no cloud relay)
- Discovery limited to local broadcast domain
- No support for remote access without VPN
- Some features require specific firmware versions
- Authentication varies by device generation

## Resources

- **Library GitHub**: https://github.com/python-kasa/python-kasa
- **Documentation**: https://python-kasa.readthedocs.io/
- **Device List**: https://python-kasa.readthedocs.io/en/latest/discover.html
- **Protocol Info**: https://github.com/softScheck/tplink-smartplug
