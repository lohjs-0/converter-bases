import tkinter as tk
from tkinter import messagebox, filedialog

from converter import validate_input, convert, export_history
from app.themes import THEMES, BASE_KEYS
from app.panels.header import Header
from app.panels.main_panel import MainPanel
from app.panels.side_panel import SidePanel


class ConversorApp:
    """
    Orquestrador principal da aplicação.
    Conecta converter.py <-> MainPanel <-> SidePanel <-> Header.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Conversor de Bases Numéricas")
        self.root.resizable(True, True)
        self.root.minsize(860, 600)

        self._dark_mode = False
        self._history: list[dict] = []

        self._build_layout()
        self._apply_theme()

    # -- Layout ---------------------------------------------------------------

    def _build_layout(self):
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=1)

        self.header = Header(
            self.root,
            on_theme_toggle=self._toggle_theme,
        )
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.main_panel = MainPanel(
            self.root,
            on_convert=self._handle_convert,
        )
        self.main_panel.grid(row=1, column=0, sticky="nsew")

        self.side_panel = SidePanel(
            self.root,
            on_export=self._handle_export,
            on_clear_history=self._handle_clear_history,
        )
        self.side_panel.grid(row=1, column=1, sticky="nsew")

    # -- Callbacks ------------------------------------------------------------

    def _handle_convert(self, value: str, base: int):
        t = self._current_theme()

        if not value:
            self.main_panel.show_error("Digite um valor para converter.", t["error"])
            return
        if not validate_input(value, base):
            self.main_panel.show_error(f"Valor inválido para base {base}.", t["error"])
            return

        self.main_panel.show_error("", t["error"])

        data = convert(value.upper(), base)
        r    = data["results"]

        self.main_panel.update_results(r, data["padded_bin"])

        row = {
            "entrada": value.upper(), "base": base,
            "BIN": r["BIN"], "OCT": r["OCT"],
            "DEC": r["DEC"], "HEX": r["HEX"],
            "B32": r["B32"], "B64": r["B64"],
        }
        self._history.insert(0, row)
        self._refresh_history()

        self.side_panel.set_explanation(data["explanation"])
        self.side_panel.set_manual(data["manual"])

        c2 = data["twos_complement"]
        c2_text = (
            f"Complemento de 2  ({data['bits']} bits)\n"
            + "=" * 40 + "\n\n"
            + "\n".join(c2["steps"])
        )
        self.side_panel.set_c2(c2_text)

    def _handle_export(self, fmt: str):
        if not self._history:
            messagebox.showinfo("Histórico vazio", "Faça ao menos uma conversão antes de exportar.")
            return

        if fmt == "pdf":
            try:
                import reportlab
            except ImportError:
                messagebox.showerror(
                    "reportlab não instalado",
                    "Para exportar PDF instale o reportlab:\n\n  pip install reportlab"
                )
                return

        path = filedialog.asksaveasfilename(
            defaultextension=f".{fmt}",
            filetypes=[(f"Arquivo {fmt.upper()}", f"*.{fmt}"),
                       ("Todos os arquivos", "*.*")],
            title="Salvar histórico",
        )
        if not path:
            return

        ok = export_history(self._history, path, fmt)
        if ok:
            messagebox.showinfo("Exportado!", f"Histórico salvo em:\n{path}")
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o arquivo.")

    def _handle_clear_history(self):
        self._history.clear()
        self._refresh_history()

    # -- Histórico ------------------------------------------------------------

    def _refresh_history(self):
        lines = [
            f"{r['entrada']} (base {r['base']})  "
            f"BIN:{r['BIN']}  OCT:{r['OCT']}  DEC:{r['DEC']}  HEX:{r['HEX']}"
            for r in self._history
        ]
        self.side_panel.set_history(lines)

    # -- Tema -----------------------------------------------------------------

    def _toggle_theme(self):
        self._dark_mode = not self._dark_mode
        self.header.set_theme_label(self._dark_mode)
        self._apply_theme()

    def _apply_theme(self):
        t = self._current_theme()
        self.root.config(bg=t["bg"])
        self.header.apply_theme(t)
        self.main_panel.apply_theme(t)
        self.side_panel.apply_theme(t)

    def _current_theme(self) -> dict:
        return THEMES["dark"] if self._dark_mode else THEMES["light"]


# -- Entry point --------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorApp(root)
    root.mainloop()
