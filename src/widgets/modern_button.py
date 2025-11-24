"""
Modern Button Widget - Premium Edition
Enhanced button dengan elevation dan glow effect
"""

import tkinter as tk
from src.config import COLORS, SPACING, FONTS


class ModernButton(tk.Button):
    """Premium button dengan hover effect dan elevation"""
    
    def __init__(self, master, text, icon, command, 
                 color=COLORS["button_bg"], 
                 hover_color=COLORS["accent_hover"], 
                 **kwargs):
        super().__init__(master, **kwargs)
        self.color = color
        self.hover_color = hover_color
        self.command = command
        
        self.config(
            text=f" {icon}  {text}",
            font=(FONTS["family"], 11, FONTS["weight_bold"]),
            bg=self.color,
            fg=COLORS["text_primary"],
            activebackground=self.hover_color,
            activeforeground=COLORS["text_primary"],
            relief="flat",
            bd=0,
            padx=SPACING["lg"],
            pady=12,
            cursor="hand2",
            anchor="w",
            command=self.on_click
        )
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        """Mouse hover - add glow effect"""
        if self['state'] != 'disabled':
            self.config(bg=self.hover_color)
            
    def on_leave(self, e):
        """Mouse leave"""
        if self['state'] != 'disabled':
            self.config(bg=self.color)

    def on_click(self):
        """Button clicked"""
        if self.command:
            self.command()


class PremiumButton(tk.Button):
    """Large premium button untuk primary actions"""
    
    def __init__(self, master, text, icon, command, 
                 bg_color=COLORS["success"], 
                 **kwargs):
        super().__init__(master, **kwargs)
        self.bg_color = bg_color
        self.hover_color = COLORS["success_glow"] if bg_color == COLORS["success"] else COLORS["accent_hover"]
        
        self.config(
            text=f"{icon}  {text}",
            font=(FONTS["family"], 14, FONTS["weight_bold"]),
            bg=self.bg_color,
            fg=COLORS["text_primary"],
            activebackground=self.hover_color,
            activeforeground=COLORS["text_primary"],
            relief="raised",
            bd=2,
            padx=SPACING["xl"],
            pady=SPACING["md"],
            cursor="hand2",
            command=command
        )
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        if self['state'] != 'disabled':
            self.config(bg=self.hover_color, relief="raised")
    
    def on_leave(self, e):
        if self['state'] != 'disabled':
            self.config(bg=self.bg_color, relief="raised")
