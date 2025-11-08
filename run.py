#!/usr/bin/env python3
"""
Hospital KPI Intelligence WebApp Runner
Simple script to run the application for testing
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("🏥 Hospital KPI Intelligence WebApp")
    print("=" * 50)
    print("Starting application...")
    
    # Check if all required files exist
    required_files = [
        'ontology/hospital_kpi.owl',
        'ontology/kpi_data.ttl',
        'templates/index.html',
        'templates/insights.html',
        'templates/simulation.html',
        'static/js/dashboard.js',
        'static/js/simulation.js'
    ]
    
    print("\nChecking required files:")
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some required files are missing!")
        sys.exit(1)
    
    print("\n✅ All required files found!")
    print("\nStarting Flask development server...")
    print("The application will be available at: http://localhost:8080")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)