# Home Assistant Component for a tk_tts installation.

[![hacs_badge](https://img.shields.io/badge/HACS-default-orange.svg)](https://github.com/custom-components/hacs)

This is a component for Home Assistant which integrates picoTTS from a remote server.
Its recommended to run the server via my [Home Assistant Supervisor Addon](https://github.com/Poeschl/Hassio-Addons/tree/master/picoTTS).

# Installation

## HACS

Install it in the `Integrations` tab on the [Home Asssistant Community Store](https://github.com/custom-components/hacs).

## Manual way
To use it, copy the `tk_tts` folder inside your `config/custom_components` folder on your home assistant installation first.


# Configuration

Add following config to your yaml if you are using the Supervisor Addon

```yaml
tts:
  - platform: tk_tts

```
The integration will connect to picoTTS after an Home Assistant restart.

## Other host

For setting your own host and port:

```yaml
tts:
  - platform: tk_tts
    host: <host>
    port: <port>

```

## Language

The languge can be set to any language supported by your Android device.

```yaml
tts:
  - platform: tk_tts
    language: "de"

```
