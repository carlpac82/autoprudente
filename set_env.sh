#!/bin/bash
# Force export DATABASE_URL from Render environment
# This fixes the issue where Render stores it as Key/Value instead of exporting it

# Extract DATABASE_URL from environment
if [ -z "$DATABASE_URL" ]; then
    # Try to extract from printenv output
    DB_URL=$(printenv | grep "^Value=" | grep "postgresql://" | cut -d'=' -f2-)
    if [ ! -z "$DB_URL" ]; then
        export DATABASE_URL="$DB_URL"
        echo "✅ DATABASE_URL exported: ${DATABASE_URL:0:30}..."
    else
        echo "⚠️  DATABASE_URL not found in environment"
    fi
else
    echo "✅ DATABASE_URL already set: ${DATABASE_URL:0:30}..."
fi

# Execute the main application
exec "$@"
