import numpy as np


class individuo:

    def __init__(self, quantity, mutacionPercentage):
        self.calificacion = 0
        self.fenotipo = 0
        self.plumas5 = 0
        self.plumas8 = 0
        self.plumas23 = 0
        self.relacionMutua = 0
        self.relacionFenotipica = 0
        self.mutacionProbability = mutacionPercentage
        self.genotipo = np.random.randint(0, 2, quantity)

    def newcomer(self, genotipo):
        self.genotipo = genotipo

    def Mutacion(self):
        i = np.random.randint(0, 100)
        if (self.mutacionProbability * 100) >= i:
            i = np.random.randint(0, len(self.genotipo) - 1)
            tmp = self.genotipo.copy()
            self.genotipo[i] = abs(self.genotipo[i] - 1)
            print('El individuo {} muto a {}'.format(tmp, self.genotipo))
