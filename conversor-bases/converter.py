import base64
import math


# ── Validação ─────────────────────────────────────────────────────────────────

VALID_CHARS = {
    2:  set("01"),
    8:  set("01234567"),
    10: set("0123456789"),
    16: set("0123456789abcdefABCDEF"),
}


def validate_input(value: str, base: int) -> bool:
    """Valida se o valor é compatível com a base informada."""
    v = value.strip()
    if not v:
        return False
    if base in VALID_CHARS:
        return all(c in VALID_CHARS[base] for c in v)
    return True


# ── Conversão principal ───────────────────────────────────────────────────────

def convert(value: str, from_base: int) -> dict:
    """
    Converte um valor de qualquer base para todas as outras.
    Retorna resultados, LEDs, complemento de 2, explicação e guia manual.
    """
    value = value.strip().upper()
    decimal = int(value, from_base)

    # Binário alinhado a múltiplo de 8 bits
    raw_bin = bin(decimal)[2:]
    padded_bin = raw_bin.zfill(max(8, math.ceil(len(raw_bin) / 8) * 8))

    # Base32 e Base64
    num_bytes = max(1, math.ceil(decimal.bit_length() / 8))
    raw_bytes = decimal.to_bytes(num_bytes, byteorder="big")
    b32 = base64.b32encode(raw_bytes).decode().rstrip("=")
    b64 = base64.b64encode(raw_bytes).decode()

    results = {
        "BIN": padded_bin,
        "OCT": oct(decimal)[2:],
        "DEC": str(decimal),
        "HEX": hex(decimal)[2:].upper(),
        "B32": b32,
        "B64": b64,
    }

    # Complemento de 2 (8 bits se <= 255, senão 16)
    bits = 8 if decimal <= 255 else 16
    twos = twos_complement(decimal, bits)

    return {
        "results": results,
        "explanation": build_explanation(value, from_base, decimal, results),
        "manual": build_manual_guide(value, from_base, decimal, results),
        "twos_complement": twos,
        "bits": bits,
        "decimal": decimal,
        "padded_bin": padded_bin,
    }


# ── Complemento de 2 ──────────────────────────────────────────────────────────

def twos_complement(value: int, bits: int = 8) -> dict:
    """Calcula o complemento de 2 e retorna os passos detalhados."""
    if value == 0:
        zero = "0" * bits
        return {
            "result": zero,
            "negative_value": 0,
            "steps": [f"{'Original:':22}{zero}  (= 0)",
                      "O complemento de 2 de 0 é 0."],
            "bits": bits,
        }

    original  = bin(value)[2:].zfill(bits)
    inverted  = "".join("1" if b == "0" else "0" for b in original)
    comp2_int = int(inverted, 2) + 1
    comp2_bin = bin(comp2_int)[2:].zfill(bits)
    neg_value = comp2_int - (2 ** bits)

    steps = [
        f"{'Número original:':22}{original}  (= +{value})",
        f"{'Complemento de 1:':22}{inverted}  (todos os bits invertidos)",
        f"{'Somar 1:':22}{'+ ' + '0' * (bits - 1) + '1'}",
        "─" * (bits + 24),
        f"{'Resultado (C2):':22}{comp2_bin}  (= {neg_value} com sinal)",
    ]

    return {
        "result": comp2_bin,
        "negative_value": neg_value,
        "steps": steps,
        "bits": bits,
    }


# ── Explicação automática ─────────────────────────────────────────────────────

