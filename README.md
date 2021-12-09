# TelenorDrift for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-telenordrift?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

HomeAssistant-integration for TelenorDrift

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "TelenorDrift"-integration.
4. Restart Home Assistant.
5. Configure the `TelenorDrift` integration.

### MANUAL INSTALLATION

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/ha-telenordrift/releases/latest).
2. Unpack the release and copy the `custom_components/ha-telenordrift` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Configure the `TelenorDrift`-integration.

## Configuration
- Search your address at https://www.telenor.no/driftsmeldinger/
- You are redirected to a page with the url: https://www.telenor.no/driftsmeldinger/sok/ **"area-id"**
- Use this area-id when configuring the integration in HA

## Todo
- [ ] Easier way to add your area-code
- [ ] Rewrite API-logic
- [ ] Configurable polling-interval

## Features
### Sensors
- TV
- Internet
- Mobile

The sensors represent the number of current issues for your area. They also have an "issues"-attribute which contains the descriptions of the issues (if it exists in the API).

