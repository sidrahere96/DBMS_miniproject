"""
Data models for Car Rental System
"""
from datetime import datetime
from typing import Optional, Dict, Any

class User:
    def __init__(self, uid: str, email: str, name: str, role: str, 
                 phone: str = "", address: str = "", created_at: datetime = None):
        self.uid = uid
        self.email = email
        self.name = name
        self.role = role  # 'admin' or 'customer'
        self.phone = phone
        self.address = address
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'uid': self.uid,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        return User(
            uid=data.get('uid', ''),
            email=data.get('email', ''),
            name=data.get('name', ''),
            role=data.get('role', 'customer'),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            created_at=data.get('created_at', datetime.now())
        )

class Car:
    def __init__(self, car_id: str, brand: str, model: str, year: int,
                 daily_rate: float, status: str = "Available", 
                 color: str = "", fuel_type: str = "", 
                 seats: int = 5, image_url: str = ""):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.status = status  # 'Available' or 'Booked'
        self.color = color
        self.fuel_type = fuel_type
        self.seats = seats
        self.image_url = image_url
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'car_id': self.car_id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'daily_rate': self.daily_rate,
            'status': self.status,
            'color': self.color,
            'fuel_type': self.fuel_type,
            'seats': self.seats,
            'image_url': self.image_url
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Car':
        return Car(
            car_id=data.get('car_id', ''),
            brand=data.get('brand', ''),
            model=data.get('model', ''),
            year=data.get('year', 2024),
            daily_rate=data.get('daily_rate', 0.0),
            status=data.get('status', 'Available'),
            color=data.get('color', ''),
            fuel_type=data.get('fuel_type', ''),
            seats=data.get('seats', 5),
            image_url=data.get('image_url', '')
        )

class Booking:
    def __init__(self, booking_id: str, customer_id: str, car_id: str,
                 start_date: datetime, end_date: datetime, 
                 total_amount: float, status: str = "Active",
                 customer_name: str = "", car_info: str = "",
                 created_at: datetime = None):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_amount = total_amount
        self.status = status  # 'Active', 'Completed', 'Cancelled'
        self.customer_name = customer_name
        self.car_info = car_info
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'booking_id': self.booking_id,
            'customer_id': self.customer_id,
            'car_id': self.car_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_amount': self.total_amount,
            'status': self.status,
            'customer_name': self.customer_name,
            'car_info': self.car_info,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Booking':
        return Booking(
            booking_id=data.get('booking_id', ''),
            customer_id=data.get('customer_id', ''),
            car_id=data.get('car_id', ''),
            start_date=data.get('start_date', datetime.now()),
            end_date=data.get('end_date', datetime.now()),
            total_amount=data.get('total_amount', 0.0),
            status=data.get('status', 'Active'),
            customer_name=data.get('customer_name', ''),
            car_info=data.get('car_info', ''),
            created_at=data.get('created_at', datetime.now())
        )

class Payment:
    def __init__(self, payment_id: str, booking_id: str, amount: float,
                 payment_date: datetime, payment_method: str = "Cash",
                 status: str = "Completed"):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'payment_date': self.payment_date,
            'payment_method': self.payment_method,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Payment':
        return Payment(
            payment_id=data.get('payment_id', ''),
            booking_id=data.get('booking_id', ''),
            amount=data.get('amount', 0.0),
            payment_date=data.get('payment_date', datetime.now()),
            payment_method=data.get('payment_method', 'Cash'),
            status=data.get('status', 'Completed')
        )
