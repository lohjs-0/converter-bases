import tkinter as tk


CARD_DEFINITIONS = [
    ("BIN", "Binário"),
    ("OCT", "Octal"),
    ("DEC", "Decimal"),
    ("HEX", "Hex"),
    ("B32", "Base 32"),
    ("B64", "Base 64"),
]

COLUMNS = 3   # cards por linha


class ResultCards(tk.Frame):
    """
    Grade de cards exibindo resultados de conversão.

    Uso:
        cards = ResultCards(parent)
        cards.grid(...)
        cards.update({"BIN": "11111111", "OCT": "377", ...})
        cards.apply_theme(theme_dict)
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._cards: dict[str, tuple] = {}   # key → (frame, lbl_name, lbl_val)
        self._build()

    def _build(self):
        for i, (key, label) in enumerate(CARD_DEFINITIONS):
            row, col = divmod(i, COLUMNS)
            self.columnconfigure(col, weight=1)

            card = tk.Frame(self, padx=10, pady=8)
            card.grid(row=row, column=col, padx=(0, 8), pady=(0, 8), sticky="ew")

            lbl_name = tk.Label(card, text=label, font=("Helvetica", 9))
            lbl_name.pack(anchor="w")

            lbl_val = tk.Label(card, text="—", font=("Courier", 11, "bold"))
            lbl_val.pack(anchor="w", pady=(4, 0))

            self._cards[key] = (card, lbl_name, lbl_val)

    def update_values(self, results: dict):
        """Atualiza os valores exibidos nos cards."""
        for key, (_card, _name, lbl_val) in self._cards.items():
            lbl_val.config(text=results.get(key, "—"))

    def reset(self):
        """Volta todos os cards para '—'."""
        for _key, (_card, _name, lbl_val) in self._cards.items():
            lbl_val.config(text="—")

    def apply_theme(self, theme: dict):
        """Aplica as cores do tema a todos os cards."""
        self.config(bg=theme["bg"])
        for _key, (card, lbl_name, lbl_val) in self._cards.items():
            card.config(bg=theme["result_bg"])
            lbl_name.config(bg=theme["result_bg"], fg=theme["text_muted"])
            lbl_val.config(bg=theme["result_bg"],  fg=theme["result_fg"])