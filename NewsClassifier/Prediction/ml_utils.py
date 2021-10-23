import pandas as pd
import numpy as np
import torch
from tensorflow.keras.models import load_model
import bert

def init_app():
    print('Initializing the things...')


def load_trained_model():
    return load_model("models/bert_model.h5",custom_objects={"BertModelLayer": bert.BertModelLayer})

# function to predict the class

def predict(text):
    max_seq_len = 512
    classes = ['Science/Technology', 'Sports', 'Politics', 'Business']
    saved_tokenizer = torch.load('models/tokenizer')
    saved_model = load_trained_model()
    sentences = [text]
    pred_tokens = map(saved_tokenizer.tokenize, sentences)
    pred_tokens = map(lambda tok: ["[CLS]"] + tok + ["[SEP]"], pred_tokens)
    pred_token_ids = list(map(saved_tokenizer.convert_tokens_to_ids, pred_tokens))

    pred_token_ids = map(lambda tids: tids + [0] * (max_seq_len - len(tids)), pred_token_ids)
    pred_token_ids = np.array(list(pred_token_ids))

    predictions = saved_model.predict(pred_token_ids).argmax(axis=-1)
    result = []

    for text, label in zip(sentences, predictions):
        print("text:", text, "\nintent:", classes[label])
        result.append(classes[label])

    return result[0]
