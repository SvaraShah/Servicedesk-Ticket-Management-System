import sqlite3
from datetime import datetime

class ServiceDesk:
    def __init__(self):
        self.conn = sqlite3.connect('service_desk.db')
        self.create_table()

    def create_table(self):
        # Professional Table Schema with Timestamps
        query = '''CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT DEFAULT 'OPEN',
                    created_at TEXT)'''
        self.conn.execute(query)
        self.conn.commit()

    def raise_ticket(self, desc, priority):
        # Mimics SAP "Create Ticket" functionality
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO tickets (description, priority, created_at) VALUES (?, ?, ?)"
        self.conn.execute(query, (desc, priority, timestamp))
        self.conn.commit()
        print(f"Ticket logged successfully at {timestamp}")

    def display_active_tickets(self):
        # Display logic with priority-based formatting
        cursor = self.conn.execute("SELECT * FROM tickets WHERE status != 'CLOSED'")
        tickets = cursor.fetchall()
        
        print("\n--- ACTIVE SERVICE TICKETS ---")
        print(f"{'ID':<5} {'Description':<25} {'Priority':<10} {'Status':<10}")
        print("-" * 55)
        for t in tickets:
            print(f"{t[0]:<5} {t[1]:<25} {t[2]:<10} {t[3]:<10}")

    def resolve_ticket(self, ticket_id):
        # Updates status, similar to SAP ticket lifecycle management
        self.conn.execute("UPDATE tickets SET status = 'CLOSED' WHERE id = ?", (ticket_id,))
        self.conn.commit()
        print(f"Ticket #{ticket_id} has been marked as RESOLVED.")

# --- Main Console Loop ---
def main():
    sd = ServiceDesk()
    while True:
        print("\n1. Raise New Ticket\n2. View Active Tickets\n3. Resolve Ticket\n4. Exit")
        choice = input("Select Option: ")

        if choice == '1':
            d = input("Issue Description: ")
            p = input("Priority (High/Medium/Low): ").upper()
            sd.raise_ticket(d, p)
        elif choice == '2':
            sd.display_active_tickets()
        elif choice == '3':
            tid = input("Enter Ticket ID to Resolve: ")
            sd.resolve_ticket(tid)
        elif choice == '4':
            break

if __name__ == "__main__":
    main()