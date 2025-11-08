"""
Database operations for Firebase Firestore
"""
from config import Config
from models import User, Car, Booking, Payment
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid

class Database:
    def __init__(self):
        self.db = Config.get_db()
    
    # User Operations
    def create_user(self, user: User) -> bool:
        """Create a new user in Firestore"""
        try:
            self.db.collection('users').document(user.uid).set(user.to_dict())
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user(self, uid: str) -> Optional[User]:
        """Get user by UID"""
        try:
            doc = self.db.collection('users').document(uid).get()
            if doc.exists:
                return User.from_dict(doc.to_dict())
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            users = self.db.collection('users').where('email', '==', email).limit(1).get()
            if users:
                return User.from_dict(users[0].to_dict())
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def update_user(self, uid: str, data: Dict[str, Any]) -> bool:
        """Update user information"""
        try:
            self.db.collection('users').document(uid).update(data)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def get_all_customers(self) -> List[User]:
        """Get all customers"""
        try:
            users = self.db.collection('users').where('role', '==', 'customer').get()
            return [User.from_dict(user.to_dict()) for user in users]
        except Exception as e:
            print(f"Error getting customers: {e}")
            return []
    
    def delete_user(self, uid: str) -> bool:
        """Delete a user"""
        try:
            self.db.collection('users').document(uid).delete()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    # Car Operations
    def add_car(self, car: Car) -> bool:
        """Add a new car"""
        try:
            self.db.collection('cars').document(car.car_id).set(car.to_dict())
            return True
        except Exception as e:
            print(f"Error adding car: {e}")
            return False
    
    def get_car(self, car_id: str) -> Optional[Car]:
        """Get car by ID"""
        try:
            doc = self.db.collection('cars').document(car_id).get()
            if doc.exists:
                return Car.from_dict(doc.to_dict())
            return None
        except Exception as e:
            print(f"Error getting car: {e}")
            return None
    
    def get_all_cars(self) -> List[Car]:
        """Get all cars"""
        try:
            cars = self.db.collection('cars').get()
            return [Car.from_dict(car.to_dict()) for car in cars]
        except Exception as e:
            print(f"Error getting cars: {e}")
            return []
    
    def get_available_cars(self) -> List[Car]:
        """Get all available cars"""
        try:
            cars = self.db.collection('cars').where('status', '==', 'Available').get()
            return [Car.from_dict(car.to_dict()) for car in cars]
        except Exception as e:
            print(f"Error getting available cars: {e}")
            return []
    
    def update_car(self, car_id: str, data: Dict[str, Any]) -> bool:
        """Update car information"""
        try:
            self.db.collection('cars').document(car_id).update(data)
            return True
        except Exception as e:
            print(f"Error updating car: {e}")
            return False
    
    def delete_car(self, car_id: str) -> bool:
        """Delete a car"""
        try:
            self.db.collection('cars').document(car_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting car: {e}")
            return False
    
    def update_car_status(self, car_id: str, status: str) -> bool:
        """Update car availability status"""
        return self.update_car(car_id, {'status': status})
    
    # Booking Operations
    def create_booking(self, booking: Booking) -> bool:
        """Create a new booking"""
        try:
            # Check for booking conflicts
            if not self.check_car_availability(booking.car_id, booking.start_date, booking.end_date):
                print("Car is not available for the selected dates")
                return False
            
            self.db.collection('bookings').document(booking.booking_id).set(booking.to_dict())
            # Update car status to Booked
            self.update_car_status(booking.car_id, 'Booked')
            return True
        except Exception as e:
            print(f"Error creating booking: {e}")
            return False
    
    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Get booking by ID"""
        try:
            doc = self.db.collection('bookings').document(booking_id).get()
            if doc.exists:
                return Booking.from_dict(doc.to_dict())
            return None
        except Exception as e:
            print(f"Error getting booking: {e}")
            return None
    
    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings"""
        try:
            bookings = self.db.collection('bookings').get()
            return [Booking.from_dict(booking.to_dict()) for booking in bookings]
        except Exception as e:
            print(f"Error getting bookings: {e}")
            return []
    
    def get_customer_bookings(self, customer_id: str) -> List[Booking]:
        """Get all bookings for a customer"""
        try:
            bookings = self.db.collection('bookings').where('customer_id', '==', customer_id).get()
            return [Booking.from_dict(booking.to_dict()) for booking in bookings]
        except Exception as e:
            print(f"Error getting customer bookings: {e}")
            return []
    
    def update_booking(self, booking_id: str, data: Dict[str, Any]) -> bool:
        """Update booking information"""
        try:
            self.db.collection('bookings').document(booking_id).update(data)
            return True
        except Exception as e:
            print(f"Error updating booking: {e}")
            return False
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        try:
            booking = self.get_booking(booking_id)
            if booking:
                self.update_booking(booking_id, {'status': 'Cancelled'})
                # Update car status back to Available
                self.update_car_status(booking.car_id, 'Available')
                return True
            return False
        except Exception as e:
            print(f"Error cancelling booking: {e}")
            return False
    
    def complete_booking(self, booking_id: str) -> bool:
        """Complete a booking"""
        try:
            booking = self.get_booking(booking_id)
            if booking:
                self.update_booking(booking_id, {'status': 'Completed'})
                # Update car status back to Available
                self.update_car_status(booking.car_id, 'Available')
                return True
            return False
        except Exception as e:
            print(f"Error completing booking: {e}")
            return False
    
    def check_car_availability(self, car_id: str, start_date: datetime, 
                               end_date: datetime, exclude_booking_id: str = None) -> bool:
        """Check if a car is available for the given date range"""
        try:
            # Get all active bookings for this car
            bookings = self.db.collection('bookings')\
                .where('car_id', '==', car_id)\
                .where('status', '==', 'Active')\
                .get()
            
            for booking_doc in bookings:
                booking_data = booking_doc.to_dict()
                
                # Skip if this is the booking being updated
                if exclude_booking_id and booking_data['booking_id'] == exclude_booking_id:
                    continue
                
                existing_start = booking_data['start_date']
                existing_end = booking_data['end_date']
                
                # Check for date overlap
                if not (end_date <= existing_start or start_date >= existing_end):
                    return False
            
            return True
        except Exception as e:
            print(f"Error checking car availability: {e}")
            return False
    
    # Payment Operations
    def create_payment(self, payment: Payment) -> bool:
        """Create a new payment record"""
        try:
            self.db.collection('payments').document(payment.payment_id).set(payment.to_dict())
            return True
        except Exception as e:
            print(f"Error creating payment: {e}")
            return False
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment by ID"""
        try:
            doc = self.db.collection('payments').document(payment_id).get()
            if doc.exists:
                return Payment.from_dict(doc.to_dict())
            return None
        except Exception as e:
            print(f"Error getting payment: {e}")
            return None
    
    def get_all_payments(self) -> List[Payment]:
        """Get all payments"""
        try:
            payments = self.db.collection('payments').get()
            return [Payment.from_dict(payment.to_dict()) for payment in payments]
        except Exception as e:
            print(f"Error getting payments: {e}")
            return []
    
    def get_booking_payments(self, booking_id: str) -> List[Payment]:
        """Get all payments for a booking"""
        try:
            payments = self.db.collection('payments').where('booking_id', '==', booking_id).get()
            return [Payment.from_dict(payment.to_dict()) for payment in payments]
        except Exception as e:
            print(f"Error getting booking payments: {e}")
            return []
    
    # Utility Methods
    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique ID"""
        return f"{prefix}{uuid.uuid4().hex[:8].upper()}"
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get statistics for dashboard"""
        try:
            total_cars = len(self.get_all_cars())
            available_cars = len(self.get_available_cars())
            total_bookings = len(self.get_all_bookings())
            active_bookings = len([b for b in self.get_all_bookings() if b.status == 'Active'])
            total_customers = len(self.get_all_customers())
            
            # Calculate total revenue
            payments = self.get_all_payments()
            total_revenue = sum(p.amount for p in payments)
            
            return {
                'total_cars': total_cars,
                'available_cars': available_cars,
                'booked_cars': total_cars - available_cars,
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'total_customers': total_customers,
                'total_revenue': total_revenue
            }
        except Exception as e:
            print(f"Error getting dashboard stats: {e}")
            return {}