def build_explanation(value: str, from_base: int, decimal: int, results: dict) -> str:
    """Texto explicando como a conversão foi feita."""
    base_names = {2: "Binário", 8: "Octal", 10: "Decimal", 16: "Hexadecimal"}
    origin = base_names.get(from_base, f"Base {from_base}")

    lines = [
        f"Entrada: {value}  ({origin}, base {from_base})",
        "",
        "── Etapa 1: converter para Decimal ──",
    ]

    if from_base == 10:
        lines.append(f"  O valor já é decimal: {decimal}")
    else:
        digits = value[::-1]
        parts = [f"{d}×{from_base}^{i}" for i, d in enumerate(digits)]
        lines.append("  Expansão posicional (da direita para a esquerda):")
        lines.append("  " + " + ".join(reversed(parts)) + f" = {decimal}")

    lines += [
        "",
        "── Etapa 2: decimal → outras bases ──",
        f"  {decimal} → Binário:       {results['BIN']}",
        f"  {decimal} → Octal:         {results['OCT']}",
        f"  {decimal} → Hexadecimal:   {results['HEX']}",
        f"  {decimal} → Base 32:       {results['B32']}",
        f"  {decimal} → Base 64:       {results['B64']}",
        "",
        "Toda conversão passa pelo decimal como etapa intermediária.",
    ]
    return "\n".join(lines)


# ── Guia manual ───────────────────────────────────────────────────────────────

def build_manual_guide(value: str, from_base: int, decimal: int, results: dict) -> str:
    """Guia passo a passo de como fazer as conversões à mão."""
    lines = [
        f"Como converter {value} (base {from_base}) à mão",
        "=" * 45,
        "",
    ]
    lines += _dec_to_bin_manual(decimal)
    lines.append("")
    lines += _dec_to_hex_manual(decimal)
    lines.append("")
    lines += _bin_to_hex_manual(results["BIN"])
    return "\n".join(lines)


