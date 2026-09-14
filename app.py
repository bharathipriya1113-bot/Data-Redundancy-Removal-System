import sqlite3

existing_data = [
    {
        "name": "Bharathi",
        "email": "bharathi@gmail.com",
        "phone": "9876543210"
    },
    {
        "name": "Priya",
        "email": "priya@gmail.com",
        "phone": "9876543211"
    }
]

# Connect to database
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
)
""")

connection.commit()

print(existing_data)

# Get new data
new_data = {
    "name": input("Enter name: ").strip(),
    "email": input("Enter email: ").strip(),
    "phone": input("Enter phone: ").strip()
}

# Validate data
if not new_data["name"] or not new_data["email"] or not new_data["phone"]:
    print("\n❌ Invalid data. All fields are required.")
    connection.close()
    exit()

print("\nNew data received:")
print(new_data)

# Get all existing records
cursor.execute("SELECT name, email, phone FROM users")
all_records = cursor.fetchall()

is_redundant = False
is_false_positive = False

# Check new data against existing data
for record in all_records:

    same_name = record[0].lower() == new_data["name"].lower()
    same_email = record[1].lower() == new_data["email"].lower()
    same_phone = record[2] == new_data["phone"]

    # All details are same
    if same_name and same_email and same_phone:
        is_redundant = True
        break

    # Some details are same, but not all
    elif same_name or same_email or same_phone:
        is_false_positive = True

# Classification
if is_redundant:

    print("\n❌ Redundant data detected.")

elif is_false_positive:

    print("\n⚠️ False positive detected - data is different.")

    cursor.execute(
        "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
        (new_data["name"], new_data["email"], new_data["phone"])
    )

    connection.commit()

    print("✅ Verified unique data added to database.")

else:

    print("\n✅ Unique data.")

    cursor.execute(
        "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
        (new_data["name"], new_data["email"], new_data["phone"])
    )

    connection.commit()

    print("✅ Data added to database.")

# Display database
cursor.execute("SELECT * FROM users")
saved_data = cursor.fetchall()

print("\nData currently stored in database:")
print(saved_data)

connection.close()