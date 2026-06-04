import sqlite3

def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    # Create an inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            typology TEXT,
            price TEXT,
            amenities TEXT
        )
    """)
    
    # Check if table is empty before seeding mock data
    cursor.execute("SELECT COUNT(*) FROM properties")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            # Core Properties
            ("Lower Parel", "4BHK Luxury Penthouse", "₹15 Crore", "Carpet Area: 3200 sq ft, Maintenance: ₹45k/mo, Structural warranty included."),
            ("Bandra West", "3BHK Sea Facing Apartment", "₹22 Crore", "Infinity balcony view, 2 dedicated car parks, Private elevator access."),
            ("Worli", "5BHK Duplex Sky Villa", "₹45 Crore", "Private sky lounge, 24/7 concierge service, Custom marble flooring."),
            
            # Premium Expansion Inventory
            ("Juhu", "5BHK Beachfront Bungalow", "₹85 Crore", "Direct beach access, private plunge pool, standalone security pavilion, 6 covered car parks, Vaastu compliant design."),
            ("Malabar Hill", "4BHK Heritage View Apartment", "₹60 Crore", "Panoramic Arabian sea views, wrap-around sunset deck, ultra-exclusive single apartment per floor layout, biometric access control."),
            ("Cuffe Parade", "3BHK Premium High-Rise Suite", "₹18 Crore", "Carpet Area: 2100 sq ft, unhindered harbor views, fully furnished with Italian design fit-outs, automated centralized climate control systems."),
            ("Prabhadevi", "4BHK Duplex Residence", "₹28 Crore", "Siddhi Vinayak view orientation, double-height living room ceiling, integrated modular kitchen by Hacker, separate staff quarters with dedicated service entry."),
            ("Breach Candy", "4BHK Coastal View Condominium", "₹52 Crore", "Unobstructed ocean vistas, temperature-controlled private wine cellar, Olympic-sized lap pool access, 24/7 private paramedic concierge response link."),
            ("Andheri West", "4BHK Celebration Penthouse", "₹12 Crore", "Located in Lokhandwala micro-market, massive 1500 sq ft open terrace deck, integrated smart home automation by Crestron, private soundproof screening room."),
            ("Powai", "5BHK Hiranandani Penthouse", "₹16 Crore", "Powai Lake view orientation, 14-foot double-height ceilings, imported Italian Botticino marble flooring, exclusive access to resident-only rooftop helipad clubhouse."),
            ("Santacruz West", "3BHK Boutique Garden Apartment", "₹14 Crore", "Low-density quiet neighborhood, private landscaped wrap-around garden terrace, 3 independent basement car parking slots, zero-noise acoustic acoustic window glazing."),
            ("Colaba", "4BHK Heritage Grande Apartment", "₹38 Crore", "Colaba Causeway perimeter location, classic high-ceiling Victorian architecture, fully restored antique teakwood flooring, immediate backdrop views of the Gateway of India.")
        ]
        cursor.executemany("INSERT INTO properties (location, typology, price, amenities) VALUES (?, ?, ?, ?)", mock_data)
        conn.commit()
    
    conn.close()

def query_property(search_text: str) -> str:
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT location, typology, price, amenities FROM properties")
    all_properties = cursor.fetchall()
    conn.close()
    
    for loc, typo, prc, amen in all_properties:
        if loc.lower() in search_text.lower():
            return f"Verified Record Found -> Location: {loc} | Type: {typo} | Price: {prc} | Specs: {amen}"
            
    return "No explicit database entry matches this location. Defaulting to general consultation guidelines."

# Initialize when file is imported
init_db()