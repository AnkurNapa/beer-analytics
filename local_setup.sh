#!/usr/bin/env bash
set -euo pipefail

echo "🍺 Beer Analytics — Local Setup"
echo "======================================="
echo ""

# Check Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Install from https://brew.sh"
    exit 1
fi

# Step 1: PostgreSQL
echo "1️⃣  Setting up PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "   Installing PostgreSQL..."
    brew install postgresql
else
    echo "   ✓ PostgreSQL already installed"
fi

echo "   Starting PostgreSQL service..."
brew services start postgresql || true

# Wait a moment for service to start
sleep 2

# Create database if it doesn't exist
echo "   Creating database 'beer_analytics'..."
createdb beer_analytics 2>/dev/null || echo "   (Database already exists)"

echo "   ✓ PostgreSQL ready"
echo ""

# Step 2: Python venv
echo "2️⃣  Setting up Python virtual environment..."
if [ -d "venv" ]; then
    echo "   ✓ venv already exists"
else
    python3 -m venv venv
    echo "   ✓ Created venv"
fi

source venv/bin/activate
echo "   ✓ venv activated"
echo ""

# Step 3: Install dependencies
echo "3️⃣  Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "   ✓ Dependencies installed"
echo ""

# Step 4: .env file
echo "4️⃣  Configuring environment..."
if [ -f ".env" ]; then
    echo "   ✓ .env already exists (skipping)"
else
    cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=local-dev-key-change-in-production
DATABASE_URL=postgres://postgres@localhost/beer_analytics
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=Asia/Kolkata
EOF
    echo "   ✓ Created .env"
fi
echo ""

# Step 5: Migrations
echo "5️⃣  Running migrations..."
python manage.py migrate --no-input
python manage.py createcachetable
echo "   ✓ Migrations complete"
echo ""

# Step 6: Initial data
echo "6️⃣  Loading initial data (97 styles, 100+ hops, 60+ fermentables, 200+ yeasts)..."
python manage.py load_initial_data
echo "   ✓ Initial data loaded"
echo ""

echo "======================================="
echo "✅ Setup complete!"
echo ""
echo "To start the app, run:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000/"
echo ""
