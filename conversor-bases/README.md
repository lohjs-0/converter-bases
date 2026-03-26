# 🔢 Conversor de Bases Numéricas

Aplicação desktop para converter números entre múltiplas bases numéricas, com interface gráfica em Python + Tkinter.

## Funcionalidades

- ✅ Conversão entre todas as bases: BIN · OCT · DEC · HEX · Base32 · Base64
- 💡 LEDs visuais mostrando cada bit do número
- 🔁 Complemento de 2 com passo a passo
- 📖 Aba "Na mão" — aprenda a fazer a conversão sem computador
- 📜 Histórico das conversões realizadas
- 💾 Exportar histórico como `.txt` ou `.csv`
- 🌙 Modo escuro / claro alternável

## Como executar

### Pré-requisitos

- Python 3.8 ou superior
- Tkinter (já incluso na instalação padrão do Python)

### Rodando o projeto

```bash
git clone https://github.com/seu-usuario/conversor-bases.git
cd conversor-bases
python main.py
```

## Estrutura do projeto

```
conversor-bases/
├── main.py        # Interface gráfica (Tkinter)
├── converter.py   # Lógica de conversão (separada da UI)
└── README.md
```

## Como funciona a conversão

Toda conversão passa pelo **decimal** como etapa intermediária:

```
Valor de origem → Decimal → Base de destino
```

**Exemplo:** `1A` (hex) → binário:
1. `1A` hex = `26` decimal
2. `26` decimal = `11010` binário

## Complemento de 2

Usado para representar números negativos em sistemas digitais:

```
+5  =  0000 0101
       ─────────
C1  =  1111 1010  (inverte todos os bits)
    +          1
       ─────────
C2  =  1111 1011  (= -5 com sinal)
```

## Tecnologias

- **Python 3** — linguagem principal
- **Tkinter** — interface gráfica (stdlib, sem dependências externas)
- **base64** — módulo stdlib para Base32/Base64

## Licença

MIT — fique à vontade para usar e modificar.