#!/usr/bin/env python3
"""
Test script for GitHub Copilot Agent integration
This script has intentional issues that Copilot agents should identify and fix.
"""

import requests
import json
import os

def fetch_data(url):
    """Fetch data from URL - needs error handling"""
    response = requests.get(url)
    data = response.json()
    return data

def process_data(data):
    """Process fetched data - needs optimization"""
    results = []
    for item in data:
        if item['status'] == 'active':
            results.append({
                'id': item['id'],
                'name': item['name'],
                'value': item['value'] * 2  # Why multiply by 2?
            })
    return results

def save_results(results):
    """Save results - needs better error handling"""
    with open('results.json', 'w') as f:
        json.dump(results, f)

def main():
    """Main function - needs restructuring"""
    url = "https://api.example.com/data"
    data = fetch_data(url)
    results = process_data(data)
    save_results(results)
    print("Processing complete!")

if __name__ == "__main__":
    main()

# TODO: Add unit tests
# TODO: Add logging
# TODO: Add configuration management
# TODO: Add proper error handling
# TODO: Optimize performance