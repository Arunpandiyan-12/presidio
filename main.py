import hashlib

class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.is_admin = is_admin

class Flight:
    def __init__(self, flight_id, flight_name, source, destination, date, seat_count=60, seat_price=100):
        self.flight_id = flight_id
        self.flight_name = flight_name
        self.source = source
        self.destination = destination
        self.date = date
        self.seat_count = seat_count
        self.available_seats = seat_count
        self.seat_price = seat_price

class Booking:
    def __init__(self, user, flight):
        self.user = user
        self.flight = flight
        self.cost = flight.seat_price
        self.canceled = False

class FlightBookingSystem:
    def __init__(self):
        self.users = [
            User("admin", "admin_password", is_admin=True),
            User("user1", "user1_password"),
            User("user2", "user2_password")
        ]
        self.flights = [
            Flight(1, "Flight1", "CityA", "CityB", "2023-11-20"),
            Flight(2, "Flight2", "CityB", "CityC", "2023-11-21"),
            Flight(3, "Flight3", "CityC", "CityA", "2023-11-22")
        ]
        self.bookings = []
        self.logged_in_user = None

    def signup(self):
        print("=== User Signup ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = User(username, password)
        self.users.append(user)
        print("Signup successful. Please login.")

    def login(self):
        print("=== User Login ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = next((u for u in self.users if u.username == username and u.password == hashed_password), None)
        if user:
            self.logged_in_user = user
            print("Login successful.")
        else:
            print("Invalid username or password.")

    def view_available_flights(self):
        print("=== View Available Flights ===")
        if not self.flights:
            print("No flights available.")
            return

        print("Available flights:")
        for flight in self.flights:
            print(f"Flight ID: {flight.flight_id}, Flight Name: {flight.flight_name}, Source: {flight.source}, "
                  f"Destination: {flight.destination}, Date: {flight.date}, Available Seats: {flight.available_seats}, "
                  f"Seat Price: {flight.seat_price}")

    def book_ticket(self):
        print("=== Book Ticket ===")
        if not self.logged_in_user:
            print("Please login first.")
            return

        flight_id = input("Enter Flight ID to book a ticket: ")
        selected_flight = next((flight for flight in self.flights if str(flight.flight_id) == flight_id and flight.available_seats > 0), None)

        if selected_flight:
            print(f"Selected Flight: {selected_flight.flight_name}")
            print(f"Source: {selected_flight.source}")
            print(f"Destination: {selected_flight.destination}")
            print(f"Available Seats: {selected_flight.available_seats}")
            num_tickets = int(input("How many tickets do you want to book? "))

            if 0 < num_tickets <= selected_flight.available_seats:
                ticket_cost = num_tickets * selected_flight.seat_price
                confirm = input(f"Total Cost: ${ticket_cost}. Do you want to proceed? (yes/no): ").lower()

                if confirm == 'yes':
                    booking = Booking(self.logged_in_user, selected_flight)
                    self.bookings.append(booking)
                    selected_flight.available_seats -= num_tickets
                    print(f"Booking successful. Enjoy your flight! Total Cost: ${ticket_cost}")
                else:
                    print("Booking canceled.")
            else:
                print("Invalid number of tickets.")
        else:
            print("Sorry, no available seats on this flight.")

    def view_flight_seats(self):
        print("=== View Flight Seats ===")
        flight_id = input("Enter Flight ID to view available seats: ")
        selected_flight = next((flight for flight in self.flights if str(flight.flight_id) == flight_id), None)

        if selected_flight:
            print(f"Flight ID: {selected_flight.flight_id}, Flight Name: {selected_flight.flight_name}, "
                  f"Available Seats: {selected_flight.available_seats}")
        else:
            print("Flight not found.")

    def add_flight(self):
        print("=== Add Flight ===")
        if not self.logged_in_user or not self.logged_in_user.is_admin:
            print("You do not have permission to add a flight.")
            return

        flight_id = input("Enter Flight ID: ")
        flight_name = input("Enter Flight Name: ")
        source = input("Enter Source: ")
        destination = input("Enter Destination: ")
        date = input("Enter Date: ")
        seat_count = int(input("Enter Seat Count: "))
        seat_price = int(input("Enter Seat Price: "))
        flight = Flight(flight_id, flight_name, source, destination, date, seat_count, seat_price)
        self.flights.append(flight)
        print("Flight added successfully.")

    def view_bookings(self):
        print("=== View Bookings ===")
        if not self.logged_in_user or not self.logged_in_user.is_admin:
            print("You do not have permission to view bookings.")
            return

        if not self.bookings:
            print("No bookings available.")
            return

        print("Bookings:")
        for booking in self.bookings:
            print(f"Username: {booking.user.username}, Flight Name: {booking.flight.flight_name}, "
                  f"Date: {booking.flight.date}, Cost: ${booking.cost}")

    def cancel_booking(self):
        print("=== Cancel Booking ===")
        if not self.logged_in_user or self.logged_in_user.is_admin:
            print("You do not have permission to cancel bookings.")
            return

        if not self.bookings:
            print("No bookings available to cancel.")
            return

        username = self.logged_in_user.username
        user_bookings = [booking for booking in self.bookings if booking.user.username == username and not booking.canceled]

        if not user_bookings:
            print("No bookings available for this user.")
            return

        print("Your bookings:")
        for i, booking in enumerate(user_bookings, 1):
            print(f"{i}. Flight Name: {booking.flight.flight_name}, Date: {booking.flight.date}, Cost: ${booking.cost}")

        flight_id_to_cancel = input("Enter Flight ID to cancel the booking: ")
        matching_booking = next((booking for booking in user_bookings if str(booking.flight.flight_id) == flight_id_to_cancel), None)

        if matching_booking:
            confirm = input("Are you sure you want to cancel this booking? (yes/no): ").lower()
            if confirm == 'yes':
                matching_booking.canceled = True
                canceled_flight = matching_booking.flight
                canceled_flight.available_seats += 1
                print(f"Booking canceled. Refunded ${matching_booking.cost}.")

                # Check if there are any remaining bookings for the user
                if not any(not booking.canceled for booking in user_bookings):
                    print("No more bookings left to cancel.")
            else:
                print("Booking not canceled.")
        else:
            print("Invalid Flight ID or no matching booking found.")

    def search_flights(self):
        print("=== Search Flights ===")
        search_criteria = input("Enter Flight Name/Date/Flight Number: ").lower()
        
        matching_flights = [
            flight for flight in self.flights
            if (
                search_criteria in flight.flight_name.lower() or
                search_criteria == flight.date or
                search_criteria == str(flight.flight_id)
            )
        ]

        if matching_flights:
            print("Matching Flights:")
            for flight in matching_flights:
                print(
                    f"Flight ID: {flight.flight_id}, Flight Name: {flight.flight_name}, "
                    f"Source: {flight.source}, Destination: {flight.destination}, "
                    f"Date: {flight.date}, Available Seats: {flight.available_seats}, "
                    f"Seat Price: {flight.seat_price}"
                )
        else:
            print("No matching flights found.")


if __name__ == "__main__":
    flight_system = FlightBookingSystem()

    while True:
        print("\n=== Flight Booking System ===")
        if not flight_system.logged_in_user:
            print("1. Signup")
            print("2. Login")
        elif flight_system.logged_in_user.is_admin:
            print("3. Add Flight")
            print("4. Delete Flight")
            print("5. View Bookings")
        else:
            print("3. View Available Flights")
            print("4. Book Ticket")
            print("5. View Flight Seats")
            print("6. Cancel Booking")
            print("7. Search Flights")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            flight_system.signup()
        elif choice == '2':
            flight_system.login()
        elif choice == '3':
            if flight_system.logged_in_user and flight_system.logged_in_user.is_admin:
                flight_system.add_flight()
            else:
                flight_system.view_available_flights()
        elif choice == '4':
            if flight_system.logged_in_user and flight_system.logged_in_user.is_admin:
                flight_system.delete_flight()
            else:
                flight_system.book_ticket()
        elif choice == '5':
            if flight_system.logged_in_user and flight_system.logged_in_user.is_admin:
                flight_system.view_bookings()
            else:
                flight_system.view_flight_seats()
        elif choice == '6':
            if flight_system.logged_in_user and not flight_system.logged_in_user.is_admin:
                flight_system.cancel_booking()
            else:
                print("Invalid choice. Please enter a valid option.")
        elif choice == '7':
            if not flight_system.logged_in_user or flight_system.logged_in_user.is_admin:
                print("Invalid choice. Please enter a valid option.")
            else:
                flight_system.search_flights()
        elif choice == '8':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
