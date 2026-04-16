"""
Tests for scraper module.
"""

import pytest
from scraper import fetch_trending, fetch_trending_with_retry


def test_fetch_trending_returns_list():
    trends = fetch_trending()
    # Just check it returns a list (may be empty if API fails)
    assert isinstance(trends, list)


def test_fetch_trending_with_retry():
    trends = fetch_trending_with_retry()
    assert isinstance(trends, list)
    # Each trend should have required keys
    for t in trends:
        assert "name" in t
        assert "url" in t
