# Railway Reservation System 🚆🛤️

A comprehensive railway reservation platform that allows users to **book seats, cancel reservations, and manage waitlists dynamically**. Designed to support both individual and group/family bookings with optimal seat allocation.

## Features ✨

- **Seat Booking & Cancellation:** Users can book seats in real-time and cancel reservations if needed.  
- **Dynamic Waitlist Management:** Automatically manages waitlists and allocates seats as they become available.  
- **Block Reservations:** Ensures families or groups are seated together.  
- **Complex Query Handling:** Efficiently fetches and manages data using optimized MySQL queries.  
- **Responsive UI:** Clean and interactive interface built with React, HTML, CSS, and JavaScript.

## My Contributions 💻

- Designed and implemented complex **MySQL queries** for dynamic data retrieval and waitlist management.  
- Developed backend logic using **Django** and **FastAPI** for smooth service integration.  
- Ensured seamless **group and family seat allocation** with custom database handling.

## Tech Stack 🛠️

- **Backend:** Django, FastAPI  
- **Database:** MySQL  
- **Frontend:** React, HTML, CSS, JavaScript  

## How It Works ⚡

1. Users select train, date, and seats.  
2. The system checks availability and assigns seats or adds to waitlist.  
3. Block reservations ensure groups/families are seated together whenever possible.  
4. Users can cancel bookings; seats are dynamically reallocated to waitlisted passengers.  

## Getting Started 🚀

Clone the repository and set up the project locally:

```bash
git clone https://github.com/Chaitanyakotipalli/Reservation_System.git
cd Reservation_System
pip install -r requirements.txt
# Run Django backend
python manage.py runserver
# Start React frontend (if separate folder)
npm install
npm start