def _dec_to_bin_manual(decimal: int) -> list:
    lines = ["── Decimal → Binário (divisões por 2) ──"]
    if decimal == 0:
        lines += ["  0 ÷ 2 = 0  resto 0", "  Resultado: 0"]
        return lines
    n, steps = decimal, []
    while n > 0:
        steps.append((n, n // 2, n % 2))
        n //= 2
    for orig, quot, rem in steps:
        lines.append(f"  {orig:>6} ÷ 2 = {quot:<6} resto {rem}")
    lines.append("  Lendo os restos de baixo para cima: "
                 + "".join(str(s[2]) for s in reversed(steps)))
    return lines


def _dec_to_hex_manual(decimal: int) -> list:
    hd = "0123456789ABCDEF"
    lines = ["── Decimal → Hexadecimal (divisões por 16) ──"]
    if decimal == 0:
        lines += ["  0 ÷ 16 = 0  resto 0  (= 0)", "  Resultado: 0"]
        return lines
    n, steps = decimal, []
    while n > 0:
        r = n % 16
        steps.append((n, n // 16, r, hd[r]))
        n //= 16
    for orig, quot, rem, hc in steps:
        lines.append(f"  {orig:>6} ÷ 16 = {quot:<6} resto {rem:<2} (= {hc})")
    lines.append("  Lendo os restos de baixo para cima: "
                 + "".join(s[3] for s in reversed(steps)))
    return lines


def _bin_to_hex_manual(binary: str) -> list:
    hd = "0123456789ABCDEF"
    lines = ["── Binário → Hexadecimal (grupos de 4 bits) ──"]
    padded = binary.zfill(math.ceil(len(binary) / 4) * 4)
    groups = [padded[i:i+4] for i in range(0, len(padded), 4)]
    result = []
    for g in groups:
        v = int(g, 2)
        c = hd[v]
        lines.append(f"  {g}  →  {v:>2} decimal  →  {c}")
        result.append(c)
    lines.append(f"  Resultado: {''.join(result)}")
    return lines


# ── Exportar histórico ────────────────────────────────────────────────────────

def export_history(history: list, filepath: str, fmt: str = "txt") -> bool:
    """
    Exporta o histórico para .txt, .csv, .json ou .pdf.
    'history' deve ser uma lista de dicts com as chaves:
        entrada, base, BIN, OCT, DEC, HEX, B32, B64
    Retorna True se salvo com sucesso.
    """
    try:
        if fmt == "csv":
            _export_csv(history, filepath)
        elif fmt == "json":
            _export_json(history, filepath)
        elif fmt == "pdf":
            _export_pdf(history, filepath)
        else:
            _export_txt(history, filepath)
        return True
    except Exception as e:
        print(f"[export_history] erro: {e}")
        return False


def _export_txt(history: list, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Histórico de Conversões\n")
        f.write("=" * 60 + "\n\n")
        for i, row in enumerate(history, 1):
            f.write(f"{i:>3}. Entrada: {row['entrada']} (base {row['base']})\n")
            f.write(f"     BIN: {row['BIN']}  OCT: {row['OCT']}  "
                    f"DEC: {row['DEC']}  HEX: {row['HEX']}\n")
            f.write(f"     B32: {row['B32']}  B64: {row['B64']}\n\n")


def _export_csv(history: list, filepath: str):
    import csv
    campos = ["entrada", "base", "BIN", "OCT", "DEC", "HEX", "B32", "B64"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(history)


def _export_json(history: list, filepath: str):
    import json
    import datetime
    payload = {
        "titulo":   "Histórico de Conversões",
        "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
        "total":    len(history),
        "conversoes": history,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _export_pdf(history: list, filepath: str):
    """PDF formatado com tabela, título, cabeçalho e rodapé usando reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                    Paragraph, Spacer)
    from reportlab.lib.enums import TA_CENTER
    import datetime

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
    )

    styles = getSampleStyleSheet()
    cor_header  = colors.HexColor("#1E3A8A")
    cor_linha_a = colors.HexColor("#EFF6FF")
    cor_linha_b = colors.white

    # Estilo do título
    titulo_style = ParagraphStyle(
        "titulo",
        parent=styles["Title"],
        fontSize=16,
        textColor=cor_header,
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    sub_style = ParagraphStyle(
        "sub",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=16,
        alignment=TA_CENTER,
    )

    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos = [
        Paragraph("Conversor de Bases Numéricas", titulo_style),
        Paragraph(f"Histórico de conversões  ·  Gerado em {agora}", sub_style),
    ]

    # Cabeçalho da tabela
    cabecalho = ["#", "Entrada", "Base", "BIN", "OCT", "DEC", "HEX", "B32", "B64"]
    dados = [cabecalho]

    for i, row in enumerate(history, 1):
        dados.append([
            str(i),
            row.get("entrada", ""),
            str(row.get("base", "")),
            row.get("BIN", ""),
            row.get("OCT", ""),
            row.get("DEC", ""),
            row.get("HEX", ""),
            row.get("B32", ""),
            row.get("B64", ""),
        ])

    # Larguras das colunas (total ~17cm na A4 com margens 2cm)
    col_widths = [1*cm, 2*cm, 1.5*cm, 2.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 2*cm, 2.3*cm]

    tabela = Table(dados, colWidths=col_widths, repeatRows=1)

    # Estilo da tabela
    estilo = TableStyle([
        # Cabeçalho
        ("BACKGROUND",    (0, 0), (-1, 0),  cor_header),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  8),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  6),
        ("TOPPADDING",    (0, 0), (-1, 0),  6),
        # Dados
        ("FONTNAME",      (0, 1), (-1, -1), "Courier"),
        ("FONTSIZE",      (0, 1), (-1, -1), 7),
        ("ALIGN",         (0, 1), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        # Grid
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [cor_linha_a, cor_linha_b]),
    ])
    tabela.setStyle(estilo)

    elementos.append(tabela)
    elementos.append(Spacer(1, 0.5*cm))

    # Rodapé como parágrafo (reportlab SimpleDocTemplate não tem rodapé nativo fácil)
    rodape_style = ParagraphStyle(
        "rodape",
        parent=styles["Normal"],
        fontSize=7,
        textColor=colors.HexColor("#9CA3AF"),
        alignment=TA_CENTER,
    )
    elementos.append(
        Paragraph(
            f"Total de conversões: {len(history)}  ·  "
            "Gerado por Conversor de Bases Numéricas",
            rodape_style,
        )
    )

    doc.build(elementos)