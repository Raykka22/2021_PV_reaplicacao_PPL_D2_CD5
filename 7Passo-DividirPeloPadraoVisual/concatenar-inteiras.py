"""
Propósito: Concatenar verticalmente todas as imagens da pasta "inteiras"
Autor: Alexandre Nassar de Peder
Criação: 03/07/2026
"""

from PIL import Image
import os

# ==============================
# CONFIGURAÇÕES
# ==============================

PASTA_ENTRADA = "inteiras"
ARQUIVO_SAIDA = "colunas_concatenadas_verticalmente.png"

# Extensões aceitas
EXTENSOES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")

# ==============================
# CARREGAR IMAGENS
# ==============================

arquivos = sorted([
    arquivo
    for arquivo in os.listdir(PASTA_ENTRADA)
    if arquivo.lower().endswith(EXTENSOES)
])

if len(arquivos) == 0:
    raise Exception("Nenhuma imagem encontrada na pasta 'inteiras'.")

print(f"{len(arquivos)} imagens encontradas.")

imagens = []

largura_maxima = 0
altura_total = 0

for arquivo in arquivos:

    caminho = os.path.join(PASTA_ENTRADA, arquivo)

    img = Image.open(caminho).convert("RGB")

    imagens.append(img)

    largura_maxima = max(largura_maxima, img.width)
    altura_total += img.height

# ==============================
# CRIAR IMAGEM FINAL
# ==============================

imagem_final = Image.new(
    "RGB",
    (largura_maxima, altura_total),
    (255, 255, 255)
)

# ==============================
# COLAR AS IMAGENS
# ==============================

y = 0

for arquivo, img in zip(arquivos, imagens):

    imagem_final.paste(img, (0, y))

    print(f"Adicionada: {arquivo}")

    y += img.height

# ==============================
# SALVAR
# ==============================

imagem_final.save(ARQUIVO_SAIDA)

print()
print("Concluído!")
print(f"Imagem salva em: {ARQUIVO_SAIDA}")
print(f"Tamanho final: {imagem_final.width} x {imagem_final.height} pixels")