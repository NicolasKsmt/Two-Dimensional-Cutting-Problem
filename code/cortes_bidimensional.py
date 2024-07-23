import matplotlib.pyplot as plt
import numpy as np
import random
import math
import os
import time

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
    start_time = time.time()

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
    ax.set_title("Solução Inicial")
    plt.show()

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convertendo para milissegundos
    arquivo.write(f"Temporizador: {execution_time:.2f} ms\n")

    return faixas, Wdf, cores

def calcular_altura(faixas):
    return sum(max(faixa, key=lambda x: x[0])[0] if faixa else 0 for faixa in faixas)

def calcular_largura(faixa):
    return sum(item[1] for item in faixa)

def trocar_itens(faixas, W):
    nova_faixa = [faixa[:] for faixa in faixas]
    faixa1, faixa2 = random.sample(range(len(nova_faixa)), 2)

    if not nova_faixa[faixa1] or not nova_faixa[faixa2]:
        return nova_faixa  # Se uma das faixas estiver vazia, não faz nada
    
    item1, item2 = random.choice(nova_faixa[faixa1]), random.choice(nova_faixa[faixa2])
    
    largura_faixa1 = calcular_largura(nova_faixa[faixa1]) - item1[1] + item2[1]
    largura_faixa2 = calcular_largura(nova_faixa[faixa2]) - item2[1] + item1[1]

    # Verifica se a troca é válida em termos de largura
    if largura_faixa1 <= W and largura_faixa2 <= W:
        # Remove os itens das faixas originais
        nova_faixa[faixa1].remove(item1)
        nova_faixa[faixa2].remove(item2)

        # Adiciona os itens nas novas faixas
        nova_faixa[faixa1].append(item2)
        nova_faixa[faixa2].append(item1)

        # Verifica se a troca respeita a ordem de alturas
        if (not nova_faixa[faixa1] or item2[0] <= max(nova_faixa[faixa1], key=lambda x: x[0])[0]) and \
           (not nova_faixa[faixa2] or item1[0] <= max(nova_faixa[faixa2], key=lambda x: x[0])[0]):
            return nova_faixa

    # Reverte a troca se a largura não for válida
    return [faixa[:] for faixa in faixas]

def descida_randomica(W, faixas, cores, iteracoes, arquivo):
    start_time = time.time()

    def calcular_altura(faixas):
        return sum(max(faixa, key=lambda x: x[0])[0] if faixa else 0 for faixa in faixas)

    def plotar_solucao(faixas, W, cores):
        H = calcular_altura(faixas)
        fig, ax = plt.subplots()
        altura_total = 0
        for faixa in faixas:
            if not faixa:
                continue  # Ignorar faixas vazias
            
            x = 0
            for item in faixa:
                rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=cores.get(tuple(item), 'gray'))
                ax.add_patch(rect)
                x += item[1]
            
            altura_total += max(item[0] for item in faixa)  # Somar a altura máxima da faixa

        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.set_title("Descida Randômica")
        plt.show()

    def gerar_vizinho(faixas, W):
        novo_faixas = trocar_itens(faixas, W)
        altura = calcular_altura(novo_faixas)
        return novo_faixas, altura

    solucao_atual = faixas
    altura_atual = calcular_altura(solucao_atual)

    for i in range(iteracoes):
        solucao_vizinha, altura_vizinha = gerar_vizinho(solucao_atual, W)
        if altura_vizinha <= altura_atual:
            solucao_atual = solucao_vizinha
            altura_atual = altura_vizinha

    arquivo.write("\n")
    for i, faixa in enumerate(solucao_atual):
        arquivo.write(f"Faixa {i+1}:\n")
        for item in faixa:
            arquivo.write(f"Item: altura = {item[0]}, largura = {item[1]}\n")
    arquivo.write(f"Altura total do objeto maior: {altura_atual}\n")

    plotar_solucao(solucao_atual, W, cores)

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convertendo para milissegundos
    arquivo.write(f"Temporizador: {execution_time:.2f} ms\n")

def simulated_annealing(W, faixas, cores, temp_inicial, temp_final, alfa, iteracoes, arquivo):
    start_time = time.time()

    temp = temp_inicial
    atual_faixas = faixas
    atual_altura = calcular_altura(atual_faixas)
    melhor_faixas = faixas
    melhor_altura = atual_altura

    def plotar_solucao(faixas, W, cores):
        H = calcular_altura(faixas)
        fig, ax = plt.subplots()
        altura_total = 0
        for faixa in faixas:
            if not faixa:
                continue  # Ignorar faixas vazias
            
            x = 0
            for item in faixa:
                rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=cores.get(tuple(item), 'gray'))
                ax.add_patch(rect)
                x += item[1]
            
            altura_total += max(item[0] for item in faixa)  # Somar a altura máxima da faixa

        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.set_title("Simulated Annealing")
        plt.show()

    while temp > temp_final:
        for _ in range(iteracoes):
            nova_faixas = trocar_itens(atual_faixas, W)
            nova_altura = calcular_altura(nova_faixas)
            delta = nova_altura - atual_altura

            # Adicionando mensagens de debug
            #print(f"Temp: {temp}, Atual Altura: {atual_altura}, Nova Altura: {nova_altura}, Delta: {delta}")

            if delta < 0 or random.random() < math.exp(-delta / temp):
                atual_faixas = nova_faixas
                atual_altura = nova_altura
                if nova_altura <= melhor_altura:
                    melhor_faixas = nova_faixas
                    melhor_altura = nova_altura

        temp *= alfa

    arquivo.write("\n")
    for i, faixa in enumerate(melhor_faixas):
        arquivo.write(f"Faixa {i+1}:\n")
        for item in faixa:
            arquivo.write(f"Item: altura = {item[0]}, largura = {item[1]}\n")
    arquivo.write(f"Altura total do objeto maior: {melhor_altura}\n")
    plotar_solucao(melhor_faixas, W, cores)

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convertendo para milissegundos
    arquivo.write(f"Temporizador: {execution_time:.2f} ms\n")

def gerador_de_instancias(n, H, W):
    itens = [(random.randint(1, H), random.randint(1, int(W/2))) for _ in range(n)]
    return itens

def main():
    W = 50
    temp_inicial = 1000
    temp_final = 1
    alfa = 0.9
    iteracoes = 1000
    n = random.randint(15, 50)
    itens = gerador_de_instancias(n, 10, W - 3)

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
        arquivo.write("\nSolucao Inicial:\n\n")
        faixas, Wdf, cores = solucao_inicial(itens, W, arquivo)
        arquivo.write("\n==============================================\n")
        arquivo.write("\nSimulated Annealing:\n")
        simulated_annealing(W, faixas, cores, temp_inicial, temp_final, alfa, iteracoes, arquivo)
        arquivo.write("\n==============================================\n")
        arquivo.write("\nDescida Randomica:\n")
        descida_randomica(W, faixas, cores, iteracoes, arquivo)

main()