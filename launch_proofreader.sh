#!/bin/bash

# Doc Proofreader Launcher Script
# This script automatically starts the Doc Proofreader Streamlit app
# Compatible with macOS and Linux

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}📝 Doc Proofreader Launcher${NC}"
echo "================================"

# Function to find and activate virtual environment
activate_venv() {
    echo -e "${YELLOW}🔍 Looking for virtual environment...${NC}"

    # Common virtual environment names
    VENV_NAMES=(".doc-proofreader_venv" "venv" ".venv" "env" ".env")

    for venv_name in "${VENV_NAMES[@]}"; do
        if [ -d "$venv_name" ]; then
            echo -e "${GREEN}✅ Found virtual environment: $venv_name${NC}"

            # Activate the virtual environment
            if [ -f "$venv_name/bin/activate" ]; then
                source "$venv_name/bin/activate"
                echo -e "${GREEN}✅ Virtual environment activated${NC}"
                return 0
            fi
        fi
    done

    echo -e "${YELLOW}⚠️  No virtual environment found${NC}"
    echo -e "${YELLOW}   Using system Python installation${NC}"
    return 1
}

# Function to check if streamlit is installed
check_streamlit() {
    if ! command -v streamlit &> /dev/null; then
        echo -e "${RED}❌ Streamlit is not installed${NC}"
        echo -e "${YELLOW}   Installing Streamlit...${NC}"
        pip install streamlit
    fi
}

# Function to check if port is already in use
check_port() {
    if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${YELLOW}⚠️  Port 8501 is already in use${NC}"
        echo -e "${YELLOW}   The app might already be running${NC}"
        read -p "   Do you want to kill the existing process? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            lsof -ti:8501 | xargs kill -9 2>/dev/null || true
            sleep 1
            echo -e "${GREEN}✅ Killed existing process${NC}"
        else
            echo -e "${BLUE}   Opening browser to existing instance...${NC}"
            open "http://localhost:8501"
            exit 0
        fi
    fi
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down Doc Proofreader...${NC}"
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
    fi
    # Kill any remaining streamlit processes on port 8501
    lsof -ti:8501 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✅ Shutdown complete${NC}"
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Main execution
activate_venv
check_streamlit
check_port

echo -e "${BLUE}🚀 Starting Streamlit app...${NC}"
echo ""

# Start streamlit in the background
streamlit run streamlit_app.py --server.headless true &
STREAMLIT_PID=$!

# Wait for the server to start
echo -e "${YELLOW}⏳ Waiting for server to start...${NC}"
sleep 3

# Check if the process is still running
if ps -p $STREAMLIT_PID > /dev/null; then
    echo -e "${GREEN}✅ Server started successfully!${NC}"
    echo ""
    echo -e "${GREEN}🌐 Opening browser at http://localhost:8501${NC}"
    echo ""

    # Open browser (works on macOS)
    if command -v open &> /dev/null; then
        open "http://localhost:8501"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:8501"
    else
        echo -e "${YELLOW}   Please open http://localhost:8501 in your browser${NC}"
    fi

    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✨ Doc Proofreader is now running!${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  📍 Local URL:   ${GREEN}http://localhost:8501${NC}"
    echo -e "  🛑 To stop:     ${YELLOW}Press Ctrl+C${NC}"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Wait for user to press Ctrl+C
    wait $STREAMLIT_PID
else
    echo -e "${RED}❌ Failed to start server${NC}"
    echo -e "${YELLOW}   Check the error messages above${NC}"
    exit 1
fi
