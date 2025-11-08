"""
Reusable UI components for Car Rental System
"""
import customtkinter as ctk
from typing import Callable, Optional, List
from config import Config

class ModernButton(ctk.CTkButton):
    """Modern styled button"""
    def __init__(self, master, text: str, command: Callable, 
                 color: str = Config.PRIMARY_COLOR, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=color,
            hover_color=Config.SECONDARY_COLOR,
            corner_radius=8,
            height=40,
            font=("Roboto", 14, "bold"),
            **kwargs
        )

class ModernEntry(ctk.CTkEntry):
    """Modern styled entry field"""
    def __init__(self, master, placeholder: str = "", **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            corner_radius=8,
            height=40,
            font=("Roboto", 12),
            **kwargs
        )

class ModernLabel(ctk.CTkLabel):
    """Modern styled label"""
    def __init__(self, master, text: str, size: int = 14, bold: bool = False, **kwargs):
        font_weight = "bold" if bold else "normal"
        super().__init__(
            master,
            text=text,
            font=("Roboto", size, font_weight),
            **kwargs
        )

class ModernFrame(ctk.CTkFrame):
    """Modern styled frame"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=12,
            **kwargs
        )

class Card(ctk.CTkFrame):
    """Card component for displaying information"""
    def __init__(self, master, title: str, value: str, color: str = Config.PRIMARY_COLOR):
        super().__init__(master, corner_radius=12, fg_color=color)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Roboto", 14),
            text_color="white"
        )
        title_label.pack(pady=(20, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Roboto", 32, "bold"),
            text_color="white"
        )
        value_label.pack(pady=(5, 20))

class DataTable(ctk.CTkScrollableFrame):
    """Table component for displaying data"""
    def __init__(self, master, headers: List[str], **kwargs):
        super().__init__(master, **kwargs)
        self.headers = headers
        self.rows = []
        self._create_header()
    
    def _create_header(self):
        """Create table header"""
        header_frame = ctk.CTkFrame(self, fg_color=Config.PRIMARY_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        for i, header in enumerate(self.headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Roboto", 12, "bold"),
                text_color="white"
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
    
    def add_row(self, data: List[str], button_text: Optional[str] = None, 
                button_command: Optional[Callable] = None):
        """Add a row to the table"""
        row_num = len(self.rows) + 1
        
        row_frame = ctk.CTkFrame(self, fg_color="transparent")
        row_frame.grid(row=row_num, column=0, sticky="ew", padx=5, pady=2)
        
        for i, value in enumerate(data):
            label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                font=("Roboto", 11)
            )
            label.grid(row=0, column=i, padx=10, pady=8, sticky="w")
        
        # Add action button if provided
        if button_text and button_command:
            button = ctk.CTkButton(
                row_frame,
                text=button_text,
                command=button_command,
                width=80,
                height=30,
                corner_radius=6
            )
            button.grid(row=0, column=len(data), padx=10, pady=5)
        
        self.rows.append(row_frame)
    
    def clear_rows(self):
        """Clear all rows except header"""
        for row in self.rows:
            row.destroy()
        self.rows = []

class MessageDialog(ctk.CTkToplevel):
    """Custom message dialog"""
    def __init__(self, parent, title: str, message: str, type: str = "info"):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Center window
        self.transient(parent)
        self.grab_set()
        
        # Message frame
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon and message
        icon_map = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️"
        }
        
        icon_label = ctk.CTkLabel(
            frame,
            text=icon_map.get(type, "ℹ️"),
            font=("Roboto", 32)
        )
        icon_label.pack(pady=(10, 5))
        
        message_label = ctk.CTkLabel(
            frame,
            text=message,
            font=("Roboto", 14),
            wraplength=350
        )
        message_label.pack(pady=10)
        
        # OK button
        ok_button = ctk.CTkButton(
            frame,
            text="OK",
            command=self.destroy,
            width=100
        )
        ok_button.pack(pady=10)

def show_message(parent, title: str, message: str, type: str = "info"):
    """Show a message dialog"""
    dialog = MessageDialog(parent, title, message, type)
    dialog.wait_window()

class ConfirmDialog(ctk.CTkToplevel):
    """Custom confirmation dialog"""
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent)
        
        self.result = False
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Center window
        self.transient(parent)
        self.grab_set()
        
        # Message frame
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Message
        message_label = ctk.CTkLabel(
            frame,
            text=message,
            font=("Roboto", 14),
            wraplength=350
        )
        message_label.pack(pady=30)
        
        # Buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            command=self._on_yes,
            width=100,
            fg_color=Config.SUCCESS_COLOR
        )
        yes_button.pack(side="left", padx=10)
        
        no_button = ctk.CTkButton(
            button_frame,
            text="No",
            command=self._on_no,
            width=100,
            fg_color=Config.DANGER_COLOR
        )
        no_button.pack(side="left", padx=10)
    
    def _on_yes(self):
        self.result = True
        self.destroy()
    
    def _on_no(self):
        self.result = False
        self.destroy()

def ask_confirmation(parent, title: str, message: str) -> bool:
    """Show a confirmation dialog"""
    dialog = ConfirmDialog(parent, title, message)
    parent.wait_window(dialog)
    return dialog.result
