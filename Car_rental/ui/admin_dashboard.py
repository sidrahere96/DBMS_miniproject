"""
Admin Dashboard for Car Rental System
Complete version with all bug fixes and proper button visibility
"""
import customtkinter as ctk
from datetime import datetime
from database import Database
from models import Car, Booking, Payment
from ui.components import (ModernButton, ModernEntry, ModernLabel, ModernFrame,
                          Card, DataTable, show_message, ask_confirmation)
from config import Config
import utils


class AdminDashboard(ctk.CTkToplevel):
    """Admin dashboard window"""
    def __init__(self, parent, user):
        super().__init__(parent)
        
        self.user = user
        self.db = Database()
        
        self.title(f"{Config.APP_NAME} - Admin Dashboard")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # Center window
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
            text="Admin Panel",
            font=("Roboto", 20, "bold"),
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
        user_label.pack(pady=15)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", self.show_home),
            ("🚗 Manage Cars", self.show_cars),
            ("📅 Bookings", self.show_bookings),
            ("👥 Customers", self.show_customers),
            ("💰 Payments", self.show_payments),
            ("📊 Reports", self.show_reports),
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
        """Show home/dashboard with statistics"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard Overview",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        try:
            # Get statistics
            stats = self.db.get_dashboard_stats()
        except Exception as e:
            print(f"Error loading dashboard stats: {e}")
            stats = {}
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(pady=20, padx=30, fill="x")
        
        cards_data = [
            ("Total Cars", str(stats.get('total_cars', 0)), Config.PRIMARY_COLOR),
            ("Available Cars", str(stats.get('available_cars', 0)), Config.SUCCESS_COLOR),
            ("Active Bookings", str(stats.get('active_bookings', 0)), Config.WARNING_COLOR),
            ("Total Revenue", utils.format_currency(stats.get('total_revenue', 0)), Config.SECONDARY_COLOR),
        ]
        
        for title, value, color in cards_data:
            card = Card(stats_frame, title, value, color)
            card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Recent bookings
        bookings_frame = ModernFrame(self.content_frame)
        bookings_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        bookings_title = ctk.CTkLabel(
            bookings_frame,
            text="Recent Bookings",
            font=("Roboto", 18, "bold")
        )
        bookings_title.pack(pady=15, padx=20, anchor="w")
        
        try:
            # Bookings table
            bookings = self.db.get_all_bookings()[:10]  # Latest 10
        except Exception as e:
            print(f"Error loading bookings: {e}")
            bookings = []
        
        if bookings:
            table = DataTable(
                bookings_frame,
                headers=["Booking ID", "Customer", "Car", "Start Date", "End Date", "Amount", "Status"],
                height=300
            )
            table.pack(pady=10, padx=20, fill="both", expand=True)
            
            for booking in bookings:
                table.add_row([
                    booking.booking_id,
                    booking.customer_name,
                    booking.car_info,
                    utils.format_date(booking.start_date),
                    utils.format_date(booking.end_date),
                    utils.format_currency(booking.total_amount),
                    booking.status
                ])
        else:
            no_data_label = ctk.CTkLabel(
                bookings_frame,
                text="No bookings found",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
    
    def show_cars(self):
        """Show car management interface with grid layout"""
        self.clear_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(pady=30, padx=30, fill="x")
        
        header = ctk.CTkLabel(
            header_frame,
            text="Manage Cars",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(side="left")
        
        add_btn = ModernButton(
            header_frame,
            text="+ Add New Car",
            command=self.show_add_car_dialog,
            color=Config.SUCCESS_COLOR,
            width=150
        )
        add_btn.pack(side="right")
        
        # Cars grid with scrollable frame
        cars_scroll = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=Config.PRIMARY_COLOR
        )
        cars_scroll.pack(pady=20, padx=30, fill="both", expand=True)
        
        try:
            cars = self.db.get_all_cars()
        except Exception as e:
            print(f"Error loading cars: {e}")
            cars = []
        
        if cars:
            # Create grid of car cards
            for i, car in enumerate(cars):
                row = i // 2
                col = i % 2
                
                car_card = self.create_car_card(cars_scroll, car)
                car_card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            # Configure grid weights
            cars_scroll.grid_columnconfigure(0, weight=1, uniform="column")
            cars_scroll.grid_columnconfigure(1, weight=1, uniform="column")
        else:
            no_data_label = ctk.CTkLabel(
                cars_scroll,
                text="No cars found. Click 'Add New Car' to add one.",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
    
    def create_car_card(self, parent, car):
        """Create a card for displaying car with edit/delete buttons"""
        # Main card frame
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=("gray90", "gray20"))
        
        # Content container
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
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
            font=("Roboto", 20, "bold")
        )
        name_label.pack(pady=5)
        
        # Car ID
        id_label = ctk.CTkLabel(
            content,
            text=f"ID: {car.car_id}",
            font=("Roboto", 10),
            text_color="gray"
        )
        id_label.pack(pady=2)
        
        # Separator
        separator = ctk.CTkFrame(content, height=2, fg_color="gray")
        separator.pack(fill="x", pady=15)
        
        # Car details in two columns
        details_frame = ctk.CTkFrame(content, fg_color="transparent")
        details_frame.pack(pady=10, fill="x")
        
        # Left column
        left_col = ctk.CTkFrame(details_frame, fg_color="transparent")
        left_col.pack(side="left", fill="x", expand=True)
        
        details_left = [
            f"📅 Year: {car.year}",
            f"🎨 Color: {car.color}",
            f"⛽ Fuel: {car.fuel_type}",
        ]
        
        for detail in details_left:
            detail_label = ctk.CTkLabel(
                left_col,
                text=detail,
                font=("Roboto", 11),
                anchor="w"
            )
            detail_label.pack(anchor="w", pady=3)
        
        # Right column
        right_col = ctk.CTkFrame(details_frame, fg_color="transparent")
        right_col.pack(side="right", fill="x", expand=True)
        
        details_right = [
            f"👥 Seats: {car.seats}",
            f"📊 Status: {car.status}",
            f"",  # Empty for alignment
        ]
        
        for detail in details_right:
            detail_label = ctk.CTkLabel(
                right_col,
                text=detail,
                font=("Roboto", 11),
                anchor="w"
            )
            detail_label.pack(anchor="w", pady=3)
        
        # Price
        price_frame = ctk.CTkFrame(content, fg_color=Config.SUCCESS_COLOR, corner_radius=8)
        price_frame.pack(pady=15, fill="x")
        
        price_label = ctk.CTkLabel(
            price_frame,
            text=f"{utils.format_currency(car.daily_rate)}/day",
            font=("Roboto", 18, "bold"),
            text_color="white"
        )
        price_label.pack(pady=10)
        
        # Action buttons frame
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(pady=(10, 5), fill="x")
        
        # Edit button
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Edit",
            command=lambda c=car: self.show_edit_car_dialog(c),
            fg_color=Config.PRIMARY_COLOR,
            hover_color=Config.SECONDARY_COLOR,
            width=120,
            height=35,
            font=("Roboto", 13, "bold"),
            corner_radius=8
        )
        edit_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Delete button
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Delete",
            command=lambda c=car: self.confirm_delete_car(c),
            fg_color=Config.DANGER_COLOR,
            hover_color="#c0392b",
            width=120,
            height=35,
            font=("Roboto", 13, "bold"),
            corner_radius=8
        )
        delete_btn.pack(side="right", padx=5, expand=True, fill="x")
        
        return card
    
    def show_add_car_dialog(self):
        """Show dialog to add new car"""
        self.show_car_form_dialog(None)
    
    def show_edit_car_dialog(self, car):
        """Show dialog to edit car"""
        self.show_car_form_dialog(car)
    
    def show_car_form_dialog(self, car=None):
        """Show dialog to add or edit car"""
        is_edit = car is not None
        title = f"Edit Car - {car.brand} {car.model}" if is_edit else "Add New Car"
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("550x750")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (dialog.winfo_screenheight() // 2) - (750 // 2)
        dialog.geometry(f"550x750+{x}+{y}")
        
        # Form
        form_frame = ctk.CTkScrollableFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        form_title = ctk.CTkLabel(
            form_frame,
            text=title,
            font=("Roboto", 24, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        form_title.pack(pady=(0, 20))
        
        # Fields
        fields = {}
        
        field_configs = [
            ("Brand *", "brand", "Enter car brand (e.g., Toyota)"),
            ("Model *", "model", "Enter car model (e.g., Camry)"),
            ("Year *", "year", "Enter manufacturing year"),
            ("Daily Rate (₹) *", "daily_rate", "Enter daily rental rate"),
            ("Color *", "color", "Enter car color"),
            ("Fuel Type *", "fuel_type", "Petrol, Diesel, Electric, Hybrid"),
            ("Seats *", "seats", "Enter number of seats (1-50)"),
        ]
        
        for label_text, field_name, placeholder in field_configs:
            label = ModernLabel(form_frame, text=label_text, size=13, bold=True)
            label.pack(anchor="w", pady=(15, 5))
            
            entry = ModernEntry(form_frame, placeholder=placeholder, width=450)
            entry.pack(pady=(0, 10), fill="x")
            
            # Pre-fill if editing
            if is_edit:
                if field_name == "brand":
                    entry.insert(0, car.brand)
                elif field_name == "model":
                    entry.insert(0, car.model)
                elif field_name == "year":
                    entry.insert(0, str(car.year))
                elif field_name == "daily_rate":
                    entry.insert(0, str(car.daily_rate))
                elif field_name == "color":
                    entry.insert(0, car.color)
                elif field_name == "fuel_type":
                    entry.insert(0, car.fuel_type)
                elif field_name == "seats":
                    entry.insert(0, str(car.seats))
            
            fields[field_name] = entry
        
        # Status field (only for edit)
        if is_edit:
            status_label = ModernLabel(form_frame, text="Status *", size=13, bold=True)
            status_label.pack(anchor="w", pady=(15, 5))
            
            status_var = ctk.StringVar(value=car.status)
            status_menu = ctk.CTkOptionMenu(
                form_frame,
                values=["Available", "Booked", "Maintenance"],
                variable=status_var,
                width=450,
                height=40,
                font=("Roboto", 12),
                fg_color=Config.PRIMARY_COLOR,
                button_color=Config.SECONDARY_COLOR
            )
            status_menu.pack(pady=(0, 10), fill="x")
            fields['status'] = status_var
        
        # Required field note
        note_label = ctk.CTkLabel(
            form_frame,
            text="* Required fields",
            font=("Roboto", 10),
            text_color="gray"
        )
        note_label.pack(pady=(10, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_car():
            """Save or update car"""
            try:
                brand = fields['brand'].get().strip()
                model = fields['model'].get().strip()
                year_str = fields['year'].get().strip()
                rate_str = fields['daily_rate'].get().strip()
                color = fields['color'].get().strip()
                fuel_type = fields['fuel_type'].get().strip()
                seats_str = fields['seats'].get().strip()
                
                # Validation
                if not all([brand, model, year_str, rate_str, color, fuel_type, seats_str]):
                    show_message(dialog, "Error", "Please fill all required fields", "error")
                    return
                
                try:
                    year = int(year_str)
                    daily_rate = float(rate_str)
                    seats = int(seats_str)
                except ValueError:
                    show_message(dialog, "Error", "Year, Rate, and Seats must be valid numbers", "error")
                    return
                
                if year < 1900 or year > datetime.now().year + 1:
                    show_message(dialog, "Error", f"Year must be between 1900 and {datetime.now().year + 1}", "error")
                    return
                
                if daily_rate <= 0:
                    show_message(dialog, "Error", "Daily rate must be greater than 0", "error")
                    return
                
                if seats < 1 or seats > 50:
                    show_message(dialog, "Error", "Seats must be between 1 and 50", "error")
                    return
                
                if is_edit:
                    # Update existing car
                    status = fields['status'].get()
                    update_data = {
                        'brand': brand,
                        'model': model,
                        'year': year,
                        'daily_rate': daily_rate,
                        'color': color,
                        'fuel_type': fuel_type,
                        'seats': seats,
                        'status': status
                    }
                    
                    if self.db.update_car(car.car_id, update_data):
                        show_message(dialog, "Success", f"Car {brand} {model} updated successfully!", "success")
                        dialog.destroy()
                        self.show_cars()
                    else:
                        show_message(dialog, "Error", "Failed to update car. Please try again.", "error")
                else:
                    # Create new car
                    new_car = Car(
                        car_id=self.db.generate_id("CAR_"),
                        brand=brand,
                        model=model,
                        year=year,
                        daily_rate=daily_rate,
                        status="Available",
                        color=color,
                        fuel_type=fuel_type,
                        seats=seats
                    )
                    
                    if self.db.add_car(new_car):
                        show_message(dialog, "Success", f"Car {brand} {model} added successfully!", "success")
                        dialog.destroy()
                        self.show_cars()
                    else:
                        show_message(dialog, "Error", "Failed to add car. Please try again.", "error")
                    
            except Exception as e:
                print(f"Error saving car: {e}")
                show_message(dialog, "Error", f"An error occurred: {str(e)}", "error")
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="✓ Save Changes" if is_edit else "✓ Add Car",
            command=save_car,
            width=200,
            height=45,
            fg_color=Config.SUCCESS_COLOR,
            hover_color="#27ae60",
            font=("Roboto", 14, "bold"),
            corner_radius=8
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="✗ Cancel",
            command=dialog.destroy,
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray",
            font=("Roboto", 14, "bold"),
            corner_radius=8
        )
        cancel_btn.pack(side="left", padx=10)
    
    def confirm_delete_car(self, car):
        """Confirm and delete car"""
        if ask_confirmation(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete?\n\n{car.brand} {car.model} ({car.year})\n\nThis action cannot be undone."
        ):
            try:
                if self.db.delete_car(car.car_id):
                    show_message(self, "Success", f"Car {car.brand} {car.model} deleted successfully!", "success")
                    self.show_cars()
                else:
                    show_message(self, "Error", "Failed to delete car. It may be associated with bookings.", "error")
            except Exception as e:
                print(f"Error deleting car: {e}")
                show_message(self, "Error", f"An error occurred: {str(e)}", "error")
    
    def show_bookings(self):
        """Show all bookings"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="All Bookings",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Bookings table
        bookings_frame = ModernFrame(self.content_frame)
        bookings_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        try:
            bookings = self.db.get_all_bookings()
        except Exception as e:
            print(f"Error loading bookings: {e}")
            bookings = []
        
        if bookings:
            table = DataTable(
                bookings_frame,
                headers=["ID", "Customer", "Car", "Start", "End", "Amount", "Status", "Actions"],
                height=500
            )
            table.pack(pady=20, padx=20, fill="both", expand=True)
            
            for booking in bookings:
                table.add_row(
                    [
                        booking.booking_id,
                        booking.customer_name,
                        booking.car_info,
                        utils.format_date(booking.start_date),
                        utils.format_date(booking.end_date),
                        utils.format_currency(booking.total_amount),
                        booking.status
                    ],
                    button_text="Manage",
                    button_command=lambda b=booking: self.manage_booking(b)
                )
        else:
            no_data_label = ctk.CTkLabel(
                bookings_frame,
                text="No bookings found",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
    
    def manage_booking(self, booking):
        """Manage booking actions"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Manage Booking - {booking.booking_id}")
        dialog.geometry("450x350")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"450x350+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            frame,
            text=f"Booking {booking.booking_id}",
            font=("Roboto", 20, "bold")
        )
        title.pack(pady=20)
        
        info = ctk.CTkLabel(
            frame,
            text=f"Customer: {booking.customer_name}\nCar: {booking.car_info}\nStatus: {booking.status}\nAmount: {utils.format_currency(booking.total_amount)}",
            font=("Roboto", 12),
            justify="center"
        )
        info.pack(pady=10)
        
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        if booking.status == "Active":
            def complete():
                try:
                    if self.db.complete_booking(booking.booking_id):
                        show_message(dialog, "Success", "Booking completed successfully!", "success")
                        dialog.destroy()
                        self.show_bookings()
                    else:
                        show_message(dialog, "Error", "Failed to complete booking", "error")
                except Exception as e:
                    print(f"Error completing booking: {e}")
                    show_message(dialog, "Error", f"Error: {str(e)}", "error")
            
            complete_btn = ModernButton(
                button_frame,
                text="✓ Complete Booking",
                command=complete,
                color=Config.SUCCESS_COLOR,
                width=200
            )
            complete_btn.pack(pady=5)
        
        close_btn = ModernButton(
            button_frame,
            text="Close",
            command=dialog.destroy,
            width=200
        )
        close_btn.pack(pady=5)
    
    def show_customers(self):
        """Show all customers"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Customer Management",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Customers table
        customers_frame = ModernFrame(self.content_frame)
        customers_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        try:
            customers = self.db.get_all_customers()
        except Exception as e:
            print(f"Error loading customers: {e}")
            customers = []
        
        if customers:
            table = DataTable(
                customers_frame,
                headers=["Customer ID", "Name", "Email", "Phone", "Address"],
                height=500
            )
            table.pack(pady=20, padx=20, fill="both", expand=True)
            
            for customer in customers:
                table.add_row([
                    customer.uid,
                    customer.name,
                    customer.email,
                    customer.phone,
                    customer.address
                ])
        else:
            no_data_label = ctk.CTkLabel(
                customers_frame,
                text="No customers found",
                font=("Roboto", 14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
    
    def show_payments(self):
        """Show all payments"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Payment Records",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        # Payments table
        payments_frame = ModernFrame(self.content_frame)
        payments_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        try:
            payments = self.db.get_all_payments()
        except Exception as e:
            print(f"Error loading payments: {e}")
            payments = []
        
        if payments:
            table = DataTable(
                payments_frame,
                headers=["Payment ID", "Booking ID", "Amount", "Date", "Method", "Status"],
                height=500
            )
            table.pack(pady=20, padx=20, fill="both", expand=True)
            
            for payment in payments:
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
    
    def show_reports(self):
        """Show reports and analytics"""
        self.clear_content()
        
        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Reports & Analytics",
            font=("Roboto", 28, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        header.pack(pady=30, padx=30, anchor="w")
        
        try:
            # Get statistics
            stats = self.db.get_dashboard_stats()
        except Exception as e:
            print(f"Error loading stats: {e}")
            stats = {}
        
        # Report cards
        report_frame = ModernFrame(self.content_frame)
        report_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        report_data = [
            ("Total Cars", stats.get('total_cars', 0)),
            ("Available Cars", stats.get('available_cars', 0)),
            ("Booked Cars", stats.get('booked_cars', 0)),
            ("Total Bookings", stats.get('total_bookings', 0)),
            ("Active Bookings", stats.get('active_bookings', 0)),
            ("Total Customers", stats.get('total_customers', 0)),
            ("Total Revenue", utils.format_currency(stats.get('total_revenue', 0))),
        ]
        
        for i, (label, value) in enumerate(report_data):
            row = i // 2
            col = i % 2
            
            card_frame = ctk.CTkFrame(report_frame, corner_radius=12)
            card_frame.grid(row=row, column=col, padx=20, pady=20, sticky="ew")
            
            label_widget = ctk.CTkLabel(
                card_frame,
                text=label,
                font=("Roboto", 16, "bold")
            )
            label_widget.pack(pady=(20, 5))
            
            value_widget = ctk.CTkLabel(
                card_frame,
                text=str(value),
                font=("Roboto", 24, "bold"),
                text_color=Config.PRIMARY_COLOR
            )
            value_widget.pack(pady=(5, 20))
        
        report_frame.grid_columnconfigure(0, weight=1)
        report_frame.grid_columnconfigure(1, weight=1)
    
    def handle_logout(self):
        """Handle logout with proper cleanup"""
        if ask_confirmation(self, "Confirm Logout", "Are you sure you want to logout?"):
            try:
                print(f"Logging out admin: {self.user.email}")
                
                # Clear any cached data
                self.clear_content()
                
                # Close dashboard window
                self.destroy()
                
            except Exception as e:
                print(f"Logout error: {e}")
                # Force close even if error occurs
                try:
                    self.destroy()
                except:
                    pass
