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

def encontrar_faixa_cinza(imagem, cor_alvo, tolerancia=20, altura_faixa=13):
    """
    Encontra posições onde há uma faixa cinza horizontal.
    """
    largura, altura = imagem.size
    pixels = imagem.load()

    posicoes_corte = []

    # MODANÇA: Varre o centro horizontal da página inteira (evita bordas vazias ou margens)
    x_verificacao = largura // 2

    y = 0
    while y < altura - altura_faixa:

        faixa_encontrada = True

        for dy in range(altura_faixa):
            # MUDANÇA: Substituído 'largura - 2' pela coordenada x centralizada
            pixel = pixels[x_verificacao, y + dy]

            if len(pixel) == 4:
                r, g, b, a = pixel
            else:
                r, g, b = pixel[:3]

            if (abs(r - cor_alvo[0]) > tolerancia or
                abs(g - cor_alvo[1]) > tolerancia or
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break

        if faixa_encontrada:
            # corta 15 pixels acima do início da faixa
            posicao_corte = max(0, y - 30)
            posicoes_corte.append(posicao_corte)

            print(f"Faixa cinza encontrada em y={y}, cortando em y={posicao_corte}")
            y += altura_faixa
        else:
            y += 1

    return posicoes_corte


def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size

    print(f"Imagem carregada: {largura}x{altura} pixels")

    posicoes_corte = encontrar_faixa_cinza(imagem, cor_alvo)

    if not posicoes_corte:
        print("Nenhuma faixa cinza encontrada!")
        return

    print(f"Encontradas {len(posicoes_corte)} faixas cinza")

    os.makedirs(pasta_saida, exist_ok=True)

    posicao_anterior = 0

    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue

        area_corte = (
            0,
            posicao_anterior,
            largura,
            posicao_corte
        )

        secao = imagem.crop(area_corte)
        caminho = os.path.join(
            pasta_saida,
            f"parte_{i+1:03d}.png"
        )
        secao.save(caminho)
        print(f"Salvo: {caminho}")

        # pula a faixa cinza (13 px)
        posicao_anterior = posicao_corte + 13

    if posicao_anterior < altura:
        area_corte = (
            0,
            posicao_anterior,
            largura,
            altura
        )

        secao = imagem.crop(area_corte)
        caminho = os.path.join(
            pasta_saida,
            f"parte_{len(posicoes_corte)+1:03d}.png"
        )
        secao.save(caminho)
        print(f"Salvo: {caminho}")


if __name__ == "__main__":
    # MUDANÇA: Nomes atualizados para corresponder ao passo de páginas inteiras
    caminho_imagem = "inteiras_concatenadas_verticalmente.png"
    pasta_saida = "questoes_paginas_inteiras"

    # Coloque aqui a cor medida no GIMP da faixa cinza.
    cor_do_padrao = converter_cor_gimp_para_rgb(79, 79, 79)

    print(f"Cor convertida: RGB{cor_do_padrao}")

    dividir_imagem_por_faixas(
        caminho_imagem,
        pasta_saida,
        cor_do_padrao
    )

    print("Divisão concluída!")

    print(f"Encontradas {len(posicoes_corte)} faixas cinza")

    os.makedirs(pasta_saida, exist_ok=True)

    posicao_anterior = 0

    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue

        area_corte = (
            0,
            posicao_anterior,
            largura,
            posicao_corte
        )

        secao = imagem.crop(area_corte)
        caminho = os.path.join(
            pasta_saida,
            f"parte_{i+1:03d}.png"
        )
        secao.save(caminho)
        print(f"Salvo: {caminho}")

        # pula a faixa cinza (13 px)
        posicao_anterior = posicao_corte + 13

    if posicao_anterior < altura:
        area_corte = (
            0,
            posicao_anterior,
            largura,
            altura
        )

        secao = imagem.crop(area_corte)
        caminho = os.path.join(
            pasta_saida,
            f"parte_{len(posicoes_corte)+1:03d}.png"
        )
        secao.save(caminho)
        print(f"Salvo: {caminho}")


if __name__ == "__main__":
    # MUDANÇA: Atualize o nome do arquivo de entrada e da pasta de saída se necessário
    caminho_imagem = "inteiras_concatenadas_verticalmente.png"
    pasta_saida = "inteiras" 

    # Coloque aqui a cor medida no GIMP da faixa cinza.
    cor_do_padrao = converter_cor_gimp_para_rgb(79, 79, 79)

    print(f"Cor convertida: RGB{cor_do_padrao}")

    dividir_imagem_por_faixas(
        caminho_imagem,
        pasta_saida,
        cor_do_padrao
    )

    print("Divisão concluída!")
