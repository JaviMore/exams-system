#!/bin/bash

echo "Stopping Exams System servers..."

# Find and kill processes
pkill -f "uvicorn app.main:app"
pkill -f "vite"

echo "Servers stopped!"
