import csv
from datetime import datetime

# ============================================================
# EDIT THESE VARIABLES TO CHANGE YOUR FILTER CRITERIA
# Set any value to None to skip that filter
# ============================================================

# Price range (in dollars)
PRICE_MIN = None        # e.g., 300000
PRICE_MAX = None    # e.g., 600000

# Listed date range (YYYY-MM-DD format)
LISTED_DATE_MIN = "2023-01-01"   # e.g., "2025-01-01"
LISTED_DATE_MAX = None            # e.g., "2025-12-31"

# Bedrooms — set both to same value for exact match, or use range
BEDROOMS_MIN = None      # e.g., 3
BEDROOMS_MAX = None     # e.g., 5

# Property type — list one or more types (case-sensitive), or None to include all
# Common values: "Single Family", "Land", "Condo", "Townhouse", "Multi Family"
PROPERTY_TYPE = ["Single Family", "Condo", "Apartment", "Townhouse"]

# Bathrooms — set both to same value for exact match, or use range
BATHROOMS_MIN = None    # e.g., 2
BATHROOMS_MAX = None   # e.g., 4

# Square footage range
SQ_FT_MIN = None        # e.g., 1000
SQ_FT_MAX = None        # e.g., 3000

# Lot size range (in square feet)
LOT_SIZE_MIN = None     # e.g., 5000
LOT_SIZE_MAX = None    # e.g., 20000

# Year built range
YEAR_BUILT_MIN = None   # e.g., 1990
YEAR_BUILT_MAX = None   # e.g., 2020

# City — must match exactly (case-sensitive)
# Set to None to include all cities
CITY = "Hilliard"

# Name of the CSV file to read (must be in same directory as this script) - THIS IS ONLY THING YOU NEED TO CHANGE TO MOVE FROM RENTAL TO SALES 

CSV_FILE = "rental_listings.csv"

# ============================================================
# SCRIPT — no need to edit below this line
# ============================================================
def parse_date(date_str):
    """Parse ISO date string like '2025-01-01T00:00:00.000Z' or 'YYYY-MM-DD'."""
    if not date_str or date_str in ("NA", "list()"):
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def parse_num(value):
    """Parse a numeric field, returning None for NA or missing."""
    if not value or value == "NA":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def meets_criteria(row):
    price = parse_num(row.get("price"))
    listed_date = parse_date(row.get("listedDate"))
    bedrooms = parse_num(row.get("bedrooms"))
    bathrooms = parse_num(row.get("bathrooms"))
    sq_ft = parse_num(row.get("squareFootage"))
    lot_size = parse_num(row.get("lotSize"))
    year_built = parse_num(row.get("yearBuilt"))
    property_type = row.get("propertyType", "")
    city = row.get("city", "")

    if PRICE_MIN is not None and (price is None or price < PRICE_MIN):
        return False
    if PRICE_MAX is not None and (price is None or price > PRICE_MAX):
        return False

    filter_date_min = parse_date(LISTED_DATE_MIN)
    filter_date_max = parse_date(LISTED_DATE_MAX)
    if filter_date_min is not None and (listed_date is None or listed_date < filter_date_min):
        return False
    if filter_date_max is not None and (listed_date is None or listed_date > filter_date_max):
        return False

    if BEDROOMS_MIN is not None and (bedrooms is None or bedrooms < BEDROOMS_MIN):
        return False
    if BEDROOMS_MAX is not None and (bedrooms is None or bedrooms > BEDROOMS_MAX):
        return False

    if BATHROOMS_MIN is not None and (bathrooms is None or bathrooms < BATHROOMS_MIN):
        return False
    if BATHROOMS_MAX is not None and (bathrooms is None or bathrooms > BATHROOMS_MAX):
        return False

    if SQ_FT_MIN is not None and (sq_ft is None or sq_ft < SQ_FT_MIN):
        return False
    if SQ_FT_MAX is not None and (sq_ft is None or sq_ft > SQ_FT_MAX):
        return False

    if LOT_SIZE_MIN is not None and (lot_size is None or lot_size < LOT_SIZE_MIN):
        return False
    if LOT_SIZE_MAX is not None and (lot_size is None or lot_size > LOT_SIZE_MAX):
        return False

    if YEAR_BUILT_MIN is not None and (year_built is None or year_built < YEAR_BUILT_MIN):
        return False
    if YEAR_BUILT_MAX is not None and (year_built is None or year_built > YEAR_BUILT_MAX):
        return False

    if PROPERTY_TYPE is not None and property_type not in PROPERTY_TYPE:
        return False

    if CITY is not None and city != CITY:
        return False

    return True


def main():
    total = 0
    matched = 0

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if meets_criteria(row):
                matched += 1

    if total == 0:
        print("No records found in file.")
        return

    share = matched / total * 100

    print(f"Total listings:   {total:,}")
    print(f"Matching listings: {matched:,}")
    print(f"Share:            {share:.1f}%")

    print("\nFilters applied:")
    print(f"  Price:         {f'${PRICE_MIN:,}' if PRICE_MIN is not None else 'any'} – {f'${PRICE_MAX:,}' if PRICE_MAX is not None else 'any'}")
    print(f"  Listed date:   {LISTED_DATE_MIN or 'any'} – {LISTED_DATE_MAX or 'any'}")
    print(f"  Bedrooms:      {BEDROOMS_MIN if BEDROOMS_MIN is not None else 'any'} – {BEDROOMS_MAX if BEDROOMS_MAX is not None else 'any'}")
    print(f"  Bathrooms:     {BATHROOMS_MIN if BATHROOMS_MIN is not None else 'any'} – {BATHROOMS_MAX if BATHROOMS_MAX is not None else 'any'}")
    print(f"  Sq footage:    {f'{SQ_FT_MIN:,}' if SQ_FT_MIN is not None else 'any'} – {f'{SQ_FT_MAX:,}' if SQ_FT_MAX is not None else 'any'}")
    print(f"  Lot size:      {f'{LOT_SIZE_MIN:,}' if LOT_SIZE_MIN is not None else 'any'} – {f'{LOT_SIZE_MAX:,}' if LOT_SIZE_MAX is not None else 'any'}")
    print(f"  Year built:    {YEAR_BUILT_MIN if YEAR_BUILT_MIN is not None else 'any'} – {YEAR_BUILT_MAX if YEAR_BUILT_MAX is not None else 'any'}")
    print(f"  Property type: {', '.join(PROPERTY_TYPE) if PROPERTY_TYPE else 'any'}")
    print(f"  City:          {CITY or 'any'}")


if __name__ == "__main__":
    main()
