import matplotlib.pyplot as plt
import numpy as np
import random

def solucao_inicial(itens, W):
    # Restrição para que todas as peças possam ser alocadas no objeto
    largura_maxima_item = max(item[1] for item in itens)
    if W < largura_maxima_item:
        raise ValueError(f"A largura do objeto ({W}) é menor que a largura do item mais largo ({largura_maxima_item}).")

    # Ordenar os itens em ordem decrescente de altura
    itens.sort(key=lambda x: x[0], reverse=True)

    # Inicializa a primeira faixa com a altura do item mais alto
    faixas = [[itens[0]]]
    Wdf = [W - itens[0][1]]  # largura disponível na faixa

    # Dicionário para armazenar as cores dos itens
    cores = {tuple(itens[0]): np.random.rand(3, )}

    # Aloca itens nas faixas, criando novas faixas conforme necessário
    for i in range(1, len(itens)):
        for j in range(len(faixas)):
            if itens[i][1] <= Wdf[j]:  # Verifica se o item cabe na faixa
                faixas[j].append(itens[i])  # Insere o item na faixa
                Wdf[j] -= itens[i][1]  # atualiza a largura disponível na faixa
                cores[tuple(itens[i])] = np.random.rand(3, )  # armazena a cor do item
                break
        else:  # Cria uma nova faixa caso não haja mais largura disponível
            faixas.append([itens[i]])
            Wdf.append(W - itens[i][1])
            cores[tuple(itens[i])] = np.random.rand(3, )  # armazena a cor do item

    # Determina a altura do objeto, somando a altura da primeira peça de cada faixa
    H = sum(faixa[0][0] for faixa in faixas)

    for i, faixa in enumerate(faixas):
        print(f"Faixa {i+1}:")
        for item in faixa:
            print(f"Item: altura = {item[0]}, largura = {item[1]}")
    print(f"Altura total do objeto maior: {H}")

    # Plotar o gráfico
    fig, ax = plt.subplots()
    altura_total = 0
    for i, faixa in enumerate(faixas):
        # Variável x é utilizada para determinar onde cada peça deve ser alocada considerando o eixo de largura
        x = 0
        for item in faixa:
            # altura_total aqui é utilizada para determinar de qual altura a peça deve ser alocada
            rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=cores[tuple(item)])
            ax.add_patch(rect)
            x += item[1]
        altura_total += faixa[0][0]
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    plt.show()
    return faixas, Wdf, cores

def descida_randomica(itens, W, faixas, Wdf, cores):
    def calcular_altura_total(faixas):
        return sum(faixa[0][0] for faixa in faixas)

    # Função para gerar uma solução vizinha trocando dois itens dentro da mesma faixa
    def gerar_vizinho(faixas, Wdf):
        # Copiar a solução atual
        novo_faixas = [faixa[:] for faixa in faixas]
        novo_Wdf = Wdf[:]

        # Selecionar uma faixa aleatoriamente
        faixa_idx = random.randint(0, len(novo_faixas) - 1)

        if len(novo_faixas[faixa_idx]) > 1:
            # Selecionar dois itens aleatórios dentro da mesma faixa
            item1_idx, item2_idx = random.sample(range(len(novo_faixas[faixa_idx])), 2)

            # Trocar os itens dentro da faixa
            novo_faixas[faixa_idx][item1_idx], novo_faixas[faixa_idx][item2_idx] = novo_faixas[faixa_idx][item2_idx], novo_faixas[faixa_idx][item1_idx]

            # Verificar se a troca não causa sobreposição na largura disponível
            largura_usada = sum(item[1] for item in novo_faixas[faixa_idx])
            if largura_usada <= W:
                return novo_faixas, novo_Wdf

        return faixas, Wdf

    # Parâmetros da busca local
    num_iteracoes = 1000

    # Solução inicial
    solucao_atual = faixas
    Wdf_atual = Wdf
    altura_atual = calcular_altura_total(solucao_atual)

    # Execução da busca local por descida randômica
    for _ in range(num_iteracoes):
        solucao_vizinha, Wdf_vizinha = gerar_vizinho(solucao_atual, Wdf_atual)
        largura_valida = all(sum(item[1] for item in faixa) <= W for faixa in solucao_vizinha)
        if largura_valida:
            altura_vizinha = calcular_altura_total(solucao_vizinha)
            if altura_vizinha < altura_atual:
                solucao_atual = solucao_vizinha
                Wdf_atual = Wdf_vizinha
                altura_atual = altura_vizinha

    # Resultado final
    print("Solução final:")
    for i, faixa in enumerate(solucao_atual):
        print(f"Faixa {i+1}:")
        for item in faixa:
            print(f"Item: altura = {item[0]}, largura = {item[1]}")
    print(f"Altura total do objeto maior: {altura_atual}")

    # Plotar o gráfico da solução final com as cores originais
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

def main():
    # Peças a serem alocadas no objeto maior
    itens = [(2, 3), (1, 2), (3, 1), (2, 2), (1, 1), (3, 3), (5, 2)]  # (altura, largura)
    W = 5  # largura do objeto
    faixas, Wdf, cores = solucao_inicial(itens, W)
    descida_randomica(itens, W, faixas, Wdf, cores)

main()