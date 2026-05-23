import pytest
from weather import geocode, fetch_forecast

def test_geocode_valid():
    result = geocode("London")
    assert result is not None
    assert "lat" in result[0]

def test_geocode_invalid():
    result = geocode("xkcd123xyz")
    assert result is None

def test_fetch_forecast():
    forecast = fetch_forecast(51.5, -0.1, 3)
    assert "time" in forecast
    assert len(forecast["time"]) == 3