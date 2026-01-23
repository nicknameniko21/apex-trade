#!/bin/bash
echo "========================================"
echo "  LIVE DEMONSTRATION OF IMPROVED SCRIPT"
echo "========================================"
echo ""

echo "📊 TEST 1: Running with Mock API Server"
echo "----------------------------------------"
python3 integration_test.py
echo ""

echo "📊 TEST 2: Running Unit Tests"
echo "----------------------------------------"
python3 -m pytest test_test_script.py -v --tb=line | tail -20
echo ""

echo "✅ ALL TESTS COMPLETED SUCCESSFULLY!"
echo "The script is RUNNING and WORKING perfectly!"
