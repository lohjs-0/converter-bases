import tkinter as tk


class Header(tk.Frame):
    
    def __init__(self, parent, on_theme_toggle, **kwargs):
        super().__init__(parent, pady=12, padx=20, **kwargs)
        self._on_theme_toggle = on_theme_toggle
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)

        self.lbl_title = tk.Label(
            self, text="Conversor de Bases",
            font=("Helvetica", 18, "bold"),
        )
        self.lbl_title.grid(row=0, column=0, sticky="w")

        self.lbl_sub = tk.Label(
            self,
            text="Binário · Octal · Decimal · Hex · Base32 · Base64",
            font=("Helvetica", 10),
        )
        self.lbl_sub.grid(row=1, column=0, sticky="w")

        self.btn_theme = tk.Button(
            self, text="🌙  Modo Escuro",
            command=self._on_theme_toggle,
            relief="flat", font=("Helvetica", 10),
            cursor="hand2", padx=12, pady=6,
        )
        self.btn_theme.grid(row=0, column=1, rowspan=2, sticky="e")

    def set_theme_label(self, dark: bool):
        """Atualiza o texto do botão conforme o tema ativo."""
        label = "☀  Modo Claro" if dark else "🌙  Modo Escuro"
        self.btn_theme.config(text=label)

    def apply_theme(self, theme: dict):
        """Aplica cores do tema ao header."""
        self.config(bg=theme["bg"])
        self.lbl_title.config(bg=theme["bg"], fg=theme["text"])
        self.lbl_sub.config(bg=theme["bg"],   fg=theme["text_muted"])
        self.btn_theme.config(
            bg=theme["surface"], fg=theme["text"],
            activebackground=theme["border"],
            activeforeground=theme["text"],
        )