# Install datasets library
!pip install datasets

# GPU config
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(f"GPU config error: {e}")

import numpy as np
from datasets import load_dataset
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import LearningRateScheduler
import re


train_dataset = load_dataset("iohadrubin/wikitext-103-raw-v1", split="train")
valid_dataset = load_dataset("iohadrubin/wikitext-103-raw-v1", split="validation")
test_dataset = load_dataset("iohadrubin/wikitext-103-raw-v1", split="test")

def clean_text(texts):
    cleaned_texts = []
    for text in texts:
        text = text.lower()
        text = re.sub(r'=.*=', '', text)
        text = re.sub(r'[^a-z\s]', '', text)
        text = ' '.join(text.split())
        if text:
            cleaned_texts.append(text)
    return cleaned_texts

train_samples = 5000
max_seq_length = 500   

clean_train_dataset = clean_text(train_dataset['text'][:train_samples])
clean_valid_dataset = clean_text(valid_dataset['text'])
clean_test_dataset = clean_text(test_dataset['text'])

tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(clean_train_dataset)

train_sequences = tokenizer.texts_to_sequences(clean_train_dataset)
valid_sequences = tokenizer.texts_to_sequences(clean_valid_dataset)
test_sequences = tokenizer.texts_to_sequences(clean_test_dataset)

def truncate_sequences(sequences, max_length):
    return [seq[:max_length] for seq in sequences]

train_trunc_sequences = truncate_sequences(train_sequences, max_seq_length)
valid_trunc_sequences = truncate_sequences(valid_sequences, max_seq_length)
test_trunc_sequences = truncate_sequences(test_sequences, max_seq_length)

def create_input_output_pairs(sequences, max_length):
    inputs, outputs = [], []
    for seq in sequences:
        if len(seq) > 1:
            inputs.append(seq[:-1])
            outputs.append(seq[1:])
    if not inputs:
        raise ValueError("No valid sequences found")
    inputs = pad_sequences(inputs, maxlen=max_length, padding='post')
    outputs = pad_sequences(outputs, maxlen=max_length, padding='post')
    return inputs, outputs

train_inputs, train_outputs = create_input_output_pairs(train_trunc_sequences, max_seq_length)
valid_inputs, valid_outputs = create_input_output_pairs(valid_trunc_sequences, max_seq_length)
test_inputs, test_outputs = create_input_output_pairs(test_trunc_sequences, max_seq_length)

def build_rnn_model(vocab_size, input_shape):
    print(f"Building model with vocab_size: {vocab_size}, input_shape: {input_shape}")
    model = Sequential(name="rnn_model")
    model.add(Embedding(input_dim=vocab_size, output_dim=100))   
    model.add(LSTM(128, return_sequences=True, dropout=0.2))
    model.add(Dense(vocab_size, activation='softmax'))
    model.build(input_shape)
    print(f"Model built with {model.count_params()} params")
    return model


def lr_schedule(epoch):
    lr = 0.001 * (0.95 ** epoch)  
    print(f"Epoch {epoch+1} LR: {lr}")
    return lr

def main():
    vocab_size = min(len(tokenizer.word_index) + 1, 10000)
    print(f"Vocabulary size: {vocab_size}")
    if np.max(train_inputs) >= vocab_size:
        raise ValueError("Token IDs exceed vocab_size!")

    input_shape = (None, max_seq_length)
    model = build_rnn_model(vocab_size, input_shape)
    
    model.compile(optimizer=Adam(learning_rate=0.001),
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])
    
    model.summary()
    
        
    history = model.fit(train_inputs, 
                       train_outputs,
                       validation_data=(valid_inputs, valid_outputs),
                       epochs=25,  
                       batch_size=64,
                       callbacks=[LearningRateScheduler(lr_schedule)],
                       verbose=1)
    
    loss, accuracy = model.evaluate(test_inputs, test_outputs, verbose=0)
    print(f'\n\nTest Accuracy: {accuracy}')
    
    val_acc = max(history.history['val_accuracy'])
    print(f"Max Validation Accuracy: {val_acc:.4f}")
    print(f"Validation accuracy test (≥25%): {'Passed' if val_acc >= 0.25 else 'Failed'}")

if __name__ == "__main__":
    main() 
