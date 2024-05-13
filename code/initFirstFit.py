import matplotlib.pyplot as plt
import numpy as np

# Suponha que temos os seguintes itens e objeto
itens = [(2, 3), (1, 2), (3, 1), (2, 2), (1, 1)]  # (altura, largura)
W = 6  # largura do objeto


#Restrição para que todas as peças possam ser alocadas no objeto
largura_maxima_item = max(item[1] for item in itens)
if W < largura_maxima_item:
    raise ValueError(f"A largura do objeto ({W}) é menor que a largura do item mais largo ({largura_maxima_item}).")

# Ordenar os itens em ordem decrescente de altura
itens.sort(key=lambda x: x[0], reverse=True)

# Inicializar a primeira faixa com a altura do item mais alto
faixas = [[itens[0]]]
Wdf = [W - itens[0][1]]  # largura disponível na faixa

# Alocar itens nas faixas seguindo as regras fornecidas, criando novas faixas conforme necessário
for i in range(1, len(itens)):
    for j in range(len(faixas)):
        if itens[i][1] <= Wdf[j]:  # se o item cabe na faixa
            faixas[j].append(itens[i])  # insere o item na faixa
            Wdf[j] -= itens[i][1]  # atualiza a largura disponível na faixa
            break
    else:  # se não encontramos uma faixa onde o item cabe, criamos uma nova faixa
        faixas.append([itens[i]])
        Wdf.append(W - itens[i][1])

# Ajustar a altura da peça original com base na altura da primeira peça de cada faixa
H = sum(faixa[0][0] for faixa in faixas)

print("Faixas:")
for i, faixa in enumerate(faixas):
    print(f"Faixa {i+1}:")
    for item in faixa:
        print(f"  Item: altura = {item[0]}, largura = {item[1]}")
print(f"Altura total do objeto maior: {H}")

# Plotar o gráfico
fig, ax = plt.subplots()
altura_acumulada = 0
for i, faixa in enumerate(faixas):
    x = 0
    for item in faixa:
        rect = plt.Rectangle((x, altura_acumulada), item[1], item[0], facecolor=np.random.rand(3,))
        ax.add_patch(rect)
        x += item[1]
    altura_acumulada += faixa[0][0]
ax.set_xlim(0, W)
ax.set_ylim(0, H)
plt.show()
