import tkinter as tk
from tkinter import ttk


class SidePanel(tk.Frame):

    def __init__(self, parent, on_export, on_clear_history, **kwargs):
        super().__init__(parent, padx=16, pady=16, **kwargs)
        self._on_export        = on_export
        self._on_clear_history = on_clear_history
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._build()

    # ── Construção ────────────────────────────────────────────────────────────

    def _build(self):
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 9))

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self._build_tab_history()
        self._build_text_tab("Explicação",    "explain")
        self._build_text_tab("Complemento 2", "c2")
        self._build_text_tab("Na mão",        "manual")

    def _build_tab_history(self):
        tab = tk.Frame(self.notebook)
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        self.notebook.add(tab, text="  Histórico  ")
        self._tab_hist = tab

        # Caixa de texto + scrollbar
        frame = tk.Frame(tab)
        frame.grid(row=0, column=0, sticky="nsew", pady=(8, 4))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.hist_box = self._make_textbox(frame)
        self.hist_box.grid(row=0, column=0, sticky="nsew")

        sb = tk.Scrollbar(frame, command=self.hist_box.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.hist_box.config(yscrollcommand=sb.set)

        # Linha de botões
        btn_row = tk.Frame(tab)
        btn_row.grid(row=1, column=0, sticky="ew", pady=(4, 8))
        self._btn_row = btn_row

        for label, fmt in [(".txt","txt"), (".csv","csv"),
                            (".json","json"), (".pdf","pdf")]:
            tk.Button(
                btn_row, text=label,
                command=lambda f=fmt: self._on_export(f),
                font=("Helvetica", 9), relief="flat",
                cursor="hand2", pady=4, padx=6,
            ).pack(side="left", padx=(0, 4))

        self._btn_clear = tk.Button(
            btn_row, text="Limpar",
            command=self._on_clear_history,
            font=("Helvetica", 9), relief="flat",
            cursor="hand2", pady=4, padx=6,
        )
        self._btn_clear.pack(side="left", padx=(4, 0))

    def _build_text_tab(self, title: str, attr: str):
        """Cria uma aba genérica com caixa de texto + scrollbar."""
        tab = tk.Frame(self.notebook)
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        self.notebook.add(tab, text=f"  {title}  ")

        box = self._make_textbox(tab)
        box.grid(row=0, column=0, sticky="nsew", pady=(8, 0))

        sb = tk.Scrollbar(tab, command=box.yview)
        sb.grid(row=0, column=1, sticky="ns", pady=(8, 0))
        box.config(yscrollcommand=sb.set)

        # Guarda referência como atributo dinâmico: self.explain_box, self.c2_box, etc.
        setattr(self, f"{attr}_box", box)

    # ── Interface pública ─────────────────────────────────────────────────────

    def set_history(self, lines: list[str]):
        """Substitui o conteúdo do histórico."""
        content = "\n".join(lines) if lines else "Nenhuma conversão ainda."
        self._set_text(self.hist_box, content)

    def set_explanation(self, text: str):
        self._set_text(self.explain_box, text)

    def set_c2(self, text: str):
        self._set_text(self.c2_box, text)

    def set_manual(self, text: str):
        self._set_text(self.manual_box, text)

    def apply_theme(self, theme: dict):
        """Propaga o tema para todas as abas."""
        self.config(bg=theme["bg"])

        for tab in [self._tab_hist]:
            tab.config(bg=theme["bg"])

        self._btn_row.config(bg=theme["bg"])
        for widget in self._btn_row.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(
                    bg=theme["surface"], fg=theme["text"],
                    activebackground=theme["border"],
                    activeforeground=theme["text"],
                )

        for box in [self.hist_box, self.explain_box, self.c2_box, self.manual_box]:
            box.config(bg=theme["surface"], fg=theme["text"])

    # ── Utilitários privados ──────────────────────────────────────────────────

    @staticmethod
    def _make_textbox(parent) -> tk.Text:
        return tk.Text(
            parent, font=("Courier", 8), relief="flat",
            state="disabled", wrap="word",
        )

    @staticmethod
    def _set_text(widget: tk.Text, content: str):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content)
        widget.config(state="disabled")