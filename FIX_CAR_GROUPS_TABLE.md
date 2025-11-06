# Fix: Missing car_groups Table

## Problem
The application was failing with:
```
ERROR:root:PostgreSQL execute error: relation "car_groups" does not exist
```

## What Was Fixed

### 1. Created Setup Endpoint
Added `/setup-car-groups-table` endpoint to create the missing table in PostgreSQL.

### 2. Fixed SQL Syntax
Updated the `map_category_to_group()` function to work with both PostgreSQL (`%s`) and SQLite (`?`) placeholders.

### 3. Table Schema
```sql
CREATE TABLE car_groups (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT,
    model TEXT,
    brand TEXT,
    category TEXT,
    doors INTEGER,
    seats INTEGER,
    transmission TEXT,
    luggage INTEGER,
    photo_url TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Next Steps (After Deployment)

### Step 1: Create the Table
Once the new deployment is live, visit:
```
https://your-app.onrender.com/setup-car-groups-table
```

You should see:
```json
{"ok": true, "message": "Tabela car_groups criada com sucesso!"}
```

### Step 2: Populate the Table
The table is now created but empty. You have two options:

#### Option A: Use the Vehicle Editor UI
1. Go to: `https://your-app.onrender.com/admin/car-groups`
2. Add car groups manually through the interface
3. For each car, specify:
   - Code (e.g., "B1", "D", "F")
   - Name (e.g., "Fiat 500")
   - Model (e.g., "500")
   - Brand (e.g., "Fiat")
   - Category (e.g., "Mini", "Economy", "Compact")
   - Other details (doors, seats, transmission, luggage)

#### Option B: Import from Export File
If you have a previous export with car_groups data:
1. Go to: `https://your-app.onrender.com/admin/import-export`
2. Upload your export JSON file
3. The car_groups data will be imported automatically

### Step 3: Verify
After populating the table, the scraping errors should disappear. Check the logs for:
- No more "relation car_groups does not exist" errors
- Cars should now be properly mapped to groups
- Example: `[DEBUG] row tem 'group'? True, valor=D`

## Files Changed
- `main.py`: Added setup endpoint + fixed SQL compatibility

## Commit
```
Add car_groups table setup and fix PostgreSQL compatibility (acb870a)
```
