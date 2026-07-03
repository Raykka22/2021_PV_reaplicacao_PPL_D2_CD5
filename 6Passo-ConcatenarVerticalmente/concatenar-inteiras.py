"""
Propósito: concatenas verticalmente as imagens de cada pasta vinda do passo 5
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "divididas-sem-bordas-do-meio" do passo 5 para essa pasta do passo 6
OBS2: não compensa concatenar as páginas inteiras. Tenha isso em mente para o passo 7. Concatene apenas as colunas.
"""

from PIL import Image
import os
import re

pasta_imagens = "inteiras"
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

# FUNÇÃO MODIFICADA: Agora busca apenas o número da página e ordena por ele
def get_sort_key(nome_arquivo):
    # Busca o número após 'pagina_enem_' e antes do '.png' (ou de outro padrão numérico)
    numero = int(re.search(r'pagina_enem_(\d+)', nome_arquivo).group(1))
    return numero

# Pegar e ordenar as imagens corretamente
arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('.png')]
arquivos.sort(key=get_sort_key)

# Abrir todas as imagens na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")  # Para verificar a ordem

# Encontrar a largura máxima
largura_max = max(img.width for img in imagens)

# Concatenar verticalmente
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new('RGB', (largura_max, altura_total))

y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

# Salvar
imagem_final.save(os.path.join(pasta_saida, 'inteiras_concatenadas_verticalmente.png'))
print("Imagens concatenadas na ordem correta!")
print(f"Ordem dos arquivos: {arquivos}")