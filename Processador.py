from io import TextIOWrapper
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from tqdm import tqdm

class Processador: #claramente ha um problema de memoria quando tentas processar os smiles todos de uma vez. tens que ir um a um ou fazer batches
    padding = False
    vocab = None
    
    def __init__(self, max_size=100, vocab="auto"):
        self.max_size = max_size
        self.vocab = vocab

    def pre_process_smiles(self, smiles, n_smiles=None):
        print("A verificar smiles...")
        smiles = [s for s in ['G' + smile.replace("Br", 'R').replace("Cl", 'C') + 'A' for smile in tqdm(smiles)] if (self.max_size != None and len(s) <= self.max_size)]
        if len(smiles) < n_smiles:
            print(f"\033[93mAviso - Nos dados fornecidos a fit apenas constam {len(smiles)} válidos segundo as configurações pedidas (foram solicitados {n_smiles})")
        return smiles[:n_smiles]

    def pad(self, encoded_smiles):
        encoded_smiles = pad_sequences(encoded_smiles, value=self.vocab['A'], maxlen=self.max_size, padding='post')
        return encoded_smiles
    
    def encode(self, smiles):
        if self.vocab == 'auto':
            print("A gerar vocabulário...")
            tokens = np.unique([c for smile in tqdm(smiles) for c in smile])
            self.vocab = {token: index for (index, token) in enumerate(tokens)}
        else:
            print('A carregar vocabulário...')
            if type(self.vocab) != dict:
                with open(self.vocab, "r") as vocab_file:
                    tokens = [x.strip() for x in vocab_file.read().strip().splitlines() if x.strip()]
                    self.vocab = {token: index for (index, token) in enumerate(tokens)}
            tokens_observados = np.unique([c for smile in tqdm(smiles) for c in smile])
            tokens_conhecidos = self.vocab.keys()
            if len(np.setdiff1d(tokens_observados, tokens_conhecidos)):
                print("O vocabulário existente não suporta os tokens encontrados")
                exit(1)

        encoded_smiles = []
        tokens_ordenados = sorted(self.vocab.keys(), key=len, reverse=True)
        print("A codificar smiles...")
        for smile in tqdm(smiles):
            encoded_smile = [None] * self.max_size
            for token in tokens_ordenados:
                while token in smile:
                    encoded_smile[smile.index(token)] = self.vocab[token]
                    smile = smile.replace(token, ' ' * len(token), 1)
            encoded_smile = list(filter(None, encoded_smile))
            encoded_smiles.append(np.asarray(encoded_smile))
        return encoded_smiles
    
    def processa(self, smiles, n_smiles):
        smiles = self.pre_process_smiles(smiles, n_smiles)
        smiles = self.encode(smiles)
        smiles = self.pad(smiles)
        x_train = smiles
        y_train = np.transpose(np.append(np.transpose(smiles)[1:], np.full((1, smiles.shape[0]), self.vocab["A"]), axis = 0))
        #x_train = np.reshape(x_train, (self.n_smiles, self.size, 1))
        y_train = np.reshape(y_train, (self.n_smiles, self.max_size))
        #print("xtrain = ", x_train, "ytrain = ", y_train)
        return (x_train, y_train), self.vocab

def main():
    reader = Processador(n_smiles=100000, max_size=100, vocab="auto")
    (x_train, y_train), vocab = reader.processa('ChEMBL_filtered.txt')
        





            


if __name__ == "__main__":
    main()