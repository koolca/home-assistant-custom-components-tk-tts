"""Support for the TK-Solution TTS speech service."""
import logging

import asyncio
import aiohttp
import re
import async_timeout
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from urllib.parse import quote


_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["en", "de", "es", "fr", "it", "hu"]

DEFAULT_LANG = "hu"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up TK-Solution speech component."""
    return PicoProvider(hass, config[CONF_LANG], config[CONF_HOST], config[CONF_PORT])


class PicoProvider(Provider):
    """The TK-Solution TTS API provider."""

    def __init__(self, hass, lang, host, port, api):
        """Initialize TK-Solution TTS provider."""
        self._hass = hass
        self._lang = lang
        self._host = host
        self._port = port
        self._api = api
        self.name = "TK-Solution TTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    async def async_get_tts_audio(self, message, language, options=None):
        """Load TTS using a remote pico2wave server."""
        websession = async_get_clientsession(self._hass)

        try:
            with async_timeout.timeout(5):
                url = "http://{}:{}/{}".format(self._host, self._port, self._api)
                encoded_message = quote(message)
                url_param = {
                    "text": encoded_message,
                    "lang": language,
                    "vol": "10",
                }

                request = await websession.get(url, params=url_param)

                if request.status != 200:
                    _LOGGER.error(
                        "Error %d on load url %s", request.status, request.url
                    )
                    return (None, None)
                data = await request.read()

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for PicoTTS API")
            return (None, None)

        if data:
            return ("mp3", data)
        return (None, None)
