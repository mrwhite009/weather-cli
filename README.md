# weather-cli

Get weather forecasts from your terminal. Powered by the free [Open-Meteo API](https://open-meteo.com/).

## Features

- Rich terminal output with weather emoji
- Precipitation and temperature
- Configurable forecast range (1–7 days)
- Simple output mode for scripts
- Handles ambiguous city names

## Install

```bash
pip install weather-cli
```

## Usage

```bash
weather London
weather Tokyo -d 5
weather Paris --simple
```