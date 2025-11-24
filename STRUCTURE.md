# ByteShield - Project Structure

## 📁 Folder Structure

```
ByteShield/
├── src/                          # Source code
│   ├── __init__.py
│   ├── main.py                   # Entry point
│   ├── app.py                    # Main application class
│   ├── config.py                 # Constants & colors
│   │
│   ├── widgets/                  # Custom widgets
│   │   ├── __init__.py
│   │   ├── modern_button.py      # ModernButton dengan hover
│   │   └── sidebar.py            # Sidebar component
│   │
│   ├── views/                    # UI views
│   │   ├── __init__.py
│   │   ├── home_view.py          # Welcome screen
│   │   ├── clean_view.py         # Clean junk page
│   │   ├── scan_view.py          # Virus scan page
│   │   ├── optimize_view.py      # Full optimization page
│   │   ├── sysinfo_view.py       # System info page
│   │   └── terminal_view.py      # Terminal output
│   │
│   └── core/                     # Business logic
│       ├── __init__.py
│       ├── cleaner.py            # File cleaning
│       ├── scanner.py            # Windows Defender integration
│       └── system_info.py        # System info gathering
│
├── byteshield_gui.py             # Backward compat wrapper
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── .gitignore
```

## 🔧 How It Works

### Entry Points

**Option 1: Direct (Recommended)**
```bash
python src/main.py
```

**Option 2: Backward Compatible**
```bash
python byteshield_gui.py
```

Both methods run the same modular code!

### Module Hierarchy

```
byteshield_gui.py
  ↓
src/main.py
  ↓
src/app.py (ByteShieldApp)
  ↓
  ├── src/config.py (COLORS)
  ├── src/widgets/sidebar.py
  ├── src/widgets/modern_button.py
  ├── src/views/*.py (all views)
  └── src/core/*.py (cleaner, scanner, system_info)
```

## 📦 PyInstaller Build

Build command tetap sama:
```bash
pyinstaller --onefile --noconsole --name ByteShield byteshield_gui.py
```

PyInstaller akan auto-include semua module dari `src/`.

## 🎯 Benefits of Modular Structure

✅ **Maintainability**: File kecil & focused (~50-150 lines each)
✅ **Testability**: Can test individual modules
✅ **Scalability**: Easy to add new features/views
✅ **Collaboration**: Multiple devs can work on different files
✅ **Reusability**: Widgets & core logic can be reused
✅ **Clean Code**: Separation of concerns (UI vs Logic)

## 📝 Adding New Features

### Add New View

1. Create `src/views/new_view.py`:
```python
def create_new_view(parent, callback):
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    # ... your UI code ...
    return view
```

2. Import dalam `src/app.py`:
```python
from src.views.new_view import create_new_view
```

3. Add to sidebar callbacks & create instance

### Add New Core Function

1. Create function in appropriate module:
   - File operations → `src/core/cleaner.py`
   - Scanning → `src/core/scanner.py`
   - System info → `src/core/system_info.py`

2. Import dalam `src/app.py` dan gunakan

## 🧪 Testing Individual Modules

```python
# Test cleaner module
python -c "from src.core.cleaner import clean_junk; clean_junk()"

# Test system info
python -c "from src.core.system_info import get_system_info; print(get_system_info())"
```

## 📊 File Breakdown

| File | Lines | Purpose |
|------|-------|---------|
| `src/config.py` | 25 | Colors & constants |
| `src/widgets/modern_button.py` | 55 | Custom button widget |
| `src/widgets/sidebar.py` | 100 | Sidebar component |
| `src/core/cleaner.py` | 90 | Cleaning logic |
| `src/core/scanner.py` | 95 | Defender integration |
| `src/core/system_info.py` | 70 | System info gathering |
| `src/views/home_view.py` | 30 | Home screen |
| `src/views/terminal_view.py` | 70 | Terminal view |
| `src/views/clean_view.py` | 75 | Clean page |
| `src/views/scan_view.py` | 75 | Scan page |
| `src/views/optimize_view.py` | 85 | Optimize page |
| `src/views/sysinfo_view.py` | 75 | System info page |
| `src/app.py` | 240 | Main app class |
| `src/main.py` | 15 | Entry point |
| **Total** | **~1100** | Much more maintainable! |

---

**Created with ❤️ by Hafis**
