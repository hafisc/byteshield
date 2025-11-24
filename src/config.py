"""
ByteShield Configuration
Premium color scheme, spacing, dan typography system
"""

# ===== PREMIUM COLOR PALETTE =====
COLORS = {
    # Backgrounds
    "bg_dark": "#0A0E27",           # Deep navy - main background
    "bg_elevated": "#12172E",       # Slightly elevated surfaces
    "sidebar": "#161B33",           # Sidebar background
    "card_bg": "#1A2039",           # Card background
    
    # Accents & Highlights
    "accent": "#00D9FF",            # Bright cyan - primary actions
    "accent_hover": "#00B8DD",      # Hover state
    "accent_light": "#33E3FF",      # Light variant
    "accent_glow": "#0066FF",       # Glow/shadow color
    
    # Status Colors
    "success": "#00FF9D",           # Bright mint green
    "success_glow": "#00CC7E",      # Success shadow
    "danger": "#FF4D6D",            # Coral red
    "danger_glow": "#CC3E57",       # Danger shadow
    "warning": "#FFD93D",           # Golden yellow
    "info": "#6C9EFF",              # Soft blue
    
    # Text
    "text_primary": "#FFFFFF",      # Pure white
    "text_secondary": "#A0AEC0",    # Cool gray
    "text_tertiary": "#718096",     # Muted gray
    "text_disabled": "#4A5568",     # Very muted
    
    # Special
    "terminal_bg": "#050811",       # Almost black for terminal
    "border": "#2D3748",            # Subtle borders
    "divider": "#1F2937",           # Divider lines
    "button_bg": "#1E3A5F",         # Default button bg
}

# ===== SPACING SYSTEM =====
SPACING = {
    "xs": 5,
    "sm": 10,
    "md": 15,
    "lg": 20,
    "xl": 30,
    "xxl": 40
}

# ===== TYPOGRAPHY =====
FONTS = {
    "family": "Segoe UI",
    "family_mono": "Consolas",
    
    # Sizes
    "size_hero": 28,        # Page titles
    "size_h1": 24,          # Main headings
    "size_h2": 18,          # Section headings
    "size_h3": 14,          # Subsection headings
    "size_body": 11,        # Body text
    "size_small": 9,        # Small text
    "size_tiny": 8,         # Tiny text
    
    # Weights
    "weight_bold": "bold",
    "weight_semibold": "normal",  # Tkinter doesn't have semibold, fake with bold
    "weight_normal": "normal"
}

# ===== BORDER RADIUS (simulated with relief) =====
BORDER = {
    "radius_sm": "groove",      # Small rounded effect
    "radius_md": "ridge",       # Medium rounded effect
    "radius_lg": "raised",      # Large rounded effect
    "flat": "flat",             # No border
    "solid": "solid"            # Solid border
}

# ===== APPLICATION INFO =====
APP_NAME = "ByteShield"
APP_VERSION = "2.0"
APP_AUTHOR = "Hafis"
APP_TITLE = f"{APP_NAME} // System Optimizer"
APP_SUBTITLE = "Premium Edition"
