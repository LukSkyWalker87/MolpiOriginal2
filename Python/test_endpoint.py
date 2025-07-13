#!/usr/bin/env python
"""Test endpoint directly"""

import requests
import json

def test_endpoint():
    try:
        response = requests.get('http://localhost:5000/productos')
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text}")
        print(f"JSON: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoint()
