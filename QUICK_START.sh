#!/bin/bash

echo "🏥 Hospital KPI Intelligence System - Quick Start"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Not in the correct directory. Please navigate to /mnt/okcomputer/output"
    exit 1
fi

echo "📋 Checking system requirements..."

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Check if dependencies are installed
echo "🔧 Checking dependencies..."
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required dependencies..."
    pip install flask flask-socketio rdflib
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please install them manually:"
        echo "   pip install flask flask-socketio rdflib"
        exit 1
    fi
    echo "✅ Dependencies installed successfully!"
else
    echo "✅ All dependencies are already installed"
fi

echo ""
echo "🚀 Starting Hospital KPI Intelligence System..."
echo ""
echo "The system will be available at: http://localhost:8080"
echo ""
echo "Available interfaces:"
echo "  • /dashboard    - Interactive KPI monitoring"
echo "  • /insights     - AI-powered recommendations"
echo "  • /simulation   - What-if scenario testing"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
python run.py