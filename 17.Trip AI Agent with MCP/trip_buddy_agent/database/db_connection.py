import sqlite3
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            state TEXT NOT NULL,
            category TEXT,
            cost_per_person_per_night REAL NOT NULL,
            recommended_nights INTEGER NOT NULL,
            best_months TEXT NOT NULL,
            summary TEXT NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS travel_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """)
        conn.commit()

def seed_db():
    destinations = [
        ("Goa", "Goa", "Beach", 3200, 3, "November, December, January, February, March",
         "Beaches, water activities, cafes and nightlife. Costs rise during peak season."),
        ("Manali", "Himachal Pradesh", "Mountains", 2800, 4, "March, April, May, June, September, October",
         "Mountain views, cafes, Solang Valley and adventure activities. Check road and weather conditions."),
        ("Hampi", "Karnataka", "Heritage", 1800, 2, "October, November, December, January, February",
         "UNESCO-listed heritage landscape, temples, ruins and boulder-strewn scenery."),
        ("Jaipur", "Rajasthan", "Heritage", 2400, 2, "October, November, December, January, February, March",
         "Forts, palaces, markets and Rajasthani food. Summers can be very hot."),
        ("Kerala", "Kerala", "Nature", 3500, 4, "September, October, November, December, January, February, March",
         "Backwaters, hill stations, beaches and green landscapes. Monsoon conditions vary by region."),
        ("Pondicherry", "Puducherry", "Coastal", 2600, 2, "October, November, December, January, February, March",
         "French Quarter, cafes, promenade and nearby beaches."),
        ("Udaipur", "Rajasthan", "Heritage", 3000, 2, "October, November, December, January, February, March",
         "Lakes, palaces, old-city walks and rooftop dining."),
    ]
    knowledge = [
        ("Goa season", "Goa is generally most popular from November to February. April and May are hot. Monsoon months roughly June to September bring heavy rain and rougher sea conditions; water activities may be restricted."),
        ("Manali in July", "July is monsoon season in the wider Himachal region. Expect rain, possible road disruption and landslide risk. Check official local advisories and road conditions before travelling. It may not be the best choice for a fixed-schedule road trip."),
        ("Hampi season", "Hampi is usually more comfortable from October to February. Summers can be very hot. Carry water, sun protection and comfortable walking shoes."),
        ("Jaipur season", "October to March is generally more comfortable for Jaipur sightseeing. April to June can be extremely hot; plan outdoor sightseeing early in the morning."),
        ("Kerala monsoon", "Kerala's monsoon season varies by coast and district, with substantial rainfall often occurring from June through September. Some travellers enjoy the green landscape, but outdoor plans can be affected."),
        ("Trip budgeting", "A practical trip budget should include stay, food, local transport, activities, intercity travel, taxes and a contingency buffer. The sample destination rates in this demo are estimates, not live quotes."),
        ("Group travel", "For groups, confirm room occupancy, extra-bed charges, transport capacity and cancellation terms. Per-person estimates can change with group size and room sharing."),
    ]
    with get_connection() as conn:
        for row in destinations:
            conn.execute("""
            INSERT OR IGNORE INTO destinations
            (name,state,category,cost_per_person_per_night,recommended_nights,best_months,summary)
            VALUES (?,?,?,?,?,?,?)
            """, row)
        count = conn.execute("SELECT COUNT(*) FROM travel_knowledge").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO travel_knowledge(topic,content) VALUES (?,?)",
                knowledge
            )
        conn.commit()
