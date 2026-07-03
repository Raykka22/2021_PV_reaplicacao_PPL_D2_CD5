from PIL import Image
import numpy as np

# ==========================================
# CONFIGURAÇÕES
# ==========================================

ARQUIVO_ENTRADA = "colunas_concatenadas_verticalmente.png"
ARQUIVO_SAIDA = "colunas_sem_espacos.png"

# Pixel considerado branco
LIMIAR_BRANCO = 245

# Espaços maiores que isso serão reduzidos
ALTURA_MIN_ESPACO = 40

# Espaço que permanecerá entre blocos
ESPACO_FINAL = 10

# ==========================================
# ABRIR IMAGEM
# ==========================================

img = Image.open(ARQUIVO_ENTRADA).convert("RGB")
dados = np.array(img)

altura, largura = dados.shape[:2]

# ==========================================
# REMOVER BORDAS BRANCAS
# ==========================================

mascara = np.any(dados < LIMIAR_BRANCO, axis=2)

ys, xs = np.where(mascara)

top = ys.min()
bottom = ys.max()

left = xs.min()
right = xs.max()

dados = dados[top:bottom+1, left:right+1]

altura, largura = dados.shape[:2]

# ==========================================
# DETECTAR LINHAS VAZIAS
# ==========================================

linhas_vazias = []

for y in range(altura):

    linha = dados[y]

    if np.all(linha > LIMIAR_BRANCO):
        linhas_vazias.append(True)
    else:
        linhas_vazias.append(False)

# ==========================================
# ENCONTRAR BLOCOS
# ==========================================

blocos = []

inicio = 0
y = 0

while y < altura:

    if linhas_vazias[y]:

        inicio_espaco = y

        while y < altura and linhas_vazias[y]:
            y += 1

        fim_espaco = y

        tamanho = fim_espaco - inicio_espaco

        if tamanho >= ALTURA_MIN_ESPACO:

            blocos.append((inicio, inicio_espaco))

            inicio = fim_espaco

    else:
        y += 1

blocos.append((inicio, altura))

# ==========================================
# CALCULAR ALTURA FINAL
# ==========================================

altura_final = 0

for inicio, fim in blocos:

    altura_final += fim - inicio

altura_final += ESPACO_FINAL * (len(blocos)-1)

# ==========================================
# MONTAR NOVA IMAGEM
# ==========================================

resultado = Image.new(
    "RGB",
    (largura, altura_final),
    (255,255,255)
)

y_destino = 0

for i,(inicio,fim) in enumerate(blocos):

    trecho = Image.fromarray(dados[inicio:fim])

    resultado.paste(trecho,(0,y_destino))

    y_destino += fim-inicio

    if i != len(blocos)-1:
        y_destino += ESPACO_FINAL

# ==========================================
# SALVAR
# ==========================================

resultado.save(ARQUIVO_SAIDA)

print("Concluído!")
print(f"Imagem salva em {ARQUIVO_SAIDA}")