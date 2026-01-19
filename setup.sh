#!/bin/bash

echo "========================================"
echo "Exams System - Complete Setup"
echo "========================================"
echo ""

# Check if running from project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Backend setup
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "✅ Backend setup complete!"

cd ..

# Frontend setup
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

echo "✅ Frontend setup complete!"

cd ..

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Create an admin user:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python create_admin.py admin@example.com admin123 'Administrator'"
echo "   cd .."
echo ""
echo "2. Import existing exams (optional):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python import_exams.py ../exams"
echo "   cd .."
echo ""
echo "3. Start the application:"
echo "   ./start.sh"
echo ""
echo "Or start manually:"
echo "   Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Terminal 2: cd frontend && npm run dev"
echo ""
