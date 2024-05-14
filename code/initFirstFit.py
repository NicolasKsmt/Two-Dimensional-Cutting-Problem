import matplotlib.pyplot as plt
import numpy as np

#Peças a serem alocadas no objeto maior
itens = [(2, 3), (1, 2), (3, 1), (2, 2), (1, 1), (3, 3), (5, 2)]  #(altura, largura)
W = 5  #largura do objeto

#Restrição para que todas as peças possam ser alocadas no objeto
largura_maxima_item = max(item[1] for item in itens)
if W < largura_maxima_item:
    raise ValueError(f"A largura do objeto ({W}) é menor que a largura do item mais largo ({largura_maxima_item}).")

#Ordenar os itens em ordem decrescente de altura
itens.sort(key=lambda x: x[0], reverse=True)

#Inicializa a primeira faixa com a altura do item mais alto
faixas = [[itens[0]]]
Wdf = [W - itens[0][1]]  #largura disponível na faixa

#Aloca itens nas faixas, criando novas faixas conforme necessário
for i in range(1, len(itens)):
    for j in range(len(faixas)):
        if itens[i][1] <= Wdf[j]:  #Verifica se o item cabe na faixa
            faixas[j].append(itens[i])  #Insere o item na faixa
            Wdf[j] -= itens[i][1]  # atualiza a largura disponível na faixa
            break
    else:  #Cria uma nova faixa caso não haja mais largura disponível
        faixas.append([itens[i]])
        Wdf.append(W - itens[i][1])

#Determina a altura do objeto, somando a altura da primeira peça de cada faixa
H = sum(faixa[0][0] for faixa in faixas)

for i, faixa in enumerate(faixas):
    print(f"Faixa {i+1}:")
    for item in faixa:
        print(f"Item: altura = {item[0]}, largura = {item[1]}")
print(f"Altura total do objeto maior: {H}")

#Plotar o gráfico
fig, ax = plt.subplots()
altura_total = 0
for i, faixa in enumerate(faixas):
    #Variável x é utilizada para determinar onde cada peça deve ser alocada considerando o eixo de largura
    x = 0
    for item in faixa:
        #altura_total aqui é utilizada para determinar de qual altura a peça deve ser alocada
        rect = plt.Rectangle((x, altura_total), item[1], item[0], facecolor=np.random.rand(3,))
        ax.add_patch(rect)
        x += item[1]
    altura_total += faixa[0][0]
ax.set_xlim(0, W)
ax.set_ylim(0, H)
plt.show()
