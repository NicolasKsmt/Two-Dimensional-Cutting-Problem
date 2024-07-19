import matplotlib.pyplot as plt
import numpy as np
import random
import os

# Função para gerenciar o contador de execuções
def contruir_contador(arquivo_contador):
    try:
        with open(arquivo_contador, "r") as arquivo:
            contador = int(arquivo.read().strip())
    except FileNotFoundError:
        contador = 0
    return contador

def atualizar_contador(arquivo_contador, contador):
    with open(arquivo_contador, "w") as arquivo:
        arquivo.write(str(contador))

def solucao_inicial(itens, W, arquivo):
    largura_maxima_item = max(item[1] for item in itens)
    if W < largura_maxima_item:
        raise ValueError(f"A largura do objeto ({W}) é menor que a largura do item mais largo ({largura_maxima_item}).")

    itens.sort(key=lambda x: x[0], reverse=True)

    faixas = [[itens[0]]]
    Wdf = [W - itens[0][1]]

    cores = {tuple(itens[0]): np.random.rand(3, )}

    for i in range(1, len(itens)):
        for j in range(len(faixas)):
            if itens[i][1] <= Wdf[j]:
                faixas[j].append(itens[i])
                Wdf[j] -= itens[i][1]
                cores[tuple(itens[i])] = np.random.rand(3, )
                break
        else:
            faixas.append([itens[i]])
            Wdf.append(W - itens[i][1])
            cores[tuple(itens[i])] = np.random.rand(3, )

    H = sum(faixa[0][0] for faixa in faixas)

    for i, faixa in enumerate(faixas):
        arquivo.write(f"Faixa {i+1}:\n")
        for item in faixa:
            arquivo.write(f"Item: altura = {item[0]}, largura = {item[1]}\n")
    arquivo.write(f"Altura total do objeto maior: {H}\n")

    fig, ax = plt.subplots()
    altura_total = 0
    for i, faixa in enumerate(faixas):
        x = 0
        for item in faixa:
            rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=cores[tuple(item)])
            ax.add_patch(rect)
            x += item[1]
        altura_total += faixa[0][0]
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    plt.show()
    return faixas, Wdf, cores

def descida_randomica(itens, W, faixas, Wdf, cores, arquivo):
    def calcular_altura_total(faixas):
        return sum(faixa[0][0] for faixa in faixas)

    def gerar_vizinho(faixas, Wdf):
        novo_faixas = [faixa[:] for faixa in faixas]
        novo_Wdf = Wdf[:]

        faixa_idx = random.randint(0, len(novo_faixas) - 1)

        if len(novo_faixas[faixa_idx]) > 1:
            item1_idx, item2_idx = random.sample(range(len(novo_faixas[faixa_idx])), 2)
            novo_faixas[faixa_idx][item1_idx], novo_faixas[faixa_idx][item2_idx] = novo_faixas[faixa_idx][item2_idx], novo_faixas[faixa_idx][item1_idx]

            largura_usada = sum(item[1] for item in novo_faixas[faixa_idx])
            if largura_usada <= W:
                return novo_faixas, novo_Wdf

        return faixas, Wdf

    num_iteracoes = 1000

    solucao_atual = faixas
    Wdf_atual = Wdf
    altura_atual = calcular_altura_total(solucao_atual)

    for _ in range(num_iteracoes):
        solucao_vizinha, Wdf_vizinha = gerar_vizinho(solucao_atual, Wdf_atual)
        altura_vizinha = calcular_altura_total(solucao_vizinha)
        if altura_vizinha < altura_atual:
            solucao_atual = solucao_vizinha
            Wdf_atual = Wdf_vizinha
            altura_atual = altura_vizinha

    arquivo.write("Solução final:\n")
    for i, faixa in enumerate(solucao_atual):
        arquivo.write(f"Faixa {i+1}:\n")
        for item in faixa:
            arquivo.write(f"Item: altura = {item[0]}, largura = {item[1]}\n")
    arquivo.write(f"Altura total do objeto maior: {altura_atual}\n")

    fig, ax = plt.subplots()
    altura_total = 0
    for i, faixa in enumerate(solucao_atual):
        x = 0
        for item in faixa:
            rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=cores[tuple(item)])
            ax.add_patch(rect)
            x += item[1]
        altura_total += faixa[0][0]
    ax.set_xlim(0, W)
    ax.set_ylim(0, altura_atual)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def gerador_de_instancias(n, H, W):
    itens = [(random.randint(1, H), random.randint(1, W)) for _ in range(n)]
    return itens

def main():
    W = 7
    n = random.randint(5, 10)
    itens = gerador_de_instancias(n, 10, W)

    # Nome do arquivo para armazenar o contador
    arquivo_contador = "execucoes/contador.txt"

    # Criar pasta contador caso nao haja
    if not os.path.exists("execucoes"):
        os.makedirs("execucoes")
    
    # Obter o contador atual e atualizar
    contador = contruir_contador(arquivo_contador)
    contador += 1
    atualizar_contador(arquivo_contador, contador)
    
    # Pasta para armazenar os arquivos de execução
    if not os.path.exists("execucoes"):
        os.makedirs("execucoes")

    # Gerar o nome do arquivo com base no contador
    nome_arquivo = os.path.join("execucoes", f"execucao_{contador}.txt")
    
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write("Lista de itens gerados:\n")
        for item in itens:
            arquivo.write(f"Item: altura = {item[0]}, largura = {item[1]}\n")
        arquivo.write("\n==============================================\n")
        
        faixas, Wdf, cores = solucao_inicial(itens, W, arquivo)
        arquivo.write("\n==============================================\n")
        descida_randomica(itens, W, faixas, Wdf, cores, arquivo)

main()