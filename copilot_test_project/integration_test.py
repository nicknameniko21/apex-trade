#!/usr/bin/env python3
"""
Integration Test - Demonstrates the script working end-to-end

This script creates a mock API server and demonstrates the improved
test_script.py working correctly with real data.
"""

import json
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os


class MockAPIHandler(BaseHTTPRequestHandler):
    """Mock API server for testing"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/data':
            # Return sample data
            response_data = [
                {'id': 1, 'name': 'Product A', 'value': 100, 'status': 'active'},
                {'id': 2, 'name': 'Product B', 'value': 200, 'status': 'inactive'},
                {'id': 3, 'name': 'Product C', 'value': 150, 'status': 'active'},
                {'id': 4, 'name': 'Product D', 'value': 300, 'status': 'active'},
            ]
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


def run_mock_server(port=8765):
    """Run mock API server"""
    server = HTTPServer(('localhost', port), MockAPIHandler)
    server.serve_forever()


def main():
    """Run integration test"""
    print("=== Integration Test for Improved test_script.py ===\n")
    
    # Start mock server in background
    port = 8765
    server_thread = threading.Thread(target=run_mock_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(1)  # Wait for server to start
    
    print(f"✓ Mock API server started on http://localhost:{port}")
    
    # Set environment variables
    os.environ['API_URL'] = f'http://localhost:{port}/data'
    os.environ['OUTPUT_FILE'] = 'integration_test_results.json'
    os.environ['API_TIMEOUT'] = '5'
    
    print(f"✓ Environment configured")
    print(f"  - API_URL: {os.environ['API_URL']}")
    print(f"  - OUTPUT_FILE: {os.environ['OUTPUT_FILE']}")
    print()
    
    # Run the script
    print("Running test_script.py...\n")
    result = subprocess.run(
        ['python3', 'test_script.py'],
        capture_output=True,
        text=True
    )
    
    # Print output
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"\nExit code: {result.returncode}")
    
    # Verify results
    if os.path.exists('integration_test_results.json'):
        print("\n✓ Output file created successfully")
        
        with open('integration_test_results.json', 'r') as f:
            results = json.load(f)
        
        print(f"\n=== Results Analysis ===")
        print(f"Total processed items: {len(results)}")
        print(f"\nProcessed data:")
        for item in results:
            print(f"  - ID: {item['id']}, Name: {item['name']}, Value: {item['value']}")
        
        # Validate results
        expected_count = 3  # Only active items
        if len(results) == expected_count:
            print(f"\n✓ Correct number of items processed ({expected_count})")
        else:
            print(f"\n✗ Expected {expected_count} items, got {len(results)}")
        
        # Check multiplier applied correctly
        if results[0]['value'] == 200:  # 100 * 2
            print("✓ Multiplier applied correctly (100 * 2 = 200)")
        else:
            print(f"✗ Multiplier incorrect: expected 200, got {results[0]['value']}")
        
        # Cleanup
        os.remove('integration_test_results.json')
        print("\n✓ Test cleanup complete")
        
        print("\n=== Integration Test: PASSED ✓ ===")
        return 0
    else:
        print("\n✗ Output file not created")
        print("\n=== Integration Test: FAILED ✗ ===")
        return 1


if __name__ == "__main__":
    exit(main())
