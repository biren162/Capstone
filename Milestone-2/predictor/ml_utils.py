import pandas as pd
import numpy as np

def init_app():
    print('Initializing the things...')


# function to retrain the model as part of the feedback loop

def predict(text):
    sentences = [text]

    pred_tokens = map(tokenizer2.tokenize, sentences)
    pred_tokens = map(lambda tok: ["[CLS]"] + tok + ["[SEP]"], pred_tokens)
    pred_token_ids = list(map(tokenizer2.convert_tokens_to_ids, pred_tokens))

    pred_token_ids = map(lambda tids: tids + [0] * (512 - len(tids)), pred_token_ids)
    pred_token_ids = np.array(list(pred_token_ids))

    predictions = model2.predict(pred_token_ids).argmax(axis=-1)

    for text, label in zip(sentences, predictions):
        print("text:", text, "\nintent:", classes[label])
    return
