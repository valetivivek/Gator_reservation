class GatorReservationSystem:
    def __init__(self):
        self.total_seats = 0
        self.available_seats = 0
        self.reservations = {}  # Seat -> User
        self.waitlist = []  # List of (user_id, priority)

    def initialize(self, seats):
        self.total_seats = seats
        self.available_seats = seats
        self.reservations = {}
        self.waitlist = []
        print(f"{self.total_seats} Seats are made available for reservation")

    def available(self):
        print(f"Total Seats Available : {self.available_seats}, Waitlist : {len(self.waitlist)}")

    def reserve(self, user_id, priority):
        if self.available_seats > 0:
            seat_num = self.total_seats - self.available_seats + 1
            self.reservations[seat_num] = user_id
            self.available_seats -= 1
            print(f"User {user_id} reserved seat {seat_num}")
        else:
            self.waitlist.append((user_id, priority))
            print(f"User {user_id} is added to the waiting list")

    def cancel(self, user_id, seat_num):
        if seat_num in self.reservations and self.reservations[seat_num] == user_id:
            del self.reservations[seat_num]
            self.available_seats += 1
            print(f"User {user_id} canceled their reservation")
            self.process_waitlist()
        else:
            print(f"User {user_id} has no reservation for seat {seat_num} to cancel")

    def process_waitlist(self):
        if self.available_seats > 0 and self.waitlist:
            self.waitlist.sort(key=lambda x: x[1])  # Sort by priority
            next_user = self.waitlist.pop(0)
            self.reserve(next_user[0], next_user[1])

    def print_reservations(self):
        for seat, user in sorted(self.reservations.items()):
            print(f"Seat {seat}, User {user}")

    def add_seats(self, seats):
        self.total_seats += seats
        self.available_seats += seats
        print(f"Additional {seats} Seats are made available for reservation")

    def release_seats(self, start_seat, end_seat):
        for seat in range(start_seat, end_seat + 1):
            if seat in self.reservations:
                del self.reservations[seat]
                self.available_seats += 1
        self.process_waitlist()
        print(f"Reservations of the Users in the range [{start_seat}, {end_seat}] are released")

    def update_priority(self, user_id, new_priority):
        for i in range(len(self.waitlist)):
            if self.waitlist[i][0] == user_id:
                self.waitlist[i] = (user_id, new_priority)
                print(f"User {user_id} priority has been updated to {new_priority}")
                return
        print(f"User {user_id} is not in waitlist")


# Function to handle dynamic inputs
def handle_dynamic_inputs():
    system = GatorReservationSystem()

    while True:
        command = input().strip()
        if command.startswith("Initialize"):
            _, seats = command.split("(")
            seats = int(seats[:-1])
            system.initialize(seats)

        elif command == "Available()":
            system.available()

        elif command.startswith("Reserve"):
            _, params = command.split("(")
            user_id, priority = map(int, params[:-1].split(", "))
            system.reserve(user_id, priority)

        elif command.startswith("Cancel"):
            _, params = command.split("(")
            user_id, seat_num = map(int, params[:-1].split(", "))
            system.cancel(user_id, seat_num)

        elif command == "PrintReservations()":
            system.print_reservations()

        elif command.startswith("AddSeats"):
            _, seats = command.split("(")
            seats = int(seats[:-1])
            system.add_seats(seats)

        elif command.startswith("ReleaseSeats"):
            _, params = command.split("(")
            start_seat, end_seat = map(int, params[:-1].split(", "))
            system.release_seats(start_seat, end_seat)

        elif command.startswith("UpdatePriority"):
            _, params = command.split("(")
            user_id, new_priority = map(int, params[:-1].split(", "))
            system.update_priority(user_id, new_priority)

        elif command == "Quit()":
            print("Program Terminated!!")
            break

# Call the function to start the system
handle_dynamic_inputs()
