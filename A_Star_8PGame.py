from queue import PriorityQueue

#Definição dos estados Inicial e Final (objetivo)
est_inicial = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]
est_final = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

#Definição da função heurística (Distância de Manhattan)
def heuristica(estado):
    dist = 0
    for i in range(3):
        for j in range(3):
            if estado[i][j] != 0:
                x, y = divmod(estado[i][j]-1, 3)
                dist += abs(x - i) + abs(y - j)
    return dist

#Checagem da possibilidade de solução
def soluvel_check(estado):
    flat_est = [x for linha in estado for x in linha if x != 0]
    inversoes = sum(1 for i in range(len(flat_est)) for j in range(i+1, len(flat_est)) if flat_est[i] > flat_est[j])
    return inversoes % 2 == 0

#Geração de estados
def sucessores(estado):
    x, y = next((i, j) for i, x in enumerate(estado) for j, val in enumerate(x) if val == 0)
    for i, j in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if 0 <= i < 3 and 0 <= j < 3:
            sucessor = [list(linha) for linha in estado]
            sucessor[x][y], sucessor[i][j] = sucessor[i][j], sucessor[x][y]
            yield sucessor

#Resolvedor: A*
def a_estrela(est_inicial, est_final):
    if not soluvel_check(est_inicial):
        return None
    front = PriorityQueue()
    front.put((0, est_inicial, []))
    visitado = set()
    while not front.empty():
        f, estado, caminho = front.get()
        if estado == est_final:
          print("Estado (objetivo) => f(n) = %d, g(n) = %d, h(n) = %d:\n%s\n" % (g+h, g, h, "\n".join(str(linha) for linha in estado)))
          return caminho + [estado]
        visitado.add(tuple(map(tuple, estado)))
        g = len(caminho)
        h = heuristica(estado)
        print("Estado (melhor nó na fronteira)=> f(n) = %d, g(n) = %d, h(n) = %d:\n%s\n" % (g+h, g, h, "\n".join(str(linha) for linha in estado)))
        for sucessor in sucessores(estado):
            if tuple(map(tuple, sucessor)) not in visitado:
                h_sucessor = heuristica(sucessor)
                front.put((g + h_sucessor, sucessor, caminho + [estado]))
    return None

#Execução do A* e exibição da solução
solucao = a_estrela(est_inicial, est_final)
if solucao is None:
    print("Não é possível encontrar uma solução para esse jogo.")
else:
    print("Solução encontrada:\n")
    for estado in solucao:
        print("\n".join(str(linha) for linha in estado))
        print()
print("O custo final da solução foi: g(n) %d + h(n) %d = f(n) %d" % (len(solucao)-1, heuristica(solucao[-1]), len(solucao)-1 + heuristica(solucao[-1])))
