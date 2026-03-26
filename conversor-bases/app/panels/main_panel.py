import tkinter as tk
from tkinter import ttk

from app.themes import BASE_OPTIONS, BASE_MAP
from app.widgets.led_canvas import LedCanvas
from app.widgets.result_cards import ResultCards


class MainPanel(tk.Frame):

    def __init__(self, parent, on_convert, **kwargs):
        super().__init__(parent, padx=20, pady=16, **kwargs)
        self._on_convert = on_convert
        self.columnconfigure(0, weight=1)
        self._build()

    # ── Construção ────────────────────────────────────────────────────────────

    def _build(self):
        self._build_base_selector()
        self._build_entry()
        self._build_convert_button()
        self._build_leds()
        self._build_result_cards()

    def _build_base_selector(self):
        tk.Label(self, text="Base de entrada", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        self.base_var = tk.StringVar(value=BASE_OPTIONS[2])  # Decimal padrão
        self.combo = ttk.Combobox(
            self, textvariable=self.base_var,
            values=BASE_OPTIONS, state="readonly",
            font=("Helvetica", 11), width=22,
        )
        self.combo.grid(row=1, column=0, sticky="w", pady=(0, 14))

    def _build_entry(self):
        tk.Label(self, text="Valor", font=("Helvetica", 10)).grid(
            row=2, column=0, sticky="w", pady=(0, 4)
        )
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=3, column=0, sticky="ew", pady=(0, 4))
        entry_frame.columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            entry_frame, textvariable=self.entry_var,
            font=("Courier", 14), relief="flat",
            bd=0, highlightthickness=1,
        )
        self.entry.grid(row=0, column=0, sticky="ew", ipady=8, padx=1)
        self.entry.bind("<Return>",    lambda e: self._trigger_convert())
        self.entry.bind("<KeyRelease>", lambda e: self._clear_error())

        self.lbl_error = tk.Label(self, text="", font=("Helvetica", 9))
        self.lbl_error.grid(row=4, column=0, sticky="w", pady=(0, 10))

    def _build_convert_button(self):
        self.btn_convert = tk.Button(
            self, text="Converter  →",
            command=self._trigger_convert,
            font=("Helvetica", 12, "bold"), relief="flat",
            cursor="hand2", padx=20, pady=10,
        )
        self.btn_convert.grid(row=5, column=0, sticky="w", pady=(0, 16))

    def _build_leds(self):
        tk.Label(self, text="Representação em bits", font=("Helvetica", 10)).grid(
            row=6, column=0, sticky="w", pady=(0, 6)
        )
        self.leds = LedCanvas(self)
        self.leds.grid(row=7, column=0, sticky="ew", pady=(0, 16))

    def _build_result_cards(self):
        tk.Label(self, text="Resultados", font=("Helvetica", 10)).grid(
            row=8, column=0, sticky="w", pady=(0, 8)
        )
        self.cards = ResultCards(self)
        self.cards.grid(row=9, column=0, sticky="ew")

    # ── Interface pública ─────────────────────────────────────────────────────

    def show_error(self, msg: str, color: str):
        """Exibe uma mensagem de erro abaixo do campo de entrada."""
        self.lbl_error.config(text=msg, fg=color)

    def get_value(self) -> str:
        return self.entry_var.get().strip()

    def get_base(self) -> int:
        return BASE_MAP[self.base_var.get()]

    def update_results(self, results: dict, binary: str):
        """Atualiza cards e LEDs com os resultados da conversão."""
        self.cards.update_values(results)
        self.leds.update_bits(binary)

    def apply_theme(self, theme: dict):
        """Propaga o tema para todos os sub-widgets."""
        self.config(bg=theme["bg"])
        self.leds.apply_theme(theme)
        self.cards.apply_theme(theme)

        self.entry.config(
            bg=theme["entry_bg"], fg=theme["entry_fg"],
            insertbackground=theme["text"],
            highlightbackground=theme["border"],
            highlightcolor=theme["accent"],
        )
        self.btn_convert.config(
            bg=theme["accent"],  fg=theme["accent_fg"],
            activebackground=theme["accent"],
            activeforeground=theme["accent_fg"],
        )
        # Labels de seção
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=theme["bg"], fg=theme["text_muted"])

    # ── Privado ───────────────────────────────────────────────────────────────

    def _trigger_convert(self):
        self._clear_error()
        self._on_convert(self.get_value(), self.get_base())

    def _clear_error(self):
        self.lbl_error.config(text="")