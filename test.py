import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
import torch.nn as nn
import math, keras
from keras_preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras import backend as K

MAX_SEQUENCE_LENGTH = 54


class TestDataset(Dataset) :
  #Dataset - English/typo-added/labeled
  def __init__(self, df) :
    self.df = df
  
  def __len__(self) :
    return len(self.df)
  
  def __getitem__(self, idx):
    text = self.df.iloc[idx, 0]
    item = self.df.iloc[idx, 1]
    return text, item

def get_prediction(data) :
    #Tokenizer building
    total_df = pd.read_csv('augmented_data/Dataset_aug_complex_10424_original.csv', sep=',')
    total_df.dropna(inplace=True)
    total_df = total_df[["text", "label"]]
    total_df["label"] = [1 if i == "nothate" else 0 for i in total_df["label"]]
    total_dataset = TestDataset(total_df)
    total_loader = DataLoader(total_dataset, batch_size=1, shuffle=True)

    texts = []
    for text, _ in total_loader:
        texts.append(text[0])
        
    tokenizer = Tokenizer(nb_words=20000)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)

    received_text = [data]
    valid_lengths = []

    for text in received_text:
        valid_lengths.append(len(text.split(' '))) 
    sequences_test = tokenizer.texts_to_sequences(received_text)
    sequences_test = pad_sequences(sequences_test, maxlen=MAX_SEQUENCE_LENGTH, padding = 'post')
    model = keras.models.load_model('model_save_check')
    valid_lengths = np.array(valid_lengths)
    get_fil_tgt = K.function([model.layers[0].input, model.layers[3].input],
                                    [model.layers[4].output, model.layers[5].output])

    x = [sequences_test, valid_lengths]
    [_, filter_index], preds = get_fil_tgt(x)
    result = preds.argmax(axis = -1)
    return result, filter_index
t = 'fuck china'
print(get_prediction(t))