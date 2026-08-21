from PIL import Image
import numpy as np

def cortar_por_linhas_cinzas(caminho_imagem, tolerancia_cinza=50, altura_minima_secao=20):
    # Carrega a imagem e converte para escala de cinza
    img = Image.open(caminho_imagem)
    img_gray = img.convert('L')
    matriz = np.array(img_gray)
    
    largura, altura = img.size
    
    # Identifica linhas onde a média dos pixels indica uma linha divisória escura/cinza
    # Ajuste o valor conforme a intensidade da linha cinza
    medias_linhas = np.mean(matriz, axis=1)
    
    # Encontra os índices das linhas divisórias
    linhas_corte = [0]
    for y in range(1, altura - 1):
        # Se a linha for significativamente mais escura que o fundo
        if medias_linhas[y] < tolerancia_cinza:
            if y - linhas_corte[-1] > altura_minima_secao:
                linhas_corte.append(y)
                
    linhas_corte.append(altura)
    
    # Realiza os cortes e salva cada questão
    imagens_cortadas = []
    i = 1
    for idx in range(len(linhas_corte) - 1):
        y_inicio = linhas_corte[idx]
        y_fim = linhas_corte[idx + 1]
        
        # Ignora seções muito pequenas
        if y_fim - y_inicio < altura_minima_secao:
            continue
            
        caixa = (0, y_inicio, largura, y_fim)
        questao = img.crop(caixa)
        nome_arquivo = f"questao_{i}.png"
        questao.save(nome_arquivo)
        imagens_cortadas.append(nome_arquivo)
        print(f"Salvo: {nome_arquivo}")
        i += 1

# Substitua pelo nome do seu arquivo de imagem
cortar_por_linhas_cinzas("colunas_concatenadas_verticalmente.png")