from Gerador import Gerador
from Processador import Processador
from utils import *
import os


if __name__ == "__main__":
    configs = get_configs('CONFIG.csv')
    processador = Processador(configs)
    dados1, vocab = processador.processa('ChEMBL_filtered.txt')
    gerador = Gerador(configs, vocab)
    gerador.treina(dados1)
    gerador.save()
    dados2, vocab = processador.processa('dataset4.csv')
    gerador.treina(dados2)
    gerador.save()