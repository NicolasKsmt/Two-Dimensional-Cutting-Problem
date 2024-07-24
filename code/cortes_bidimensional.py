import matplotlib.pyplot as plt
import numpy as np
import random
import math
import os
import time

def ler_itens_de_csv(instancia):
    itens = []
    try:
        with open(instancia, "r") as arquivo:
            for linha in arquivo:
                if linha.strip():
                    try:
                        altura, largura = linha.strip().split(",")
                        itens.append((int(altura), int(largura)))
                    except ValueError:
                        print(f"ERRO LINHA: {linha.strip()}")
    except FileNotFoundError:
        print(f"Arquivo {instancia} não encontrado.")
    return itens

def contruir_contador(arquivo_contador):
    try:
        with open(arquivo_contador, "r") as arquivo:
            return int(arquivo.read().strip())
    except FileNotFoundError:
        return 0

def atualizar_contador(arquivo_contador, contador):
    with open(arquivo_contador, "w") as arquivo:
        arquivo.write(str(contador))

def plotar_solucao(faixas, W, cores, titulo):
    H = calcular_altura(faixas)
    fig, ax = plt.subplots()
    altura_total = 0
    for faixa in faixas:
        if not faixa:
            continue
        
        x = 0
        for item in faixa:
            rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=cores.get(tuple(item), 'gray'))
            ax.add_patch(rect)
            x += item[1]
        
        altura_total += max(item[0] for item in faixa)

    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_title(titulo)
    plt.show()

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

    plotar_solucao(faixas, W, cores, "Solução Inicial")

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
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
        return nova_faixa

    item1, item2 = random.choice(nova_faixa[faixa1]), random.choice(nova_faixa[faixa2])
    
    largura_faixa1 = calcular_largura(nova_faixa[faixa1]) - item1[1] + item2[1]
    largura_faixa2 = calcular_largura(nova_faixa[faixa2]) - item2[1] + item1[1]

    if largura_faixa1 <= W and largura_faixa2 <= W:
        nova_faixa[faixa1].remove(item1)
        nova_faixa[faixa2].remove(item2)

        nova_faixa[faixa1].append(item2)
        nova_faixa[faixa2].append(item1)

        if (not nova_faixa[faixa1] or item2[0] <= max(nova_faixa[faixa1], key=lambda x: x[0])[0]) and \
           (not nova_faixa[faixa2] or item1[0] <= max(nova_faixa[faixa2], key=lambda x: x[0])[0]):
            return nova_faixa

    return [faixa[:] for faixa in faixas]

def descida_randomica(W, faixas, cores, iteracoes, arquivo):
    start_time = time.time()

    def gerar_vizinho(faixas, W):
        novo_faixas = trocar_itens(faixas, W)
        altura = calcular_altura(novo_faixas)
        return novo_faixas, altura

    solucao_atual = faixas
    altura_atual = calcular_altura(solucao_atual)

    for _ in range(iteracoes):
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

    plotar_solucao(solucao_atual, W, cores, "Descida Randômica")

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    arquivo.write(f"Temporizador: {execution_time:.2f} ms\n")

def simulated_annealing(W, faixas, cores, temp_inicial, temp_final, alfa, iteracoes, arquivo):
    start_time = time.time()

    temp = temp_inicial
    atual_faixas = faixas
    atual_altura = calcular_altura(atual_faixas)
    melhor_faixas = faixas
    melhor_altura = atual_altura

    while temp > temp_final:
        for _ in range(iteracoes):
            nova_faixas = trocar_itens(atual_faixas, W)
            nova_altura = calcular_altura(nova_faixas)
            delta = nova_altura - atual_altura

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
    plotar_solucao(melhor_faixas, W, cores, "Simulated Annealing")

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    arquivo.write(f"Temporizador: {execution_time:.2f} ms\n")

def gerador_de_instancias(n, H, W):
    itens = [(random.randint(1, H), random.randint(1, int(W-3))) for _ in range(n)]
    return itens

def main():
    W = 50
    temp_inicial = 1000
    temp_final = 1
    alfa = 0.9
    iteracoes = 2000

    print("Escolha a origem dos itens:")
    print("1: Gerar itens aleatoriamente")
    print("2: Ler itens de um arquivo CSV")
    escolha = input("Digite o número da sua escolha (1 ou 2): ")

    if escolha == '1':
        n = random.randint(50, 100)
        itens = gerador_de_instancias(n, 10, W - 3)
    elif escolha == '2':
        inputRead = input("Digite qual o numero da instancia: ")
        itens = ler_itens_de_csv("../instancias/instancia_" + inputRead + ".csv")
        if not itens:
            print("Nenhum item carregado. Encerrando o programa.")
            return
    else:
        print("Escolha inválida. Encerrando o programa.")
        return

    arquivo_contador = "execucoes/contador.txt"

    if not os.path.exists("execucoes"):
        os.makedirs("execucoes")
    
    contador = contruir_contador(arquivo_contador)
    contador += 1
    atualizar_contador(arquivo_contador, contador)
    
    arquivo_execucoes = os.path.join("execucoes", f"execucao_{contador}.txt")
    
    with open(arquivo_execucoes, "w") as arquivo:
        arquivo.write("Lista de itens:\n")
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

if __name__ == "__main__":
    main()