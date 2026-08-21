from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_cinza(imagem, cor_alvo, tolerancia=25, altura_faixa=3, distancia_minima=100):
    """
    Encontra posições onde há uma faixa horizontal cortando a largura da imagem.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    y = 0
    
    while y < altura - altura_faixa:
        # Conta quantos pixels ao longo da linha correspondem à cor da faixa
        pixels_corretos = 0
        amostras_x = range(10, largura - 10, 2)  # Percorre a largura pulando de 2 em 2 px para alta performance
        
        for x in amostras_x:
            pixel = pixels[x, y]
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
                
            # Verifica se a cor bate com a faixa desejada
            if (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia):
                pixels_corretos += 1
        
        # Se mais de 60% dos pixels da linha forem da cor alvo, confirmamos que é o divisor de questão
        proporcao = pixels_corretos / len(amostras_x)
        if proporcao >= 0.6:
            posicao_corte = y - 2  # Corta 2 pixels acima do padrão
            if posicao_corte < 0:
                posicao_corte = 0
                
            # Verifica se está respeitando o tamanho mínimo de uma questão (evita múltiplos cortes)
            if not posicoes_corte or (posicao_corte - posicoes_corte[-1]) >= distancia_minima:
                posicoes_corte.append(posicao_corte)
                print(f"Faixa de questão confirmada em y={y} ({int(proporcao*100)}% de correspondência), corte em y={posicao_corte}")
                y += distancia_minima  # Salta a altura mínima de uma questão para evitar falsos positivos próximos
                continue
        
        y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente cortando ANTES das faixas
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_cinza(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhuma faixa de divisão encontrada na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} questões para divisão")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Salva a última questão
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"
    pasta_saida = "questoes_divididas"
    
    # Faixa cinza correspondente no GIMP
    cor_do_padrao = converter_cor_gimp_para_rgb(83.1, 83.1, 83.1)
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão concluída com sucesso!")