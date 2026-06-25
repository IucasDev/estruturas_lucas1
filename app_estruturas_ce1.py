import io
import streamlit as st
from PIL import Image

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────
PDF_PATH = "DIS-NOR-013-REV-08.pdf"   # << ajuste o caminho se necessário
DPI = 150                              # resolução da rasterização

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
    "pagina_desenho": 43,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 1 – CE1",
    "subtitulo": "Utilizada em tangente e em ângulo máximo de deflexão de 6°.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE1 é utilizada em tangentes e deflexões da rede até 6º;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE1A": {
    "pagina_desenho": 46,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 2 – CE1A",
    "subtitulo": "Utilizada em tangente e em ângulo máximo de deflexão de 6° utilizando o braço antibalanço.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf6",
        "descricao": "ESTRIBO BRACO L",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "bf2a",
        "descricao": "BRACO REDE PROT ANTIBAL 305MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6a",
        "descricao": "ESPAC RD PROT 15kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf2b",
        "descricao": "BRACO REDE PROT ANTIBAL 565MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6b",
        "descricao": "ESPAC RD PROT 35kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE1A é utilizada, a cada 200 m de rede, em longos trechos com várias estruturas tipo CE1;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE1A-PU": {
    "pagina_desenho": 49,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 3 – CE1A-PU",
    "subtitulo": "Utilizada em tangente e em ângulo máximo de deflexão de 6° utilizando o braço antibalanço. Preferencial em postes já instalados com elevação do nível da rede.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf6",
        "descricao": "ESTRIBO BRACO L",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "4",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf2a",
        "descricao": "BRACO REDE PROT ANTIBAL 305MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6a",
        "descricao": "ESPAC RD PROT 15kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE1A é utilizada, a cada 200 m de rede, em longos trechos com várias estruturas tipo CE1;",
      "Esta estrutura deve ser utilizada preferencialmente em postes já instalados onde há necessidade de elevação do",
      "nível da rede primária, como por exemplo em circuitos duplos;",
      "Deve ser respeitada as distancias de segurança estabelecidas neste normativo;",
      "Esta estrutura não se aplica em redes de 34,5 kV.",
      "A Estrutura CE1A-PU possibilita a elevar a altura da rede em 0,5 m quando comparada com a CE1A."
    ]
  },
  "CEJ1": {
    "pagina_desenho": 52,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 4 – CEJ1",
    "subtitulo": "Utilizada para aumentar o espaçamento da CE1 com afastador de 1650 mm.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf6",
        "descricao": "ESTRIBO BRACO L",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "bf14",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 1650MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6a",
        "descricao": "ESPAC RD PROT 15kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6b",
        "descricao": "ESPAC RD PROT 35kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CEJ1 é utilizada com o objetivo de afastar os condutores de edificações;",
      "A estrutura tipo CEJ1 não deve ser utilizada em postes de 200 daN quando a bitola dos condutores forem iguais",
      "ou superiores a 185 mm² para classe de tensão de 15 kV e iguais ou superiores a 70 mm² para classe de tensão",
      "de 36 kV;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CEJ1 SAH": {
    "pagina_desenho": 55,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 5 – CEJ1 SAH",
    "subtitulo": "Utilizada para aumentar o espaçamento da CE1 com afastador de 2500 mm.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf6",
        "descricao": "ESTRIBO BRACO L",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "bf10c",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 2500MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6a",
        "descricao": "ESPAC RD PROT 15kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bp6b",
        "descricao": "ESPAC RD PROT 35kV AUT-TRA POL 35-240MM2",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CEJ1 é utilizada com o objetivo de afastar os condutores de edificações;",
      "A estrutura tipo CEJ1 não deve ser utilizada em postes de 200 daN quando a bitola dos condutores forem iguais",
      "ou superiores a 185 mm² para classe de tensão de 15 kV e iguais ou superiores a 70 mm² para classe de tensão",
      "de 36 kV;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2": {
    "pagina_desenho": 58,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 6 – CE2",
    "subtitulo": "Utilizada em ângulos compreendidos entre 6° e 60°.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2 é utilizada nos casos de deflexão da rede de 7º à 60º para cabos de seções 35 mm² e 70",
      "mm² e 7º à 45º para cabos de seções 185 mm² e 240 mm²;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2-PU": {
    "pagina_desenho": 61,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 7 – CE2-PU",
    "subtitulo": "Utilizada em ângulos entre 6° e 60°. Preferencial em postes já instalados.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "4",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2 é utilizada nos casos de deflexão da rede de 7º à 60º para cabos de seções 35 mm² e 70",
      "mm² e 7º à 45º para cabos de seções 185 mm² e 240 mm²;",
      "Esta estrutura deve ser utilizada preferencialmente em postes já instalados onde há necessidade de elevação do",
      "nível da rede primária, como por exemplo em circuitos duplos;",
      "Deve ser respeitada as distancias de segurança estabelecidas neste normativo;",
      "Esta estrutura não se aplica em redes de 34,5 kV."
    ]
  },
  "CEJ2": {
    "pagina_desenho": 64,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 8 – CEJ2",
    "subtitulo": "Utilizada para aumentar o espaçamento da CE2 com afastador de 1650 mm.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "3",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "4",
        "variavel": "Poste"
      },
      {
        "item": "bf14",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 1650MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CEJ2 é utilizada nos casos de deflexão da rede de 7º à 45º ;",
      "Esta estrutura deve ser utilizada em locais onde há necessidade de deslocar a rede, decorrente de edificações,",
      "vegetação entre outros;",
      "Deve ser respeitada as distancias de segurança estabelecidas neste normativo;"
    ]
  },
  "CEJ2 SAH": {
    "pagina_desenho": 67,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 9 – CEJ2 SAH",
    "subtitulo": "Utilizada para aumentar o espaçamento da CE2 com afastador de 2500 mm.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "4",
        "variavel": "Poste"
      },
      {
        "item": "bf10c",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 2500MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CEJ2 SAH é utilizada nos casos de deflexão da rede de 7º à 45º ;",
      "Esta estrutura deve ser utilizada em locais onde há necessidade de deslocar a rede, decorrente de edificações,",
      "vegetação entre outros;",
      "Deve ser respeitada as distancias de segurança estabelecidas neste normativo;"
    ]
  },
  "CE3": {
    "pagina_desenho": 70,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 10 – CE3",
    "subtitulo": "Utilizada em fim de rede.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVAÇÃO COMPRESSÃO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gmf",
        "descricao": "MANILHA CURVA SAE1010 16,0MM 5000DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "5",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "0,60",
        "dt": "0,60",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "0,64",
        "dt": "0,64",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3 é utilizada em fim de rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de conexão, consultar Figura 14;",
      "Para a utilização de cobertura protetora para terminal de para-raios, consultar 6.17.12;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou aço",
      "cobreado são feitas com conectores paralelos de bronze estanhado (ab2) em substituição ao conector paralelo",
      "de liga de alumínio (ab1);",
      "O aterramento deverá ser executado com no mínimo 3 (três) hastes;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE3-PU": {
    "pagina_desenho": 73,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 11 – CE3-PU",
    "subtitulo": "Utilizada em fim de rede. Preferencial em áreas urbanas para fly tap.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "0,26",
        "dt": "0,26",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "6",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "4",
        "variavel": "Poste"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3 Perfil U é utilizada quando há previsão de extensão de rede futura;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva, ver 6.17.12;",
      "A instalação de para-raios nesta estrutura pode ser suprimida caso tenha para-raios em equipamentos ou outras",
      "estruturas a uma distância menor de 75 m do local onde esta estrutura será instalada.",
      "."
    ]
  },
  "CE4": {
    "pagina_desenho": 76,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 12 – CE4",
    "subtitulo": "Utilizada para amarração de rede com duplo encabeçamento. Ângulos entre 60° e 90°.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "ft1",
        "descricao": "PARAFUSO QUAD ACO CARB M16X50MM",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE4 é utilizada para deflexão de rede de 61º à 90º para cabos de seções 35 mm² e 70 mm² e 46º",
      "à 90º para cabos de seção 185 mm² e 240 mm², e também quando for necessário ancorar a rede primária;",
      "Evitar, sempre que possível, o seccionamento dos condutores. Caso seja necessário e em mudança de seção,",
      "prever conectores a compressão tipo “H” (ax), ou conectores perfurantes, para conexão das fases e conector",
      "paralelo (ab1) para conexão do cabo mensageiro;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE4-PU": {
    "pagina_desenho": 79,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 13 – CE4-PU",
    "subtitulo": "Utilizada para amarração de rede com duplo encabeçamento. Extensão a partir da CE3-PU.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "ft1",
        "descricao": "PARAFUSO QUAD ACO CARB M16X50MM",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE4 é utilizada para deflexão de rede de 61º à 90º para cabos de seções 35 mm² e 70 mm² e 46º",
      "à 90º para cabos de seção 185 mm² e 240 mm², e também quando for necessário ancorar a rede primária;",
      "Evitar, sempre que possível, o seccionamento dos condutores. Caso seja necessário e em mudança de seção,",
      "prever conectores a compressão tipo “H” (ax), ou conectores perfurantes, para conexão das fases e conector",
      "paralelo (ab1) para conexão do cabo mensageiro;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE3-CE3": {
    "pagina_desenho": 82,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 14 – CE3-CE3",
    "subtitulo": "Utilizada para ângulos de 60° a 120° com duplo encabeçamento.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gmf",
        "descricao": "MANILHA CURVA SAE1010 16,0MM 5000DAN",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "10",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "Poste"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3-CE3 é utilizada nos casos de deflexão da rede primária superior à 90º;",
      "Evitar, sempre que possível, o seccionamento dos condutores. Caso seja necessário e em mudança de seção,",
      "prever conectores a compressão tipo “H” (ax) para conexão das fases e conector paralelo (ab1) para conexão do",
      "cabo mensageiro;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE3PU-CE3PU": {
    "pagina_desenho": 85,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 15 – CE3PU-CE3PU",
    "subtitulo": "Utilizada para ângulos de 60° a 120° com duplo encabeçamento.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "6",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "5",
        "variavel": "Poste"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3PU-CE3PU é utilizada nos casos de deflexão da rede primária superior à 90º;",
      "Evitar, sempre que possível, o seccionamento dos condutores. Caso seja necessário e em mudança de seção,",
      "prever conectores a compressão tipo “H” (ax) ou perfurante para conexão das fases e conector paralelo (ab1)",
      "para conexão do cabo mensageiro;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2.3": {
    "pagina_desenho": 88,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 16 – CE2.3",
    "subtitulo": "Derivação aérea com estruturas no mesmo nível e mesmo lado.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gmf",
        "descricao": "MANILHA CURVA SAE1010 16,0MM 5000DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "5",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2.3 é utilizada quando a saída do ramal cruzar a rua;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Caso haja a necessidade de instalação de chaves-fusíveis, essas devem ser previstas na próxima estrutura após",
      "a derivação (estrutura CE4 CF);",
      "Para os casos de atendimento a consumidores primário, consultar as normas de fornecimento em rede primária",
      "de cada distribuidora;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2.CE3": {
    "pagina_desenho": 91,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 17 – CE2.CE3",
    "subtitulo": "Derivação aérea com estruturas no mesmo nível, lados opostos.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gmf",
        "descricao": "MANILHA CURVA SAE1010 16,0MM 5000DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "8",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "3",
        "variavel": "Poste"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf3a",
        "descricao": "BRACO REDE PROT TIPO C 580X440X365X76MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "5",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "5",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf3b",
        "descricao": "BRACO REDE PROT TIPO C 640X495X470X76MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "5",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "5",
        "dt": "5",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2.CE3 é utilizada quando a saída do ramal não cruzar a rua;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2-CE3": {
    "pagina_desenho": 94,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 18 – CE2-CE3",
    "subtitulo": "Derivação aérea com estruturas em níveis diferentes, lados opostos.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "9",
        "dt": "13",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2-CE3 é utilizada quando a saída do ramal cruzar a rua;",
      "Esta estrutura é limitada a derivações com corrente máxima de 50 A. Para correntes de valores superiores,",
      "substituir o grampo de linha viva e o conector estribo por conector a compressão tipo “H” (ax);",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva, ver 6.17.12;",
      "Esta estrutura pode ser utilizada também para derivar rede compacta de rede nua existente, na estrutura do",
      "primeiro nível;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2-CE3 CF": {
    "pagina_desenho": 97,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 19 – CE2-CE3 CF",
    "subtitulo": "Derivação aérea com chaves fusíveis, níveis diferentes, lados opostos.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "10",
        "dt": "14",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2-CE3 CF é utilizada quando a saída do ramal não irá cruzar a rua e há a necessidade de",
      "instalação de chaves-fusíveis;",
      "Esta estrutura é limitada a derivações com corrente máxima de 50 A. Para correntes de valores superiores,",
      "substituir o grampo de linha viva e o conector estribo por conector a compressão tipo “H” (ax).",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14.",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha, consultar 6.17.12.",
      "Esta estrutura pode ser utilizada também para derivar rede compacta de rede nua existente, na estrutura do",
      "primeiro nível. Nesta condição deverá ser adicionado isolador de pino e pino (ie/bm) na estrutura de derivação",
      "para o jumper até a chave;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2-CE3 CF LP": {
    "pagina_desenho": 100,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 20 – CE2-CE3 CF LP",
    "subtitulo": "Derivação aérea com chaves fusíveis, lado do passeio.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "10",
        "dt": "14",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2-CE3 CF LP (lado passeio) é utilizada quando a saída do ramal irá cruzar a rua e há a",
      "necessidade de instalação de chaves-fusíveis do lado do passeio;",
      "Esta estrutura é limitada a derivações com corrente máxima de 50 A. Para correntes de valores superiores,",
      "substituir o grampo de linha viva e o conector estribo por conector a compressão tipo “H” (ax).",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14.",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha, consultar 6.17.12.",
      "Esta estrutura pode ser utilizada também para derivar rede compacta de rede nua existente, na estrutura do",
      "primeiro nível. Nesta condição deverá ser adicionado isolador de pino e pino (ie/bm) na estrutura de derivação",
      "para o jumper até a chave;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação;",
      "Esta estrutura só pode ser utilizada em locais onde a calçada tenha largura suficiente para a operação da chave",
      "fusível."
    ]
  },
  "CE2-N3 CF": {
    "pagina_desenho": 103,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 21 – CE2-N3 CF",
    "subtitulo": "Derivação aérea em rede convencional com chaves fusíveis.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "10",
        "dt": "13",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6,6",
        "dt": "6,6",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "7",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "8,5",
        "dt": "8,5",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "9,5",
        "dt": "9,5",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2-N3 CF é utilizada em derivação para ramal com rede nua;",
      "Esta estrutura é limitada a derivações com corrente máxima de 50 A. Para correntes de valores superiores,",
      "substituir o grampo de linha viva e o conector estribo por conector a compressão tipo “H” (ax);",
      "Para a utilização de cobertura protetora de estribo e grampo de linha viva, consultar 6.17.12;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de conexão, consultar Figura 14;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE2 DS": {
    "pagina_desenho": 106,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 22 – CE2 DS",
    "subtitulo": "Derivação rede compacta em tangência para rede subterrânea.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "18",
        "dt": "23",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "3,5",
        "dt": "3,5",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "8",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fl3",
        "descricao": "HASTE ATERRAM CIRC 13,0X 2400,0MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "7",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "10",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "cb11",
        "descricao": "CABO DE COBRE EPR 20KV",
        "und": "m",
        "circular": "Adeq.",
        "dt": "Adeq.",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "pb1",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,0M REFORCADA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "eq10",
        "descricao": "TERMINACAO CONTRÁTIL EXT. A FRIO 15  KV",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "Cabo"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "cb17",
        "descricao": "CABO DE COBRE EPR 35KV",
        "und": "m",
        "circular": "Adeq.",
        "dt": "Adeq.",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "eq17",
        "descricao": "TERMINACAO CONTRÁTIL EXT. A FRIO 36,2  KV",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "Cabo"
      }
    ],
    "notas": [
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "CE3 DS": {
    "pagina_desenho": 109,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 23 – CE3 DS",
    "subtitulo": "Derivação de fim de rede compacta para rede subterrânea.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "17",
        "dt": "20",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "3,5",
        "dt": "3,5",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "- fg 3423030 51608 26005103 GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fl3",
        "descricao": "HASTE ATERRAM CIRC 13,0X 2400,0MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "7",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "cb11",
        "descricao": "CABO DE COBRE EPR 20KV",
        "und": "m",
        "circular": "Adeq.",
        "dt": "Adeq.",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "eq10",
        "descricao": "TERMINACAO CONTRÁTIL EXT. A FRIO 15  KV",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "Cabo"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "cb17",
        "descricao": "CABO DE COBRE EPR 35KV",
        "und": "m",
        "circular": "Adeq.",
        "dt": "Adeq.",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "eq17",
        "descricao": "TERMINACAO CONTRÁTIL EXT. A FRIO 36,2  KV",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "Cabo"
      }
    ],
    "notas": [
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "N3.CE3": {
    "pagina_desenho": 112,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 24 – N3.CE3",
    "subtitulo": "Transição da estrutura N3 da rede convencional para rede compacta.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "8",
        "dt": "9",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "5",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "7",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo N3.CE3 é utilizada nas transições de rede nua para rede protegida compacta, para ângulo de",
      "deflexão até 60º;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar 6.17.12;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "N3.CE3 SUH": {
    "pagina_desenho": 115,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 25 – N3.CE3 SUH",
    "subtitulo": "Transição N3 para rede compacta com seccionadores unipolares horizontais.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "20",
        "dt": "21",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "adeq",
        "dt": "adeq.",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "4",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "gj1",
        "descricao": "SUPORTE INCL SECCIONADOR FACA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ec1",
        "descricao": "CH SEC 15KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ec3",
        "descricao": "CH SEC 36,2KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo N3.CE3 SUH é utilizada nas transições de Rede Nua para rede protegida compacta com",
      "seccionador tipo faca unipolar na posição horizontal;",
      "Observar o sentido Fonte-Carga;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva, 6.17.12;",
      "Para a tensão de 36,2 kV, as ferragens do seccionador unipolar tipo faca devem ser interligadas ao cabo",
      "mensageiro e aterradas;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "A posição do seccionador deve ser invertida para o caso de transição de rede protegida compacta para rede nua;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação."
    ]
  },
  "N3.CE3 SUI": {
    "pagina_desenho": 118,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 26 – N3.CE3 SUI",
    "subtitulo": "Transição N3 para rede compacta com seccionadores unipolares inclinados.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "21",
        "dt": "22",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "adeq",
        "dt": "adeq",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "4",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "gj1",
        "descricao": "SUPORTE INCL SECCIONADOR FACA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ec1",
        "descricao": "CH SEC 15KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ec3",
        "descricao": "CH SEC 36,2KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "",
      "A estrutura tipo N3.CE3 SUI é utilizada nas transições de rede nua para rede protegida compacta com seccionador unipolar",
      "tipo faca na posição inclinada. Observar o sentido Fonte-Carga;",
      "",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva e de cobertura protetora de",
      "estribo, conector e conector de derivação de linha viva, ver 6.17.12;",
      "",
      "A posição do seccionador unipolar tipo faca deve ser invertida para o caso de transição de rede protegida compacta para rede",
      "nua;",
      "",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou cobreado",
      "devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector paralelo de liga de alumínio",
      "(ab1);",
      "",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede protegida",
      "compacta;",
      "",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.11 desta especificação;",
      "",
      "Nesta estrutura podemos em substituição a chave seccionadora unipolar tipo faca utilizar chave corta circuito fusível com",
      "estribo e grampo de linha viva. A utilização de conector estribo e grampo de linha viva está limitada a corrente de 50 A. Para",
      "corrente superiores utilizar conector tipo “H” (ax)."
    ]
  },
  "B3.CE3": {
    "pagina_desenho": 121,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 27 – B3.CE3",
    "subtitulo": "Transição da estrutura L3/B3 da rede convencional para rede compacta.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "10",
        "dt": "12",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fm2",
        "descricao": "MAO FRANCESA PERFIL ACO 44X 5,0X1971MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "5",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb1",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,0M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo B3.CE3 é utilizada nas transições da estrutura L3 ou B3 da rede convencional para rede",
      "compacta;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "B3.CE3 SUI": {
    "pagina_desenho": 124,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 28 – B3.CE3 SUI",
    "subtitulo": "Transição de rede nua para rede protegida compacta, ângulo até 60°.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "10",
        "dt": "12",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn3",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 1053MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fm2",
        "descricao": "MAO FRANCESA PERFIL ACO 44X 5,0X1971MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "4",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "gj1",
        "descricao": "SUPORTE INCL SECCIONADOR FACA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ec1",
        "descricao": "CH SEC 15KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ec3",
        "descricao": "CH SEC 36,2KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo N3.CE3 SUI é utilizada nas transições de rede nua para rede protegida compacta, para angulo de",
      "deflexão até 60º;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta."
    ]
  },
  "CE3-I": {
    "pagina_desenho": 127,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 29 – CE3-I",
    "subtitulo": "Transição da rede isolada para rede compacta.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "10",
        "dt": "11",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "5",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3-I é utilizada nas transições de rede isolada para rede protegida compacta e vice-versa;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta;",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva e de cobertura",
      "protetora de estribo, conector e conector de derivação de linha viva, ver 6.17.12;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE3-I SUI": {
    "pagina_desenho": 130,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 30 – CE3-I SUI",
    "subtitulo": "Transição da rede isolada para rede compacta com seccionadores unipolares inclinados.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "23",
        "dt": "24",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "0,50",
        "dt": "0,50",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "5",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "3",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "4",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "ft3",
        "descricao": "PARAFUSO QUAD ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "gj1",
        "descricao": "SUPORTE INCL SECCIONADOR FACA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ec1",
        "descricao": "CH SEC 15KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ec3",
        "descricao": "CH SEC 36,2KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3-I SUI utilizada nas transições de rede protegida compacta para rede isolada com instalação",
      "de seccionador unipolar;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Na relação de materiais somente estão contemplados os materiais necessários à instalação da estrutura da rede",
      "protegida compacta;",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva, ver 6.17.12;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE2 PR": {
    "pagina_desenho": 133,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 31 – CE2 PR",
    "subtitulo": "Utilizada para instalação de para-raios ao longo da rede.",
    "materiais": [
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "0,26",
        "dt": "0,26",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf5",
        "descricao": "CANTONEIRA 65X65X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "7",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "Poste"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2 PR é utilizada quando há a necessidade de instalação de para-raios ao longo da rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Para a utilização de cobertura protetora de estribo, conector e conector de derivação de linha viva, ver 6.17.12;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE4 CF": {
    "pagina_desenho": 136,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 32 – CE4 CF",
    "subtitulo": "Utilizada para instalação de chaves fusíveis ao longo da rede.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fd",
        "descricao": "ARRUELA LIS CIRC SAE1020 M18",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "12",
        "dt": "12",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "5",
        "dt": "9",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE4 CF é utilizada para instalação de chaves-fusíveis ao longo da rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Evitar, sempre que possível, o seccionamento do cabo mensageiro. Caso seja necessário, prever conector",
      "paralelo (ab1);",
      "Observar o sentido Fonte-Carga;",
      "Para os critérios de aplicação das chaves-fusíveis, consultar a Norma DIS-NOR-012;",
      "As chaves-fusíveis podem ser instaladas, formando ângulos de até 30º em relação ao eixo longitudinal da rede e",
      "voltadas para o centro da estrutura, visando à facilidade de operação das mesmas;",
      "Utilizar arruelas redondas para a fixação da mão-francesa em fibra de vidro na estrutura;",
      "Em substituição ao conector ax, para corrente até 50 A, pode-se utilizar conector estribo e grampo de linha via;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE4 CF SAH": {
    "pagina_desenho": 139,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 33 – CE4 CF SAH",
    "subtitulo": "Utilizada para chaves fusíveis com braço afastador horizontal.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fd",
        "descricao": "ARRUELA LIS CIRC SAE1020 M18",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "12",
        "dt": "12",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ax",
        "descricao": "CONECTOR DERIVACAO COMPRESSAO \"H\" AL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "2",
        "dt": "6",
        "variavel": "Poste"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf10b",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 1650MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE4 CF com suporte afastador horizontal (SAH) é utilizada para instalação de chaves fusíveis",
      "com suporte afastador horizontal ao longo da rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Evitar, sempre que possível, o seccionamento do cabo mensageiro. Caso seja necessário, prever conector",
      "paralelo (ab1);",
      "Observar o sentido Fonte-Carga;",
      "Observar que o suporte z é fixado na parte inferior do suporte afastador horizontal, permitindo assim atingir a",
      "distância mínima de segurança entre fase e terra e correta fixação;",
      "Em substituição ao conector ax, para corrente até 50 A, pode-se utilizar conector estribo e grampo de linha via;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE4 SUH": {
    "pagina_desenho": 142,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 34 – CE4 SUH",
    "subtitulo": "Utilizada para seccionadores unipolares com montagem horizontal.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "12",
        "dt": "10",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "5",
        "dt": "9",
        "variavel": "Poste"
      },
      {
        "item": "ft2",
        "descricao": "PARAFUSO QUAD ACO CARB M16X125MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "10",
        "dt": "10",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ec1",
        "descricao": "CH SEC 15KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ec3",
        "descricao": "CH SEC 36,2KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE4 SUH é utilizada para instalação de seccionadores unipolares na posição horizontal ao longo",
      "da rede;",
      "Observar o sentido Fonte-Carga;",
      "Evitar, sempre que possível, o seccionamento do cabo mensageiro. Caso seja necessário, prever conector",
      "paralelo (ab1);",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "As ferragens dos seccionadores de classe 36,2 kV devem ser interligadas ao cabo mensageiro e aterradas;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE4 SUI": {
    "pagina_desenho": 145,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 35 – CE4 SUI",
    "subtitulo": "Utilizada para seccionadores unipolares com montagem inclinada.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "21",
        "dt": "21",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ay",
        "descricao": "CONECTOR TERMINAL COMPRESSAO",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "pb2",
        "descricao": "CRUZETA FIBRA RETA 90X90 2,4M REFORCADA",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn2",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 726MM",
        "und": "un",
        "circular": "7",
        "dt": "7",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fu3",
        "descricao": "PARAFUSO ABAU ACO CARB M16X150MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "5",
        "dt": "9",
        "variavel": "Poste"
      },
      {
        "item": "fy",
        "descricao": "PORCA QUAD SAE1020 M16",
        "und": "un",
        "circular": "10",
        "dt": "10",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gc",
        "descricao": "SELA CRUZETA 110X116MM",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "gj1",
        "descricao": "SUPORTE INCL SECCIONADOR FACA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ec1",
        "descricao": "CH SEC 15KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ie1",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 15,0KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "ec3",
        "descricao": "CH SEC 36,2KV 630A 1P MAN SECO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "ie2",
        "descricao": "PINO ISOLADOR RETO NORMAL ACO 36,2KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE4 SUI é utilizada para instalação de seccionadores unipolares na posição inclinada ao longo",
      "da rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Evitar, sempre que possível, o seccionamento do cabo mensageiro. Caso seja necessário, prever conector",
      "paralelo (ab1);",
      "Observar o sentido Fonte-Carga;",
      "As ferragens dos seccionadores devem ser interligadas ao cabo mensageiro e aterradas;",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE2 TR": {
    "pagina_desenho": 148,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 36 – CE2 TR",
    "subtitulo": "Utilizada para instalação de transformador trifásico sob rede compacta.",
    "materiais": [
      {
        "item": "fd",
        "descricao": "ARRUELA LIS CIRC SAE1020 M18",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "6",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bl",
        "descricao": "FIO ALUM COBERTO 10MM2",
        "und": "m",
        "circular": "4,5",
        "dt": "4,5",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "9",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "8",
        "variavel": "Poste"
      },
      {
        "item": "ft1",
        "descricao": "PARAFUSO QUAD ACO CARB M16X50MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bf10b",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 1650MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fx",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO DT",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "ge",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO R",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf4a",
        "descricao": "BRACO REDE PROT TIPO L 354MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "5,5",
        "dt": "5,5",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "bf4b",
        "descricao": "BRACO REDE PROT TIPO L 600MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "6,5",
        "dt": "6,5",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE2 TR é utilizada para posto de transformação ao longo da rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Para a utilização de cobertura protetora de estribo, grampo de linha viva, para-raios e bucha do transformador,",
      "ver 6.17.12;",
      "Observar que o suporte z é fixado na parte inferior do suporte afastador horizontal, permitindo assim atingir a",
      "distância mínima de segurança entre fase e terra e correta fixação;",
      "Para o caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE3 TR": {
    "pagina_desenho": 151,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 37 – CE3 TR",
    "subtitulo": "Utilizada para transformador trifásico em fim de rede compacta.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fd",
        "descricao": "ARRUELA LIS CIRC SAE1020 M18",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "7",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "Poste"
      },
      {
        "item": "ft1",
        "descricao": "PARAFUSO QUAD ACO CARB M16X50MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf10b",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 1650MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fx",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO DT",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "ge",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO R",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "9,5",
        "dt": "9,5",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "10,5",
        "dt": "10,5",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3 TR é utilizada para postos de transformação em finais de rede;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Para a utilização de cobertura protetora de estribo, grampo de linha viva, para-raios e bucha do transformador,",
      "ver 6.17.12;",
      "Observar que o suporte z é fixado na parte inferior do suporte afastador horizontal, permitindo assim atingir a",
      "distância mínima de segurança entre fase e terra e correta fixação;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado(ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE3 TRSC": {
    "pagina_desenho": 154,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 38 – CE3 TRSC",
    "subtitulo": "Utilizada para transformador trifásico sem chaves fusíveis em fim de rede.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fd",
        "descricao": "ARRUELA LIS CIRC SAE1020 M18",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "fg",
        "descricao": "GANCHO SUSP OLHAL",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "2",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "7",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "Poste"
      },
      {
        "item": "ft1",
        "descricao": "PARAFUSO QUAD ACO CARB M16X50MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fx",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO DT",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "ge",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO R",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "10,5",
        "dt": "10,5",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11a",
        "descricao": "SUPORTE REDE PROT HORIZ 675X300X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "10,5",
        "dt": "10,5",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf11b",
        "descricao": "SUPORTE REDE PROT HORIZ 875X400X60MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      }
    ],
    "notas": [
      "A estrutura tipo CE3 TRSC é utilizada para postos de transformação em finais de rede quando não for instalada",
      "chave fusível deslocada;",
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Para a utilização de cobertura protetora de estribo, grampo de linha viva, para-raios e bucha do transformador,",
      "ver 6.17.12;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado (ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "CE4 TR": {
    "pagina_desenho": 157,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 39 – CE4 TR",
    "subtitulo": "Utilizada para transformador trifásico sob rede compacta.",
    "materiais": [
      {
        "item": "ga4",
        "descricao": "ALCA PREFORMADA ESTAI 7,90 MM EAR",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fd",
        "descricao": "ARRUELA LIS CIRC SAE1020 M18",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "feb",
        "descricao": "ARRUELA LIS QUAD SAE1020 M18",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "dh7",
        "descricao": "CABO ISOL COBRE XLPE PT  10,00MM2",
        "und": "m",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ff",
        "descricao": "CINTA DE ACO CARBONO",
        "und": "un",
        "circular": "4",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "af",
        "descricao": "CONECTOR DERIVACAO TIPO ESTRIBO",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "Cabo"
      },
      {
        "item": "ae",
        "descricao": "GRAMPO LINHA VIVA BR",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "ab2",
        "descricao": "GRAMPO PARAL BRONZE  10,0-70,0MM2",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "gg",
        "descricao": "MANILHA SAPATILHA ACO  5000DAN",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "fn1",
        "descricao": "MAO FRANCESA NORMAL ACO 32X 6,0X 619MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fq",
        "descricao": "OLHAL P/PARAF FOFO M16-5/8\" 5000DAN",
        "und": "un",
        "circular": "8",
        "dt": "8",
        "variavel": "-"
      },
      {
        "item": "fu1",
        "descricao": "PARAFUSO ABAU ACO CARB M16X45MM",
        "und": "un",
        "circular": "7",
        "dt": "5",
        "variavel": "-"
      },
      {
        "item": "fu2",
        "descricao": "PARAFUSO ABAU ACO CARB M16X70MM",
        "und": "un",
        "circular": "1",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ft",
        "descricao": "PARAFUSO CABECA M16",
        "und": "un",
        "circular": "-",
        "dt": "6",
        "variavel": "Poste"
      },
      {
        "item": "ft1",
        "descricao": "PARAFUSO QUAD ACO CARB M16X50MM",
        "und": "un",
        "circular": "4",
        "dt": "4",
        "variavel": "-"
      },
      {
        "item": "bf8",
        "descricao": "PERFIL U ACO GALV 76X38X6,5X900MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "gb",
        "descricao": "SAPATILHA CABO 9,5MM",
        "und": "un",
        "circular": "2",
        "dt": "2",
        "variavel": "-"
      },
      {
        "item": "bf10b",
        "descricao": "SUPORTE AFASTADOR HORIZ ACO RC 1650MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fx",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO DT",
        "und": "un",
        "circular": "-",
        "dt": "2",
        "variavel": "Poste"
      },
      {
        "item": "ge",
        "descricao": "SUPORTE INSTALAÇÃO DE EQUIPAMENTO R",
        "und": "un",
        "circular": "2",
        "dt": "-",
        "variavel": "Poste"
      },
      {
        "item": "bf12",
        "descricao": "SUPORTE REDE PROT TIPO Z 85X113X85MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "ba1",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 15 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "9,5",
        "dt": "9,5",
        "variavel": "-"
      },
      {
        "item": "ee1",
        "descricao": "CHAVE FUS DIST C   15KV 100A 7,1KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk1",
        "descricao": "ISOLADOR SUSP POLIMERICO 50KN 15kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "bm1",
        "descricao": "ISOLADOR PINO POLIM 15,0KV 25MM 1200DAN",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "bf9a",
        "descricao": "PINO ISOL ACO 16,0MM 154X38X192MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "br1",
        "descricao": "PARA-RAIOS RD 12KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      },
      {
        "item": "ba2",
        "descricao": "ALCA PRE-FORMADA CABO COBERTO 36,2 KV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "Cabo"
      },
      {
        "item": "bd31",
        "descricao": "CABO AEREO COBRE XLPE 15KV  16,00MM2",
        "und": "m",
        "circular": "10,5",
        "dt": "10,5",
        "variavel": "-"
      },
      {
        "item": "ee5",
        "descricao": "CH FUS DIST C 34,5KV 300A 3,5KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bk2",
        "descricao": "ISOLADOR SUSP POLIMERICO 50kN 35kV",
        "und": "un",
        "circular": "6",
        "dt": "6",
        "variavel": "-"
      },
      {
        "item": "br2",
        "descricao": "PARA-RAIOS RD 33KV 10KA",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bm2",
        "descricao": "ISOLADOR PINO POLIM 36,2KV 25MM 1200DAN",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "bf9b",
        "descricao": "PINO ISOL ACO 18,0MM 200X40X240MM",
        "und": "un",
        "circular": "3",
        "dt": "3",
        "variavel": "-"
      },
      {
        "item": "un",
        "descricao": "-",
        "und": "un",
        "circular": "-",
        "dt": "-",
        "variavel": "-"
      }
    ],
    "notas": [
      "Para reconstituição da cobertura do cabo coberto nos pontos de emenda, consultar Figura 14;",
      "Para a utilização de cobertura protetora de estribo, grampo de linha viva, para-raios e bucha do transformador,",
      "ver 6.17.12;",
      "Observar que o suporte z é fixado na parte inferior do suporte afastador horizontal, permitindo assim atingir a",
      "distância mínima de segurança entre fase e terra e correta fixação;",
      "No caso de aterramento com cabo de cobre ou fio de aço cobreado, as conexões entre materiais de cobre ou",
      "cobreado devem ser feitas com conectores paralelo de bronze estanhado(ab2) em substituição ao conector",
      "paralelo de liga de alumínio (ab1);",
      "Os postes DT (ph) e circular (pa) devem ser definidos conforme item 6.10 desta especificação."
    ]
  },
  "Aterramento Ext": {
    "pagina_desenho": 159,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 40 – Aterramento com Condutor Externo",
    "subtitulo": "Aterramento do cabo mensageiro com condutor externo ao poste.",
    "materiais": [
      {
        "item": "jb",
        "descricao": "CABO NU ACO-COBRE  2 AWG",
        "und": "kg",
        "circular": "2,85",
        "dt": "2,85",
        "variavel": "-"
      },
      {
        "item": "dx3",
        "descricao": "FIO ALUM NU H14/H24 21,15MM2",
        "und": "kg",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fl3",
        "descricao": "HASTE ATERRAM CIRC 13,0X 2400,0MM",
        "und": "un",
        "circular": "adeq.",
        "dt": "adeq.",
        "variavel": "-"
      },
      {
        "item": "dr2",
        "descricao": "MASSA CALAFETADORA",
        "und": "kg",
        "circular": "adeq.",
        "dt": "adeq",
        "variavel": "-"
      },
      {
        "item": "pf",
        "descricao": "MOLDURA POLIMERICA FIO TERRA 30X 3000MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      }
    ],
    "notas": [
      "Nesta relação de materiais, constam somente os itens necessários à descida do condutor para aterramento até a",
      "primeira haste. A cada haste adicional, acrescentar os materiais necessários;",
      "O condutor de aterramento deve ser o fio de aço cobreado 2 AWG (jb), utilizados com hastes circular de aço",
      "cobreado (fl3);",
      "A conexão entre o condutor de descida e a haste de aterramento deve ser protegida com massa calafetadora",
      "(0,10 kg por haste);",
      "Sempre que houver neutro da rede secundária, o condutor de aterramento deve ser interligado;",
      "As amarrações da moldura de proteção do condutor de aterramento devem ser feitas com 0,60 kg de fio de",
      "alumínio nu H14, constituídas de cinco voltas cada e no mínimo três pontos, e as amarrações do condutor de",
      "descida no poste devem ser feitas com o mesmo fio, constituídas de uma volta por ponto de amarração.",
      "O comprimento previsto do condutor de aterramento é suficiente para poste até 12 m;",
      "Em substituição ao fio H14 para amarração da moldura, pode ser utilizado fita de aço inoxidável, ajustador e",
      "fecho."
    ]
  },
  "Aterramento Int": {
    "pagina_desenho": 162,
    "crop_top_ratio": 0.13,
    "crop_bottom_ratio": 0.0,
    "titulo": "Estrutura 41 – Aterramento com Condutor Interno",
    "subtitulo": "Aterramento do cabo mensageiro com condutor interno ao poste.",
    "materiais": [
      {
        "item": "di2",
        "descricao": "CABO COBRE NU 25MM2 1F CL2A",
        "und": "kg",
        "circular": "2,65",
        "dt": "2,65",
        "variavel": "-"
      },
      {
        "item": "as",
        "descricao": "CONECTOR COMP COBRE 1/0-2/0/ F8- 2AWG",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "ab1",
        "descricao": "GRAMPO PARAL ALUM 6,05-10,50MM",
        "und": "un",
        "circular": "1",
        "dt": "1",
        "variavel": "-"
      },
      {
        "item": "fl3",
        "descricao": "HASTE ATERRAM CIRC 13,0X 2400,0MM",
        "und": "kg",
        "circular": "adeq",
        "dt": "adeq",
        "variavel": "-"
      },
      {
        "item": "dr2",
        "descricao": "MASSA CALAFETADORA",
        "und": "un",
        "circular": "adeq",
        "dt": "adeq",
        "variavel": "-"
      }
    ],
    "notas": [
      "Nesta relação de materiais, constam somente os itens necessários à descida do condutor para aterramento até a",
      "primeira haste. A cada haste adicional, acrescentar os materiais necessários;",
      "O condutor de aterramento deve ser cabo de cobre nu meio duro 25 mm² (di2).",
      "Neste tipo de aterramento, o condutor desce internamente ao poste e deve ser executado nos casos de",
      "construção de estruturas para instalação de equipamentos e/ou em regiões de alta agressividade ambiental",
      "(poluentes químicos) ou em regiões litorâneas, onde sejam utilizados condutores de cobre ou cobreados como",
      "descida para o aterramento, mesmo que a rede seja com cabos de alumínio. Quando não houver necessidade de",
      "utilização de condutores cobreados ou de cobre, deve ser obedecido o padrão constante na Estrutura 40;",
      "A conexão entre o condutor de descida e a haste de aterramento deve ser protegida com massa calafetadora",
      "(0,10 kg por haste);",
      "Sempre que houver neutro da rede secundária, o condutor de aterramento deve ser interligado;",
      "O comprimento previsto do condutor de aterramento é suficiente para poste até 12 m."
    ]
  }
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
    Tenta pdftoppm (se poppler-utils instalado), senão usa PyMuPDF.
    """
    import subprocess, tempfile, os, glob

    # Tenta pdftoppm
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            prefix = os.path.join(tmpdir, "pag")
            subprocess.run(
                ["pdftoppm", "-jpeg", "-r", str(dpi), "-f", str(pagina), "-l", str(pagina), pdf_path, prefix],
                check=True, capture_output=True,
            )
            arquivos = sorted(glob.glob(f"{prefix}-*.jpg"))
            if arquivos:
                img = Image.open(arquivos[0])
                w, h = img.size
                top    = int(h * crop_top)
                bottom = int(h * (1.0 - crop_bottom)) if crop_bottom > 0 else h
                img = img.crop((0, top, w, bottom))
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                return buf.getvalue()
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Fallback: PyMuPDF
    import pymupdf
    doc = pymupdf.open(pdf_path)
    page = doc[pagina - 1]
    mat = pymupdf.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
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

# ── Agrupamento das estruturas ──
CATEGORIAS = {
    "Básicas (Tangente/Ângulo)": ["CE1", "CE1A", "CE1A-PU", "CEJ1", "CEJ1 SAH"],
    "Ângulo (6° a 60°)": ["CE2", "CE2-PU", "CEJ2", "CEJ2 SAH"],
    "Fim de Rede / Ancoragem": ["CE3", "CE3-PU", "CE4", "CE4-PU"],
    "Duplo Encabeçamento": ["CE3-CE3", "CE3PU-CE3PU"],
    "Derivações": ["CE2.3", "CE2.CE3", "CE2-CE3", "CE2-CE3 CF", "CE2-CE3 CF LP", "CE2-N3 CF"],
    "Derivações Subterrâneas": ["CE2 DS", "CE3 DS"],
    "Transições Convenção/Isolada": ["N3.CE3", "N3.CE3 SUH", "N3.CE3 SUI", "B3.CE3", "B3.CE3 SUI", "CE3-I", "CE3-I SUI"],
    "Para-raios / Chaves": ["CE2 PR", "CE4 CF", "CE4 CF SAH", "CE4 SUH", "CE4 SUI"],
    "Transformadores": ["CE2 TR", "CE3 TR", "CE3 TRSC", "CE4 TR"],
    "Aterramentos": ["Aterramento Ext", "Aterramento Int"],
}

# ── Seleção da estrutura ──
st.subheader("Selecione a estrutura")

estrutura_selecionada = st.session_state.get("estrutura_ativa", None)

# Cria um mapeamento código -> código para o selectbox
codigos = list(ESTRUTURAS.keys())
categoria_map = {}
for cat, itens in CATEGORIAS.items():
    for item in itens:
        categoria_map[item] = cat

# Selectbox com formato "código - categoria"
opcoes = {c: f"{c} ({categoria_map.get(c, 'Outros')})" for c in codigos}
opcao_lista = list(opcoes.values())

indice_atual = codigos.index(estrutura_selecionada) if estrutura_selecionada in codigos else 0

selecao = st.selectbox(
    "Escolha uma estrutura:",
    options=opcao_lista,
    index=indice_atual,
    format_func=lambda x: x,
)

# Extrai o código da opção selecionada
codigo_selecionado = None
for cod, label in opcoes.items():
    if label == selecao:
        codigo_selecionado = cod
        break

if codigo_selecionado:
    estrutura_selecionada = codigo_selecionado
    st.session_state["estrutura_ativa"] = codigo_selecionado

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
