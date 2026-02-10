# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### Kasa Smart Devices
> Kasa smart switch/plug/bulb control via python-kasa
> Use: `python3 skills/kasa-smart-switch/scripts/kasa_control.py <action>`

**Configured Devices:** (None yet - will auto-populate after first discovery)
```
# Run discovery to find devices:
# python3 skills/kasa-smart-switch/scripts/kasa_control.py list

# Example device list (update after discovery):
# - Living Room Light → 192.168.1.100 (Smart Bulb)
# - Kitchen Outlet → 192.168.1.101 (Smart Plug with Energy Monitoring)
# - Bedroom Lamp → 192.168.1.102 (Dimmable Bulb)
```

---

Add whatever helps you do your job. This is your cheat sheet.
