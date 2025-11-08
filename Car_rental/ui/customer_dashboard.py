"""
Customer Dashboard for Car Rental System
Optimized with bug fixes and improved UI rendering
"""
import customtkinter as ctk
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from database import Database
from models import Car, Booking, Payment
from ui.components import (ModernButton, ModernEntry, ModernLabel, ModernFrame,
                          Card, DataTable, show_message, ask_confirmation)
from config import Config
import utils


class CustomerDashboard(ctk.CTkToplevel):
    """Customer dashboard window"""
    def __init__(self, parent, user):
        super().__init__(parent)
        
        self.user = user
        self.db = Database()
        
        self.title(f"{Config.APP_NAME} - Customer Dashboard")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # Center window on screen
        self.center_window()
        
        # Create UI
        self.create_dashboard_ui()
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (Config.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (Config.WINDOW_HEIGHT // 2)
        self.geometry(f'{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}')
    
    def create_dashboard_ui(self):
        """Create main dashboard UI"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_container, fg_color=Config.BG_COLOR)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Show home by default
        self.show_home()
    
    def create_sidebar(self, parent):
        """Create sidebar navigation"""
        sidebar = ctk.CTkFrame(parent, width=250, fg_color=Config.PRIMARY_COLOR, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Header
        header_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        header_frame.pack(pady=30, padx=20)
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🚗",
            font=("Roboto", 40)
        )
        icon_label.pack()
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Customer Portal",
            font=("Roboto", 18, "bold"),
            text_color="white"
        )
        title_label.pack()
        
        # User info
        user_frame = ctk.CTkFrame(sidebar, fg_color=Config.SECONDARY_COLOR, corner_radius=10)
        user_frame.pack(pady=20, padx=15, fill="x")
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.user.name}",
            font=("Roboto", 14),
            text_color="white"
        )
        user_label.pack(pady=10, padx=10)
        
        email_label = ctk.CTkLabel(
            user_frame,
            text=self.user.email,
            font=("Roboto", 10),
            text_color="lightgray"
        )
        email_label.pack(pady=(0, 10), padx=10)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Home", self.show_home),
            ("🚗 Browse Cars", self.show_browse_cars),
            ("📅 My Bookings", self.show_my_bookings),
            ("💰 Payment History", self.show_payment_history),
            ("👤 My Profile", self.show_profile),
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                text_color="white",
                hover_color=Config.SECONDARY_COLOR,
                anchor="w",
                height=45,
                font=("Roboto", 14)
            )
            btn.pack(pady=5, padx=15, fill="x")
        
        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            sidebar,
            text="🚪 Logout",
            command=self.handle_logout,
            fg_color=Config.DANGER_COLOR,
            hover_color="#c0392b",
            height=45,
            font=("Roboto", 14, "bold")
        )
        logout_btn.pack(side="bottom", pady=20, padx=15, fill="x")
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Show home/dashboard"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text=f"Welcome back, {self.user.name.split()[0]}! 👋",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Quick stats
        try:
            bookings = self.db.get_customer_bookings(self.user.uid)
            active_bookings = [b for b in bookings if b.status == "Active"]
            completed_bookings = [b for b in bookings if b.status == "Completed"]
        except Exception as e:
            print(f"Error loading bookings: {e}")
            bookings = []
            active_bookings = []
            completed_bookings = []
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(pady=20, padx=30, fill="x")
        
        cards_data = [
            ("Active Bookings", str(len(active_bookings)), Config.WARNING_COLOR),
            ("Completed Bookings", str(len(completed_bookings)), Config.SUCCESS_COLOR),
            ("Total Bookings", str(len(bookings)), Config.PRIMARY_COLOR),
        ]
        
        for title, value, color in cards_data:
            card = Card(stats_frame, title, value, color)
            card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Quick actions
        actions_frame = ModernFrame(self.content_frame)
        actions_frame.pack(pady=20, padx=30, fill="x")
        
        actions_title = ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=("Roboto", 18, "bold")
        )
        actions_title.pack(pady=20, padx=20, anchor="w")
        
        actions_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_container.pack(pady=10, padx=20, fill="x")
        
        browse_btn = ModernButton(
            actions_container,
            text="🚗 Browse Available Cars",
            command=self.show_browse_cars,
            width=250,
            color=Config.SUCCESS_COLOR
        )
        browse_btn.pack(side="left", padx=10)
        
        bookings_btn = ModernButton(
            actions_container,
            text="📅 View My Bookings",
            command=self.show_my_bookings,
            width=250
        )
        bookings_btn.pack(side="left", padx=10)
        
        # Recent bookings
        if bookings:
            recent_frame = ModernFrame(self.content_frame)
            recent_frame.pack(pady=20, padx=30, fill="both", expand=True)
            
            recent_title = ctk.CTkLabel(
                recent_frame,
                text="Recent Bookings",
                font=("Roboto", 18, "bold")
            )
            recent_title.pack(pady=15, padx=20, anchor="w")
            
            table = DataTable(
                recent_frame,
                headers=["Booking ID", "Car", "Start Date", "End Date", "Amount", "Status"],
                height=250
            )
            table.pack(pady=10, padx=20, fill="both", expand=True)
            
            for booking in bookings[:5]:  # Latest 5
                table.add_row([
                    booking.booking_id,
                    booking.car_info,
                    utils.format_date(booking.start_date),
                    utils.format_date(booking.end_date),
                    utils.format_currency(booking.total_amount),
                    booking.status
                ])
    
    def show_browse_cars(self):
        """Show available cars for booking"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Browse Available Cars",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Cars grid container with scrollable frame
        cars_scroll = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=Config.PRIMARY_COLOR
        )
        cars_scroll.pack(pady=20, padx=30, fill="both", expand=True)
        
        try:
            cars = self.db.get_available_cars()
        except Exception as e:
            print(f"Error loading cars: {e}")
            cars = []
        
        if cars:
            # Create grid of car cards
            for i, car in enumerate(cars):
                row = i // 3
                col = i % 3
                
                car_card = self.create_car_card(cars_scroll, car)
                car_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Configure grid weights for responsive layout
            for i in range(3):
                cars_scroll.grid_columnconfigure(i, weight=1, uniform="column")
        else:
            no_cars_label = ctk.CTkLabel(
                cars_scroll,
                text="No cars available at the moment. Please check back later.",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_cars_label.pack(pady=50)
    
    def create_car_card(self, parent, car):
        """Create a card for displaying car information"""
        # Main card frame - FIXED: Removed pack_propagate(False)
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=("gray90", "gray20"))
        
        # Content container inside card
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Car icon
        icon_label = ctk.CTkLabel(
            content,
            text="🚗",
            font=("Roboto", 50)
        )
        icon_label.pack(pady=(10, 5))
        
        # Car name
        name_label = ctk.CTkLabel(
            content,
            text=f"{car.brand} {car.model}",
            font=("Roboto", 18, "bold")
        )
        name_label.pack(pady=5)
        
        # Car details
        details_frame = ctk.CTkFrame(content, fg_color="transparent")
        details_frame.pack(pady=10, fill="x")
        
        details = [
            f"📅 Year: {car.year}",
            f"🎨 Color: {car.color}",
            f"⛽ Fuel: {car.fuel_type}",
            f"👥 Seats: {car.seats}",
        ]
        
        for detail in details:
            detail_label = ctk.CTkLabel(
                details_frame,
                text=detail,
                font=("Roboto", 11),
                anchor="w"
            )
            detail_label.pack(anchor="w", pady=2)
        
        # Price
        price_label = ctk.CTkLabel(
            content,
            text=f"{utils.format_currency(car.daily_rate)}/day",
            font=("Roboto", 20, "bold"),
            text_color=Config.SUCCESS_COLOR
        )
        price_label.pack(pady=10)
        
        # Book button - FIXED: Using lambda to prevent immediate execution
        book_btn = ctk.CTkButton(
            content,
            text="Book Now",
            command=lambda c=car: self.show_booking_dialog(c),
            fg_color=Config.SUCCESS_COLOR,
            hover_color="#27ae60",
            height=40,
            font=("Roboto", 14, "bold"),
            corner_radius=8
        )
        book_btn.pack(pady=(10, 5), fill="x")
        
        return card
    
    def show_booking_dialog(self, car):
        """Show booking dialog for selected car"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Book {car.brand} {car.model}")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Main form frame
        form_frame = ctk.CTkScrollableFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Car info header
        car_info_frame = ctk.CTkFrame(form_frame, fg_color=Config.PRIMARY_COLOR, corner_radius=10)
        car_info_frame.pack(pady=(0, 20), fill="x")
        
        car_icon = ctk.CTkLabel(car_info_frame, text="🚗", font=("Roboto", 40))
        car_icon.pack(pady=(15, 5))
        
        car_name = ctk.CTkLabel(
            car_info_frame,
            text=f"{car.brand} {car.model}",
            font=("Roboto", 20, "bold"),
            text_color="white"
        )
        car_name.pack()
        
        car_rate = ctk.CTkLabel(
            car_info_frame,
            text=f"{utils.format_currency(car.daily_rate)} per day",
            font=("Roboto", 14),
            text_color="white"
        )
        car_rate.pack(pady=(5, 15))
        
        # Date selection frame
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(pady=10, fill="x")
        
        # Start date
        start_label = ModernLabel(date_frame, text="Start Date", size=14, bold=True)
        start_label.pack(anchor="w", pady=(10, 5))
        
        start_date_entry = DateEntry(
            date_frame,
            width=45,
            background=Config.PRIMARY_COLOR,
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy',
            mindate=datetime.now(),
            font=("Roboto", 12)
        )
        start_date_entry.pack(pady=(0, 15), fill="x")
        
        # End date
        end_label = ModernLabel(date_frame, text="End Date", size=14, bold=True)
        end_label.pack(anchor="w", pady=(10, 5))
        
        end_date_entry = DateEntry(
            date_frame,
            width=45,
            background=Config.PRIMARY_COLOR,
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy',
            mindate=datetime.now() + timedelta(days=1),
            font=("Roboto", 12)
        )
        end_date_entry.pack(pady=(0, 15), fill="x")
        
        # Total amount display
        amount_frame = ctk.CTkFrame(date_frame, fg_color=("gray85", "gray25"), corner_radius=10)
        amount_frame.pack(pady=20, fill="x")
        
        amount_label = ctk.CTkLabel(
            amount_frame,
            text="Total Amount: ₹0.00",
            font=("Roboto", 18, "bold"),
            text_color=Config.SUCCESS_COLOR
        )
        amount_label.pack(pady=20)
        
        def update_amount(*args):
            """Calculate and update total amount"""
            try:
                start = start_date_entry.get_date()
                end = end_date_entry.get_date()
                
                if end <= start:
                    amount_label.configure(
                        text="⚠️ End date must be after start date",
                        text_color=Config.DANGER_COLOR
                    )
                    return
                
                days = utils.calculate_days(start, end)
                total = utils.calculate_total_amount(car.daily_rate, start, end)
                amount_label.configure(
                    text=f"Total Amount: {utils.format_currency(total)}\n({days} {'day' if days == 1 else 'days'})",
                    text_color=Config.SUCCESS_COLOR
                )
            except Exception as e:
                print(f"Error calculating amount: {e}")
                amount_label.configure(
                    text="Error calculating amount",
                    text_color=Config.DANGER_COLOR
                )
        
        # Bind date change events
        start_date_entry.bind("<<DateEntrySelected>>", update_amount)
        end_date_entry.bind("<<DateEntrySelected>>", update_amount)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=30)
        
        def confirm_booking():
            """Confirm and create booking"""
            try:
                start_date = start_date_entry.get_date()
                end_date = end_date_entry.get_date()
                
                # Validation
                if end_date <= start_date:
                    show_message(dialog, "Error", "End date must be after start date", "error")
                    return
                
                if start_date < datetime.now().date():
                    show_message(dialog, "Error", "Start date cannot be in the past", "error")
                    return
                
                # Check availability
                if not self.db.check_car_availability(car.car_id, start_date, end_date):
                    show_message(dialog, "Error", "Car is not available for selected dates", "error")
                    return
                
                # Calculate amount
                total_amount = utils.calculate_total_amount(car.daily_rate, start_date, end_date)
                
                # Create booking
                booking = Booking(
                    booking_id=self.db.generate_id("BOOK_"),
                    customer_id=self.user.uid,
                    car_id=car.car_id,
                    start_date=datetime.combine(start_date, datetime.min.time()),
                    end_date=datetime.combine(end_date, datetime.min.time()),
                    total_amount=total_amount,
                    status="Active",
                    customer_name=self.user.name,
                    car_info=f"{car.brand} {car.model}"
                )
                
                if self.db.create_booking(booking):
                    # Create payment record
                    payment = Payment(
                        payment_id=self.db.generate_id("PAY_"),
                        booking_id=booking.booking_id,
                        amount=total_amount,
                        payment_date=datetime.now(),
                        payment_method="Online",
                        status="Completed"
                    )
                    self.db.create_payment(payment)
                    
                    show_message(dialog, "Success", "Booking confirmed successfully!", "success")
                    dialog.destroy()
                    self.show_my_bookings()
                else:
                    show_message(dialog, "Error", "Failed to create booking. Please try again.", "error")
                
            except Exception as e:
                print(f"Booking error: {e}")
                show_message(dialog, "Error", f"Booking error: {str(e)}", "error")
        
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="✓ Confirm Booking",
            command=confirm_booking,
            width=180,
            height=45,
            fg_color=Config.SUCCESS_COLOR,
            hover_color="#27ae60",
            font=("Roboto", 14, "bold"),
            corner_radius=8
        )
        confirm_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="✗ Cancel",
            command=dialog.destroy,
            width=180,
            height=45,
            fg_color=Config.DANGER_COLOR,
            hover_color="#c0392b",
            font=("Roboto", 14, "bold"),
            corner_radius=8
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Initial amount calculation
        dialog.after(100, update_amount)
    
    def show_my_bookings(self):
        """Show customer's bookings"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="My Bookings",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Bookings table
        bookings_frame = ModernFrame(self.content_frame)
        bookings_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        try:
            bookings = self.db.get_customer_bookings(self.user.uid)
        except Exception as e:
            print(f"Error loading bookings: {e}")
            bookings = []
        
        if bookings:
            table = DataTable(
                bookings_frame,
                headers=["Booking ID", "Car", "Start Date", "End Date", "Amount", "Status", "Actions"],
                height=500
            )
            table.pack(pady=20, padx=20, fill="both", expand=True)
            
            for booking in bookings:
                table.add_row(
                    [
                        booking.booking_id,
                        booking.car_info,
                        utils.format_date(booking.start_date),
                        utils.format_date(booking.end_date),
                        utils.format_currency(booking.total_amount),
                        booking.status
                    ],
                    button_text="Cancel" if booking.status == "Active" else "View",
                    button_command=lambda b=booking: self.handle_booking_action(b)
                )
        else:
            no_data_label = ctk.CTkLabel(
                bookings_frame,
                text="No bookings found. Browse cars to make your first booking!",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
            
            browse_btn = ModernButton(
                bookings_frame,
                text="Browse Cars",
                command=self.show_browse_cars,
                width=200,
                color=Config.SUCCESS_COLOR
            )
            browse_btn.pack(pady=20)
    
    def handle_booking_action(self, booking):
        """Handle booking action (cancel/view)"""
        if booking.status == "Active":
            if ask_confirmation(self, "Cancel Booking", f"Are you sure you want to cancel booking {booking.booking_id}?"):
                try:
                    if self.db.cancel_booking(booking.booking_id):
                        show_message(self, "Success", "Booking cancelled successfully!", "success")
                        self.show_my_bookings()
                    else:
                        show_message(self, "Error", "Failed to cancel booking", "error")
                except Exception as e:
                    print(f"Error cancelling booking: {e}")
                    show_message(self, "Error", f"Error: {str(e)}", "error")
        else:
            self.show_booking_details(booking)
    
    def show_booking_details(self, booking):
        """Show detailed booking information"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Booking Details - {booking.booking_id}")
        dialog.geometry("450x550")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"450x550+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            frame,
            text="Booking Details",
            font=("Roboto", 24, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        title.pack(pady=20)
        
        # Details
        details_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        details_scroll.pack(pady=20, fill="both", expand=True)
        
        details = [
            ("Booking ID:", booking.booking_id),
            ("Car:", booking.car_info),
            ("Start Date:", utils.format_date(booking.start_date)),
            ("End Date:", utils.format_date(booking.end_date)),
            ("Duration:", f"{utils.calculate_days(booking.start_date, booking.end_date)} days"),
            ("Total Amount:", utils.format_currency(booking.total_amount)),
            ("Status:", booking.status),
            ("Booked On:", utils.format_datetime(booking.created_at)),
        ]
        
        for label, value in details:
            detail_container = ctk.CTkFrame(details_scroll, fg_color="transparent")
            detail_container.pack(fill="x", pady=8)
            
            label_widget = ctk.CTkLabel(
                detail_container,
                text=label,
                font=("Roboto", 12, "bold"),
                anchor="w"
            )
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(
                detail_container,
                text=value,
                font=("Roboto", 12),
                anchor="e"
            )
            value_widget.pack(side="right")
        
        # Close button
        close_btn = ModernButton(
            frame,
            text="Close",
            command=dialog.destroy,
            width=200
        )
        close_btn.pack(pady=20)
    
    def show_payment_history(self):
        """Show payment history"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Payment History",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        try:
            # Get customer's bookings to find payments
            bookings = self.db.get_customer_bookings(self.user.uid)
            booking_ids = [b.booking_id for b in bookings]
            
            # Get all payments and filter
            all_payments = self.db.get_all_payments()
            customer_payments = [p for p in all_payments if p.booking_id in booking_ids]
        except Exception as e:
            print(f"Error loading payments: {e}")
            customer_payments = []
        
        # Payments table
        payments_frame = ModernFrame(self.content_frame)
        payments_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        if customer_payments:
            table = DataTable(
                payments_frame,
                headers=["Payment ID", "Booking ID", "Amount", "Date", "Method", "Status"],
                height=500
            )
            table.pack(pady=20, padx=20, fill="both", expand=True)
            
            for payment in customer_payments:
                table.add_row([
                    payment.payment_id,
                    payment.booking_id,
                    utils.format_currency(payment.amount),
                    utils.format_datetime(payment.payment_date),
                    payment.payment_method,
                    payment.status
                ])
        else:
            no_data_label = ctk.CTkLabel(
                payments_frame,
                text="No payment records found",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
    
    def show_profile(self):
        """Show user profile"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="My Profile",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Profile frame
        profile_frame = ModernFrame(self.content_frame)
        profile_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # Profile icon
        icon = ctk.CTkLabel(
            profile_frame,
            text="👤",
            font=("Roboto", 80)
        )
        icon.pack(pady=30)
        
        # Profile details
        details_container = ctk.CTkFrame(profile_frame, fg_color="transparent")
        details_container.pack(pady=20, padx=50, fill="both", expand=True)
        
        details = [
            ("Name:", self.user.name),
            ("Email:", self.user.email),
            ("Phone:", self.user.phone),
            ("Address:", self.user.address),
            ("Member Since:", utils.format_date(self.user.created_at)),
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(details_container, fg_color="transparent")
            detail_frame.pack(fill="x", pady=15)
            
            label_widget = ctk.CTkLabel(
                detail_frame,
                text=label,
                font=("Roboto", 14, "bold"),
                anchor="w"
            )
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(
                detail_frame,
                text=value,
                font=("Roboto", 14),
                anchor="e"
            )
            value_widget.pack(side="right")
    
    def handle_logout(self):
        """Handle logout"""
        if ask_confirmation(self, "Confirm Logout", "Are you sure you want to logout?"):
            self.destroy()
