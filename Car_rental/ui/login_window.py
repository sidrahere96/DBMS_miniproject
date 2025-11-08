"""
Login and Registration window for Car Rental System
Optimized with fullscreen support and proper logout handling
"""
import customtkinter as ctk
from auth import AuthManager
from ui.components import ModernButton, ModernEntry, ModernLabel, show_message
from config import Config
import utils


class LoginWindow(ctk.CTk):
    """Main login window"""
    def __init__(self):
        super().__init__()
        
        self.auth_manager = AuthManager()
        self.title(Config.APP_NAME)
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Set fullscreen
        self.attributes('-fullscreen', True)
        
        # Get screen dimensions
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Bind Escape key to exit fullscreen
        self.bind("<Escape>", self.toggle_fullscreen)
        self.bind("<F11>", self.toggle_fullscreen)
        
        # Create UI
        self.create_login_ui()
        
        # Update window to ensure proper rendering
        self.update_idletasks()
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        current_state = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not current_state)
        
        if not current_state:
            # Entering fullscreen
            self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        else:
            # Exiting fullscreen
            self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
            self.center_window()
    
    def center_window(self):
        """Center the window on screen (for non-fullscreen mode)"""
        self.update_idletasks()
        width = Config.WINDOW_WIDTH
        height = Config.WINDOW_HEIGHT
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_login_ui(self):
        """Create login interface"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Left side - Image/Branding
        left_frame = ctk.CTkFrame(main_frame, fg_color=Config.PRIMARY_COLOR, corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Brand content
        brand_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        brand_container.place(relx=0.5, rely=0.5, anchor="center")
        
        brand_label = ctk.CTkLabel(
            brand_container,
            text="🚗",
            font=("Roboto", 100)
        )
        brand_label.pack(pady=30)
        
        title_label = ctk.CTkLabel(
            brand_container,
            text=Config.APP_NAME,
            font=("Roboto", 42, "bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            brand_container,
            text="Your trusted car rental partner",
            font=("Roboto", 18),
            text_color="white"
        )
        subtitle_label.pack(pady=10)
        
        # Fullscreen hint
        hint_label = ctk.CTkLabel(
            brand_container,
            text="Press ESC or F11 to toggle fullscreen",
            font=("Roboto", 11),
            text_color="lightgray"
        )
        hint_label.pack(pady=(30, 0))
        
        # Right side - Login form
        right_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Login form container
        form_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Login title
        login_title = ctk.CTkLabel(
            form_container,
            text="Welcome Back",
            font=("Roboto", 32, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        login_title.pack(pady=(0, 10))
        
        login_subtitle = ctk.CTkLabel(
            form_container,
            text="Sign in to continue",
            font=("Roboto", 16),
            text_color="gray"
        )
        login_subtitle.pack(pady=(0, 40))
        
        # Email field
        email_label = ModernLabel(form_container, text="Email Address", size=13, bold=True)
        email_label.pack(anchor="w", pady=(0, 8))
        
        self.email_entry = ModernEntry(
            form_container,
            placeholder="Enter your email",
            width=400
        )
        self.email_entry.pack(pady=(0, 25))
        
        # Password field
        password_label = ModernLabel(form_container, text="Password", size=13, bold=True)
        password_label.pack(anchor="w", pady=(0, 8))
        
        self.password_entry = ModernEntry(
            form_container,
            placeholder="Enter your password",
            show="•",
            width=400
        )
        self.password_entry.pack(pady=(0, 40))
        
        # Login button
        login_btn = ModernButton(
            form_container,
            text="Login",
            command=self.handle_login,
            width=400
        )
        login_btn.pack(pady=(0, 25))
        
        # Register link
        register_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        register_frame.pack()
        
        register_label = ctk.CTkLabel(
            register_frame,
            text="Don't have an account?",
            font=("Roboto", 13),
            text_color="gray"
        )
        register_label.pack(side="left", padx=(0, 8))
        
        register_btn = ctk.CTkButton(
            register_frame,
            text="Register",
            command=self.create_register_ui,
            fg_color="transparent",
            text_color=Config.PRIMARY_COLOR,
            hover_color="#e8f4f8",
            width=90,
            height=35,
            font=("Roboto", 13, "bold")
        )
        register_btn.pack(side="left")
        
        # Bind Enter key
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Focus on email field
        self.email_entry.focus()
    
    def create_register_ui(self):
        """Create registration interface"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Left side - Image/Branding
        left_frame = ctk.CTkFrame(main_frame, fg_color=Config.PRIMARY_COLOR, corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Brand content
        brand_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        brand_container.place(relx=0.5, rely=0.5, anchor="center")
        
        brand_label = ctk.CTkLabel(
            brand_container,
            text="🚗",
            font=("Roboto", 100)
        )
        brand_label.pack(pady=30)
        
        title_label = ctk.CTkLabel(
            brand_container,
            text="Join Us Today",
            font=("Roboto", 42, "bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            brand_container,
            text="Start your journey with us",
            font=("Roboto", 18),
            text_color="white"
        )
        subtitle_label.pack(pady=10)
        
        # Fullscreen hint
        hint_label = ctk.CTkLabel(
            brand_container,
            text="Press ESC or F11 to toggle fullscreen",
            font=("Roboto", 11),
            text_color="lightgray"
        )
        hint_label.pack(pady=(30, 0))
        
        # Right side - Registration form
        right_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Scrollable form container
        form_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
        form_scroll.pack(fill="both", expand=True, padx=80, pady=60)
        
        # Center content
        form_container = ctk.CTkFrame(form_scroll, fg_color="transparent")
        form_container.pack(expand=True)
        
        # Register title
        register_title = ctk.CTkLabel(
            form_container,
            text="Create Account",
            font=("Roboto", 32, "bold"),
            text_color=Config.PRIMARY_COLOR
        )
        register_title.pack(pady=(0, 40))
        
        # Name field
        name_label = ModernLabel(form_container, text="Full Name *", size=13, bold=True)
        name_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_name_entry = ModernEntry(
            form_container,
            placeholder="Enter your full name",
            width=400
        )
        self.reg_name_entry.pack(pady=(0, 20))
        
        # Email field
        email_label = ModernLabel(form_container, text="Email Address *", size=13, bold=True)
        email_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_email_entry = ModernEntry(
            form_container,
            placeholder="Enter your email",
            width=400
        )
        self.reg_email_entry.pack(pady=(0, 20))
        
        # Phone field
        phone_label = ModernLabel(form_container, text="Phone Number *", size=13, bold=True)
        phone_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_phone_entry = ModernEntry(
            form_container,
            placeholder="Enter 10-digit phone number",
            width=400
        )
        self.reg_phone_entry.pack(pady=(0, 20))
        
        # Address field
        address_label = ModernLabel(form_container, text="Address *", size=13, bold=True)
        address_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_address_entry = ModernEntry(
            form_container,
            placeholder="Enter your address",
            width=400
        )
        self.reg_address_entry.pack(pady=(0, 20))
        
        # Password field
        password_label = ModernLabel(form_container, text="Password *", size=13, bold=True)
        password_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_password_entry = ModernEntry(
            form_container,
            placeholder="Create a password (min 6 characters)",
            show="•",
            width=400
        )
        self.reg_password_entry.pack(pady=(0, 20))
        
        # Confirm Password field
        confirm_label = ModernLabel(form_container, text="Confirm Password *", size=13, bold=True)
        confirm_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_confirm_entry = ModernEntry(
            form_container,
            placeholder="Confirm your password",
            show="•",
            width=400
        )
        self.reg_confirm_entry.pack(pady=(0, 35))
        
        # Register button
        register_btn = ModernButton(
            form_container,
            text="Create Account",
            command=self.handle_register,
            width=400
        )
        register_btn.pack(pady=(0, 25))
        
        # Login link
        login_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        login_frame.pack()
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account?",
            font=("Roboto", 13),
            text_color="gray"
        )
        login_label.pack(side="left", padx=(0, 8))
        
        login_btn = ctk.CTkButton(
            login_frame,
            text="Login",
            command=self.create_login_ui,
            fg_color="transparent",
            text_color=Config.PRIMARY_COLOR,
            hover_color="#e8f4f8",
            width=90,
            height=35,
            font=("Roboto", 13, "bold")
        )
        login_btn.pack(side="left")
        
        # Focus on first field
        self.reg_name_entry.focus()
    
    def handle_login(self):
        """Handle login action"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validation
        if not email or not password:
            show_message(self, "Error", "Please enter both email and password", "error")
            return
        
        if not utils.validate_email(email):
            show_message(self, "Error", "Please enter a valid email address", "error")
            return
        
        # Attempt login
        try:
            success, message, user = self.auth_manager.login(email, password)
            
            if success:
                show_message(self, "Success", "Login successful!", "success")
                self.open_dashboard(user)
            else:
                show_message(self, "Error", message, "error")
        except Exception as e:
            print(f"Login error: {e}")
            show_message(self, "Error", f"Login failed: {str(e)}", "error")
    
    def handle_register(self):
        """Handle registration action"""
        name = self.reg_name_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        phone = self.reg_phone_entry.get().strip()
        address = self.reg_address_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_entry.get()
        
        # Validation
        if not all([name, email, phone, address, password, confirm_password]):
            show_message(self, "Error", "Please fill all required fields", "error")
            return
        
        if not utils.validate_email(email):
            show_message(self, "Error", "Please enter a valid email address", "error")
            return
        
        if not utils.validate_phone(phone):
            show_message(self, "Error", "Please enter a valid 10-digit phone number starting with 6-9", "error")
            return
        
        if len(password) < 6:
            show_message(self, "Error", "Password must be at least 6 characters long", "error")
            return
        
        if password != confirm_password:
            show_message(self, "Error", "Passwords do not match", "error")
            return
        
        # Attempt registration
        try:
            success, message = self.auth_manager.register_user(
                email=email,
                password=password,
                name=name,
                role="customer",
                phone=phone,
                address=address
            )
            
            if success:
                show_message(self, "Success", "Registration successful! Please login.", "success")
                self.create_login_ui()
            else:
                show_message(self, "Error", message, "error")
        except Exception as e:
            print(f"Registration error: {e}")
            show_message(self, "Error", f"Registration failed: {str(e)}", "error")
    
    def open_dashboard(self, user):
        """Open appropriate dashboard based on user role"""
        try:
            self.withdraw()  # Hide login window
            
            if user.role == "admin":
                from ui.admin_dashboard import AdminDashboard
                dashboard = AdminDashboard(self, user)
            else:
                from ui.customer_dashboard import CustomerDashboard
                dashboard = CustomerDashboard(self, user)
            
            # Set dashboard to fullscreen
            dashboard.attributes('-fullscreen', True)
            
            # Handle dashboard window close
            dashboard.protocol("WM_DELETE_WINDOW", lambda: self.on_dashboard_close(dashboard))
            
            # Bind ESC and F11 for dashboard too
            dashboard.bind("<Escape>", lambda e: self.toggle_dashboard_fullscreen(dashboard))
            dashboard.bind("<F11>", lambda e: self.toggle_dashboard_fullscreen(dashboard))
            
        except Exception as e:
            print(f"Error opening dashboard: {e}")
            show_message(self, "Error", f"Failed to open dashboard: {str(e)}", "error")
            self.deiconify()
    
    def toggle_dashboard_fullscreen(self, dashboard):
        """Toggle fullscreen for dashboard"""
        try:
            current_state = dashboard.attributes('-fullscreen')
            dashboard.attributes('-fullscreen', not current_state)
            
            if not current_state:
                # Entering fullscreen
                dashboard.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
            else:
                # Exiting fullscreen
                dashboard.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
                dashboard.update_idletasks()
                x = (dashboard.winfo_screenwidth() // 2) - (Config.WINDOW_WIDTH // 2)
                y = (dashboard.winfo_screenheight() // 2) - (Config.WINDOW_HEIGHT // 2)
                dashboard.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}")
        except Exception as e:
            print(f"Error toggling fullscreen: {e}")
    
    def on_dashboard_close(self, dashboard):
        """Handle dashboard window close"""
        try:
            # Logout user
            self.auth_manager.logout()
            print("User logged out successfully")
            
            # Destroy dashboard
            dashboard.destroy()
            
            # Show login window again in fullscreen
            self.deiconify()
            self.attributes('-fullscreen', True)
            self.create_login_ui()
            
        except Exception as e:
            print(f"Error during logout: {e}")
            # Force cleanup
            try:
                dashboard.destroy()
            except:
                pass
            self.deiconify()
            self.attributes('-fullscreen', True)
            self.create_login_ui()
