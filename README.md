# 🔢 Number Base Converter

A desktop application to convert numbers between multiple bases, built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- ✅ Convert between all bases: **Binary · Octal · Decimal · Hex · Base32 · Base64**
- 💡 Visual **bit LED display** — each bit shown as a colored circle
- 🔁 **Two's complement** with step-by-step explanation
- 📖 **"Do it by hand"** tab — learn how to convert without a computer
- 📜 **Conversion history** panel
- 💾 Export history as `.txt`, `.csv`, `.json` or `.pdf`
- 🌙 **Dark / light mode** toggle
- 🗂️ Modular codebase — clean separation between logic and UI

---

## Screenshots

> _Add screenshots here after running the app_

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Tkinter (included in the standard Python installation)
- `reportlab` — only required for PDF export

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/conversor-bases.git

# Enter the project folder
cd conversor-bases

# (Optional) Install reportlab for PDF export
pip install reportlab
```

### Running

```bash
python main.py
```

---

## Project Structure

```
conversor-bases/
├── main.py                  # Entry point — orchestrates all panels
├── converter.py             # Pure conversion logic (no UI)
└── app/
    ├── themes.py            # Color themes and constants
    ├── panels/
    │   ├── header.py        # Top bar with title and theme toggle
    │   ├── main_panel.py    # Input field, LEDs and result cards
    │   └── side_panel.py    # Tabs: history, explanation, C2, manual
    └── widgets/
        ├── led_canvas.py    # Reusable LED bit display widget
        └── result_cards.py  # Reusable result cards grid
```

---

## How Conversion Works

Every conversion uses **decimal as an intermediate step**:

```
Input (any base) → Decimal → Target base
```

**Example:** converting `1A` (hex) to binary:
1. `1A` hex → `26` decimal
2. `26` decimal → `11010` binary

---

## Two's Complement

Used to represent negative numbers in digital systems:

```
+5  →  0000 0101   (original)
       0000 0101
       ---------
C1  →  1111 1010   (invert all bits)
    +          1
       ---------
C2  →  1111 1011   (= -5 with sign)
```

---

## Test Values

| Input | Base | BIN | OCT | DEC | HEX |
|-------|------|-----|-----|-----|-----|
| `255` | Decimal | `11111111` | `377` | `255` | `FF` |
| `1010` | Binary | `1010` | `12` | `10` | `A` |
| `FF` | Hexadecimal | `11111111` | `377` | `255` | `FF` |
| `17` | Octal | `1111` | `17` | `15` | `F` |

---

## Technologies

| Tool | Purpose |
|------|---------|
| **Python 3** | Main language |
| **Tkinter** | GUI (stdlib, no extra dependencies) |
| **base64** | Base32 / Base64 encoding (stdlib) |
| **reportlab** | PDF export (optional) |
