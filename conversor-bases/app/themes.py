# ── Temas de cor ──────────────────────────────────────────────────────────────

THEMES = {
    "light": {
        "bg":         "#F5F5F0",
        "surface":    "#FFFFFF",
        "border":     "#DDDDD8",
        "text":       "#1A1A18",
        "text_muted": "#6B6B65",
        "accent":     "#2563EB",
        "accent_fg":  "#FFFFFF",
        "result_bg":  "#EFF6FF",
        "result_fg":  "#1E3A8A",
        "hist_bg":    "#FAFAF8",
        "entry_bg":   "#FFFFFF",
        "entry_fg":   "#1A1A18",
        "error":      "#DC2626",
        "led_on":     "#22C55E",
        "led_off":    "#D1D5DB",
        "led_border": "#9CA3AF",
    },
    "dark": {
        "bg":         "#1A1A1E",
        "surface":    "#25252B",
        "border":     "#3A3A42",
        "text":       "#E8E8E0",
        "text_muted": "#8A8A80",
        "accent":     "#3B82F6",
        "accent_fg":  "#FFFFFF",
        "result_bg":  "#1E2D45",
        "result_fg":  "#93C5FD",
        "hist_bg":    "#1E1E24",
        "entry_bg":   "#2E2E36",
        "entry_fg":   "#E8E8E0",
        "error":      "#F87171",
        "led_on":     "#4ADE80",
        "led_off":    "#374151",
        "led_border": "#6B7280",
    },
}

# ── Bases numéricas ───────────────────────────────────────────────────────────

BASE_OPTIONS = ["Binário (2)", "Octal (8)", "Decimal (10)", "Hexadecimal (16)"]

BASE_MAP = {
    "Binário (2)":     2,
    "Octal (8)":       8,
    "Decimal (10)":   10,
    "Hexadecimal (16)": 16,
}

BASE_KEYS = {2: "BIN", 8: "OCT", 10: "DEC", 16: "HEX"}

# ── LEDs ──────────────────────────────────────────────────────────────────────

LED_SIZE  = 14   # diâmetro do círculo em pixels
LED_GAP   = 3    # espaço entre LEDs
GROUP_GAP = 8    # espaço extra a cada 4 bits