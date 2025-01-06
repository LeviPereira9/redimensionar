def carregar_imagem(caminho):
    with open(caminho, "rb") as f:
        cabecalho = f.read(54)
        largura = int.from_bytes(cabecalho[18:22], 'little')
        altura = int.from_bytes(cabecalho[22:26], 'little')
        f.seek(54)
        pixels = list(f.read())
    return largura, altura, pixels

def salvar_imagem(caminho, largura, altura, pixels):
    tamanho_imagem = largura * altura * 3
    cabecalho = b"BM" + (54 + tamanho_imagem).to_bytes(4, 'little') + b"\x00\x00\x00\x00" + b"6\x00\x00\x00" + b"(\x00\x00\x00"
    cabecalho += largura.to_bytes(4, 'little') + altura.to_bytes(4, 'little') + b"\x01\x00\x18\x00" + b"\x00\x00\x00\x00" + tamanho_imagem.to_bytes(4, 'little')
    cabecalho += b"\x13\x0B\x00\x00\x13\x0B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    with open(caminho, "wb") as f:
        f.write(cabecalho + bytes(pixels))

def tons_de_cinza(largura, altura, pixels):
    novos_pixels = []
    for i in range(0, len(pixels), 3):
        azul, verde, vermelho = pixels[i], pixels[i+1], pixels[i+2]
        cinza = (vermelho + verde + azul) // 3
        novos_pixels.extend([cinza, cinza, cinza])
    return novos_pixels

def preto_e_branco(largura, altura, pixels, limiar=128):
    novos_pixels = []
    for i in range(0, len(pixels), 3):
        azul, verde, vermelho = pixels[i], pixels[i+1], pixels[i+2]
        cinza = (vermelho + verde + azul) // 3
        valor = 255 if cinza >= limiar else 0
        novos_pixels.extend([valor, valor, valor])
    return novos_pixels

caminho_original = "img/src/imagem.bmp"
caminho_cinza = "img/dist/imagem_cinza.bmp"
caminho_pb = "img/dist/imagem_pb.bmp"

largura, altura, pixels = carregar_imagem(caminho_original)
pixels_cinza = tons_de_cinza(largura, altura, pixels)
pixels_pb = preto_e_branco(largura, altura, pixels)
salvar_imagem(caminho_cinza, largura, altura, pixels_cinza)
salvar_imagem(caminho_pb, largura, altura, pixels_pb)
