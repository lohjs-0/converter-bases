import tkinter as tk
from app.themes import LED_SIZE, LED_GAP, GROUP_GAP


class LedCanvas(tk.Canvas):
    """
    Canvas que desenha LEDs representando bits de um número binário.

    Uso:
        leds = LedCanvas(parent)
        leds.pack(fill="x")
        leds.update_bits("11001010")
        leds.apply_theme(theme_dict)
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=30, bd=0, highlightthickness=0, **kwargs)
        self._theme = {}

    def update_bits(self, binary: str):
        """Redesenha os LEDs para o valor binário informado."""
        self.delete("all")

        for i, bit in enumerate(binary):
            x = self._x_position(i)
            color = self._theme.get("led_on", "#22C55E") if bit == "1" \
                else self._theme.get("led_off", "#D1D5DB")
            border = self._theme.get("led_border", "#9CA3AF")

            self.create_oval(
                x, 4, x + LED_SIZE, 4 + LED_SIZE,
                fill=color, outline=border, width=1,
            )

    def apply_theme(self, theme: dict):
        """Atualiza as cores do tema e redesenha se já houver bits."""
        self._theme = theme
        self.config(bg=theme.get("bg", "#F5F5F0"))

    def clear(self):
        """Remove todos os LEDs."""
        self.delete("all")

    # ── Utilitário privado ────────────────────────────────────────────────────

    @staticmethod
    def _x_position(index: int) -> int:
        """Calcula a posição X de um LED, com espaço extra a cada 4 bits."""
        group_offset = (index // 4) * GROUP_GAP
        return index * (LED_SIZE + LED_GAP) + group_offset