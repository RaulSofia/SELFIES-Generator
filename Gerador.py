from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Softmax, Embedding
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import EarlyStopping
import os
from datetime import datetime


class Gerador():
    dados_treino = []

    def __init__(self, configs, vocab): #dados é uma instancia de PreProcessador()
        for config in configs:
            if config == 'optimizer' and configs[config] == 'rms_prop':
                    configs['optimizer'] = RMSprop()
            setattr(self, config, configs[config])
        self.model = Sequential()
        self.path = './'
        self.build(vocab)
        self.vocab = vocab
    
    # def __init__(self, vocab):
    #     self.vocab = vocab

    def build(self, vocab):
        self.model.add(Embedding(input_dim=len(vocab), output_dim=self.embedding_size, input_length=self.size)) #https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/
        for i in range(self.layers):
            # if i == (self.layers - 1):
            #     self.model.add(LSTM(self.unidades, dropout=self.dropout, return_sequences=False))
            #     break
            self.model.add(LSTM(self.unidades, dropout=self.dropout, return_sequences=True))
        self.model.add(Dense(len(vocab)))
        self.model.add(Softmax())
        
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=['accuracy'])

        print(self.model.summary())

    def treina(self, dados):
        x_train, y_train = dados
        #checkpoint = ModelCheckpoint()
        print(y_train.shape)
        early_stop = EarlyStopping(monitor='loss', patience=self.patience)
        callbacks_list = [early_stop]
        self.model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs, shuffle=True)#, callbacks=callbacks_list) #TODO


    def save(self):
        run_id = "run_at_" + datetime.now().strftime("%d_%m_%y_%H_%M_%S")
        dir_path = "./runs/" + run_id + "/"
        os.makedirs(dir_path)
        self.model.save(dir_path + "modelo")
        text_vocab = str(list(enumerate(self.vocab))).replace(", '", ": ").replace("'), (", "\n")[2:-3]
        with open(os.path.join(dir_path, "vocab.txt"), "w") as vocab_log:
            vocab_log.write(text_vocab)


    



        
        
if __name__ == "__main__":
    from PreProcessador import PreProcessador
    from utils import *
    configs = get_configs("CONFIG.csv")
    print(configs)
    
    leitor = PreProcessador(configs)
    dados, vocab = leitor.processa('ChEMBL_filtered.txt')
    print(dados)
    gerador = Gerador(configs, vocab)
    gerador.treina(dados)
    gerador.save()