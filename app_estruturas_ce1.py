import io
import streamlit as st
from PIL import Image

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────
PDF_PATH = "DIS-NOR-013-REV-08.pdf"   # << ajuste o caminho se necessário
DPI = 200                              # resolução da rasterização

# Proporção do cabeçalho a cortar (logotipo + cabeçalho da norma)
CROP_TOP_RATIO = 0.13   # remove os primeiros 13% da altura (cabeçalho)


# ─────────────────────────────────────────────
# BANCO DE DADOS DAS ESTRUTURAS
# ─────────────────────────────────────────────
# Cada estrutura define:
#   pagina_desenho  : página PDF onde está o desenho (1-based)
#   crop_top_ratio  : quanto cortar do topo (para remover cabeçalho)
#   crop_bottom_ratio: quanto cortar de baixo (0 = não corta)
#   titulo          : nome completo
#   subtitulo       : descrição de uso
#   materiais       : lista de dicts com Item, Descricao, Circular, DT, Variavel
#                     Use "-" para ausente, "Poste" / "Cabo" etc. para variável
#   notas           : lista de strings com as notas da estrutura

ESTRUTURAS = {

    "CE1": {
        "pagina_desenho": 43,           # página 43 do PDF = desenho CE1 Poste Circular + DT + vista frontal
        "crop_top_ratio": 0.13,
        "crop_bottom_ratio": 0.0,
        "titulo": "Estrutura 1 – CE1",
        "subtitulo": "Utilizada em tangente e em ângulo máximo de deflexão de 6°.",
        "materiais": [
            # Materiais comuns (aparecem nos dois tipos de poste)
            {
                "item": "feb",
                "descricao": "ARRUELA LIS QUAD SAE1020 M18",
                "und": "un",
                "circular": "2",
                "dt": "2",
                "variavel": "-",
            },
            {
                "item": "ff",
                "descricao": "CINTA DE AÇO CARBONO",
                "und": "un",
                "circular": "2",
                "dt": "-",
                "variavel": "Poste",
            },
            {
                "item": "fu1",
                "descricao": "PARAFUSO ABAU AÇO CARB M16X45MM",
                "und": "un",
                "circular": "-",
                "dt": "2",
                "variavel": "-",
            },
            {
                "item": "ft",
                "descricao": "PARAFUSO CABEÇA M16",
                "und": "un",
                "circular": "2",
                "dt": "-",
                "variavel": "Poste",
            },
            # Material específico 15 kV
            {
                "item": "bf4a",
                "descricao": "BRAÇO REDE PROT TIPO L 354MM  ⚡ Específico 15 kV",
                "und": "un",
                "circular": "1",
                "dt": "1",
                "variavel": "-",
            },
            # Material específico 36,2 kV
            {
                "item": "bf4b",
                "descricao": "BRAÇO REDE PROT TIPO L 600MM  ⚡ Específico 36,2 kV",
                "und": "un",
                "circular": "1",
                "dt": "1",
                "variavel": "-",
            },
        ],
        "notas": [
            "A estrutura tipo CE1 é utilizada em tangentes e deflexões da rede até 6°.",
            "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação.",
        ],
    },

    # ── Adicione as próximas estruturas aqui seguindo o mesmo padrão ──
    # "CE1A": { ... },
    # "CE2":  { ... },
    # ...
}


# ─────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ─────────────────────────────────────────────

