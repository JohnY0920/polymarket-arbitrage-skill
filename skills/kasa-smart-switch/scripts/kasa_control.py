#!/usr/bin/env python3
"""
Kasa Smart Device Control Script
Provides simple CLI interface for controlling TP-Link Kasa smart devices
"""

import asyncio
import sys
import json
import argparse
from typing import Optional, Dict, Any
from kasa import Discover, SmartDevice


async def discover_devices(timeout: int = 10) -> Dict[str, SmartDevice]:
    """Discover all Kasa devices on the network"""
    print(f"Discovering devices (timeout: {timeout}s)...", file=sys.stderr)
    devices = await Discover.discover(timeout=timeout)
    return devices


async def get_device_by_name(alias: str, timeout: int = 5) -> Optional[SmartDevice]:
    """Find a device by its alias/name"""
    devices = await discover_devices(timeout=timeout)
    
    for device in devices.values():
        await device.update()
        if device.alias.lower() == alias.lower():
            return device
    
    return None


async def get_device_by_host(host: str) -> Optional[SmartDevice]:
    """Connect to a device by IP address"""
    try:
        device = await Discover.discover_single(host)
        await device.update()
        return device
    except Exception as e:
        print(f"Error connecting to {host}: {e}", file=sys.stderr)
        return None


async def control_device(device: SmartDevice, action: str) -> Dict[str, Any]:
    """Control a device (on/off/toggle)"""
    result = {
        "device": device.alias,
        "host": device.host,
        "action": action,
        "success": False
    }
    
    try:
        if action == "on":
            await device.turn_on()
            result["success"] = True
            result["new_state"] = "on"
        elif action == "off":
            await device.turn_off()
            result["success"] = True
            result["new_state"] = "off"
        elif action == "toggle":
            if device.is_on:
                await device.turn_off()
                result["new_state"] = "off"
            else:
                await device.turn_on()
                result["new_state"] = "on"
            result["success"] = True
        else:
            result["error"] = f"Unknown action: {action}"
        
        await device.update()
        result["is_on"] = device.is_on
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


async def get_device_status(device: SmartDevice) -> Dict[str, Any]:
    """Get detailed device status"""
    await device.update()
    
    status = {
        "alias": device.alias,
        "host": device.host,
        "model": device.model,
        "is_on": device.is_on,
        "device_type": str(device.device_type),
        "has_emeter": device.has_emeter
    }
    
    # Add emeter data if supported
    if device.has_emeter:
        try:
            emeter = await device.get_emeter_realtime()
            status["emeter"] = {
                "power": emeter.get("power_mw", 0) / 1000,  # Convert to watts
                "voltage": emeter.get("voltage_mv", 0) / 1000,  # Convert to volts
                "current": emeter.get("current_ma", 0) / 1000,  # Convert to amps
                "total": emeter.get("total_wh", 0) / 1000  # Convert to kWh
            }
        except Exception as e:
            status["emeter_error"] = str(e)
    
    # Add brightness if supported (smart bulbs/dimmers)
    if hasattr(device, 'brightness'):
        status["brightness"] = device.brightness
    
    # Add color info if supported
    if hasattr(device, 'is_color') and device.is_color:
        status["color"] = {
            "hue": device.hsv[0],
            "saturation": device.hsv[1],
            "value": device.hsv[2]
        }
    
    # Add color temperature if supported
    if hasattr(device, 'color_temp'):
        status["color_temp"] = device.color_temp
    
    return status


async def list_devices(timeout: int = 10, json_output: bool = False) -> None:
    """List all discovered devices"""
    devices = await discover_devices(timeout=timeout)
    
    if not devices:
        print("No devices found.", file=sys.stderr)
        return
    
    device_list = []
    for device in devices.values():
        await device.update()
        device_list.append({
            "alias": device.alias,
            "host": device.host,
            "model": device.model,
            "is_on": device.is_on,
            "device_type": str(device.device_type)
        })
    
    if json_output:
        print(json.dumps(device_list, indent=2))
    else:
        print(f"\nFound {len(device_list)} device(s):\n")
        for dev in device_list:
            state = "ON" if dev["is_on"] else "OFF"
            print(f"  • {dev['alias']}")
            print(f"    Host: {dev['host']}")
            print(f"    Model: {dev['model']}")
            print(f"    Type: {dev['device_type']}")
            print(f"    State: {state}\n")


async def main():
    parser = argparse.ArgumentParser(
        description="Control TP-Link Kasa smart devices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all devices
  %(prog)s list
  
  # Turn on a device by name
  %(prog)s --device "Living Room Light" on
  
  # Turn off a device by IP
  %(prog)s --host 192.168.1.100 off
  
  # Toggle a device
  %(prog)s --device "Kitchen Outlet" toggle
  
  # Get device status
  %(prog)s --device "Bedroom Lamp" status
  
  # Get energy usage
  %(prog)s --device "Kitchen Outlet" status --json
        """
    )
    
    parser.add_argument('action', 
                       choices=['list', 'on', 'off', 'toggle', 'status'],
                       help='Action to perform')
    parser.add_argument('--device', '-d',
                       help='Device alias/name')
    parser.add_argument('--host',
                       help='Device IP address')
    parser.add_argument('--timeout', '-t',
                       type=int,
                       default=5,
                       help='Discovery timeout in seconds (default: 5)')
    parser.add_argument('--json',
                       action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    # List devices
    if args.action == 'list':
        await list_devices(timeout=args.timeout, json_output=args.json)
        return
    
    # Other actions require a device
    if not args.device and not args.host:
        print("Error: --device or --host is required for this action", file=sys.stderr)
        sys.exit(1)
    
    # Get the device
    device = None
    if args.host:
        device = await get_device_by_host(args.host)
    else:
        device = await get_device_by_name(args.device, timeout=args.timeout)
    
    if not device:
        if args.host:
            print(f"Error: Could not connect to device at {args.host}", file=sys.stderr)
        else:
            print(f"Error: Device '{args.device}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Perform action
    if args.action == 'status':
        status = await get_device_status(device)
        print(json.dumps(status, indent=2))
    else:
        result = await control_device(device, args.action)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                state = result["new_state"].upper()
                print(f"✓ {result['device']} turned {state}")
            else:
                print(f"✗ Failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
