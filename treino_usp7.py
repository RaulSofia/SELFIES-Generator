from Gerador import Gerador
from PreProcessador import PreProcessador
from utils import *
import os


if __name__ == "__main__":
    configs = get_configs('CONFIG.csv')
    processador = PreProcessador(configs)
    dados1, vocab = processador.processa('ChEMBL_filtered.txt')
    gerador = Gerador(configs, vocab)
    gerador.treina(dados1)
    gerador.save()
    dados2, vocab = processador.processa('dataset4.csv')
    gerador.treina(dados2)
    gerador.save()