@st.cache_data(show_spinner="Carregando imagem da estrutura...")
def extrair_imagem(pdf_path: str, pagina: int, dpi: int,
                   crop_top: float, crop_bottom: float) -> bytes:
    """
    Rasteriza uma página do PDF e aplica recorte vertical.
    Retorna os bytes da imagem PNG em memória.
    Usa pdftoppm via subprocess (sem PyMuPDF).
    """
    import subprocess, tempfile, os, glob

    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = os.path.join(tmpdir, "pag")
        subprocess.run(
            [
                "pdftoppm",
                "-jpeg",
                "-r", str(dpi),
                "-f", str(pagina),
                "-l", str(pagina),
                pdf_path,
                prefix,
            ],
            check=True,
            capture_output=True,
        )
        arquivos = sorted(glob.glob(f"{prefix}-*.jpg"))
        if not arquivos:
            raise FileNotFoundError("pdftoppm não gerou imagem.")
        img = Image.open(arquivos[0])

    w, h = img.size
    top    = int(h * crop_top)
    bottom = int(h * (1.0 - crop_bottom)) if crop_bottom > 0 else h
    img = img.crop((0, top, w, bottom))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def renderizar_tabela_materiais(materiais: list):
    """Exibe a tabela de materiais com estilo personalizado."""

    # Cabeçalho
    header_cols = st.columns([1, 5, 1.2, 1.2, 1.5])
    header_cols[0].markdown("**Item**")
    header_cols[1].markdown("**Descrição**")
    header_cols[2].markdown("**Circular**")
    header_cols[3].markdown("**DT**")
    header_cols[4].markdown("**Variável**")
    st.divider()

    for m in materiais:
        cols = st.columns([1, 5, 1.2, 1.2, 1.5])
        cols[0].markdown(f"`{m['item']}`")
        cols[1].write(m["descricao"])
        cols[2].write(m["circular"])
        cols[3].write(m["dt"])
        cols[4].write(m["variavel"])


# ─────────────────────────────────────────────
# LAYOUT DA APLICAÇÃO
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Estruturas Elétricas – Neoenergia Elektro",
    page_icon="⚡",
    layout="wide",
)

# Cabeçalho
st.title("⚡ Estruturas Elétricas — DIS-NOR-013")
st.caption("Rede de Distribuição Aérea Compacta · REV 08 · Neoenergia Elektro")
st.divider()

# ── Seleção da estrutura ──
st.subheader("Selecione a estrutura")

codigos = list(ESTRUTURAS.keys())
cols_botoes = st.columns(min(len(codigos), 8))   # até 8 botões por linha

estrutura_selecionada = st.session_state.get("estrutura_ativa", None)

for idx, codigo in enumerate(codigos):
    col = cols_botoes[idx % 8]
    label = f"**{codigo}**" if codigo == estrutura_selecionada else codigo
    if col.button(codigo, key=f"btn_{codigo}", use_container_width=True):
        st.session_state["estrutura_ativa"] = codigo
        estrutura_selecionada = codigo

st.divider()

# ── Exibição da estrutura selecionada ──
if estrutura_selecionada and estrutura_selecionada in ESTRUTURAS:
    dados = ESTRUTURAS[estrutura_selecionada]

    # Título da estrutura
    st.subheader(dados["titulo"])
    st.markdown(f"**Aplicação:** {dados['subtitulo']}")
    st.write("")

    # Imagem do desenho
    try:
        img_bytes = extrair_imagem(
            pdf_path=PDF_PATH,
            pagina=dados["pagina_desenho"],
            dpi=DPI,
            crop_top=dados.get("crop_top_ratio", 0.13),
            crop_bottom=dados.get("crop_bottom_ratio", 0.0),
        )
        # Centraliza a imagem usando colunas
        col_img_esq, col_img_centro, col_img_dir = st.columns([0.5, 9, 0.5])
        with col_img_centro:
            st.image(img_bytes, use_container_width=True)

    except Exception as e:
        st.error(
            f"⚠️ Não foi possível carregar a imagem da estrutura.\n\n"
            f"Verifique se o PDF está no caminho: `{PDF_PATH}`\n\nErro: {e}"
        )

    st.write("")

    # Tabela de materiais
    st.markdown("### 📋 Relação de Materiais")
    renderizar_tabela_materiais(dados["materiais"])

    st.write("")

    # Notas
    if dados.get("notas"):
        st.markdown("### 📌 Notas")
        for i, nota in enumerate(dados["notas"], 1):
            st.markdown(f"{i}. {nota}")

else:
    st.info("👆 Clique em um botão acima para visualizar a estrutura.")
