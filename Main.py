from source.GeneticAlgorithm.Individuo import individuo
import numpy as np

poblacion = []
herederos = []


def GenerarPoblacion(genotipo, cantidad, mutacionProbability):
    for i in range(cantidad):
        poblacion.append(individuo(genotipo, mutacionProbability))


def BinaryToDecimal(binary):
    value = 0
    j = len(binary) - 1
    i = 0
    for v in range(j, -1, -1):
        value += pow(2.0, i) * (binary[v])
        i += 1
    return value


def Evaluacion(poblat, pens):
    print("Evaluacion de individuos")
    for ind in poblat:
        x = BinaryToDecimal(ind.genotipo[:4])
        y = BinaryToDecimal(ind.genotipo[4:8])
        z = BinaryToDecimal(ind.genotipo[8:])
        grade = (5 * x) + (8 * y) + (23 * z)
        evaluacion = (abs(pens - grade)/pens)
        if evaluacion > 1:
            evaluacion = 0
        else :
            evaluacion = 1 - evaluacion
        ftp = x + y + z
        ind.calificacion = evaluacion
        ind.plumas5 = x
        ind.plumas8 = y
        ind.plumas23 = z
        ind.fenotipo = ftp
        print('Evaluacion del individuo {}, x = {}, y = {}, z = {}, evaluacion = {}, fenotipo = {}'.format(ind.genotipo, x, y, z, evaluacion, ftp))


def Seleccion(poblat, pens):
    print("<Seleccion de individuos>")
    totalR = 0
    totalF = 0
    Evaluacion(poblat, pens)
    for ind in poblat:
        totalR += ind.calificacion
        totalF += ind.fenotipo
    if totalR != 0:
        for ind in poblat:
            rm = ind.calificacion / totalR
            rf = ind.fenotipo / totalF
            ind.relacionMutua = rm
            ind.relacionFenotipica = rf
            print('Relacion Mutua del Individuo {} es = {} con una Relacion Fenotipica de {}'.format(ind.genotipo, rm, rf))
    else:
        for ind in poblat:
            ind.relacionMutua = 0
            ind.relacionFenotipica = 0
        print('Todos los individuos fracasaron')


def Mutar(poblat):
    for ind in poblat:
        ind.Mutacion()


def Cruzar(indA, indB, percentage, herd):
    i = int(percentage * len(indA.genotipo))
    genA = indA.genotipo[:i]
    genB = indB.genotipo[i:]
    gen = np.concatenate((genA, genB), axis=0)
    new = individuo(len(indA.genotipo), indA.mutacionProbability)
    new.newcomer(gen)
    herd.append(new)
    genA = indA.genotipo[i:]
    genB = indB.genotipo[:i]
    gen = np.concatenate((genB, genA), axis=0)
    new2 = individuo(len(indB.genotipo), indB.mutacionProbability)
    new2.newcomer(gen)
    herd.append(new2)
    print('Nuevos individuos nacidos de {} y {}. Los individuos son {} y {}'.format(indA.genotipo, indB.genotipo,
                                                                                    new.genotipo, new2.genotipo))


def Reinsertion(poblat, herd, elit):
    print("Reinsercion")
    for i in range(int(elit * len(poblat))):
        tmp = poblat[0]
        for ind in poblat:
            if tmp.relacionMutua < ind.relacionMutua:
                tmp = ind
            elif tmp.relacionMutua == ind.relacionMutua and tmp.relacionFenotipica > ind.relacionFenotipica:
                tmp = ind
        herd.append(tmp)
        poblat.remove(tmp)
        print(
            'El individuo {} destaco de los demas con una relacion mutua de {}'.format(tmp.genotipo, tmp.relacionMutua))
    poblat.clear()
    for ind in herd:
        poblat.append(ind)
    herd.clear()


def Elite(poblat):
    tmp = poblat[0]
    for ind in poblat:
        if tmp.relacionMutua < ind.relacionMutua:
            tmp = ind
        elif tmp.relacionMutua == ind.relacionMutua and tmp.relacionFenotipica > ind.relacionFenotipica:
            tmp = ind
    print('Individuo con mejor resultado fue {} con calificacion de {} con {} paquetes de 5, '
          '{} paquetes de 8 y {} paquetes de 23'.format(tmp.genotipo, tmp.calificacion, tmp.plumas5, tmp.plumas8, tmp.plumas23))


gentiCodeLen = 12
population = 10
mutacionPercentage = .2
elitism = .4
geneticMerch = .5
percentageNewcomers = .6
generaciones = 1000
pens = 53

GenerarPoblacion(gentiCodeLen, population, mutacionPercentage)
for i in range(generaciones):
    print("<---------------------------------------------------------------------------------------->")
    print('Generacion {}'.format(i))
    print()
    for ind in poblacion:
        print(ind.genotipo)
    print()
    Seleccion(poblacion, pens)
    print()
    while len(herederos) < (len(poblacion) * percentageNewcomers):
        indA = poblacion[np.random.randint(0, len(poblacion) - 1)]
        indB = poblacion[np.random.randint(0, len(poblacion) - 1)]
        Cruzar(indA, indB, geneticMerch, herederos)
    print()
    Reinsertion(poblacion, herederos, elitism)
    print()
    Elite(poblacion)
    print()
    Mutar(poblacion)
