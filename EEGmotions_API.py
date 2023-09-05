#RUN SERVER WITH $ uvicorn EEGmotions_API:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
import pyeeg as pe
import ast
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

from scipy import stats as st


class Item(BaseModel):
    data: str

app = FastAPI()

#Load model just once--------------------------------------------------------------------------------

#For these models, ch1 is FP2 and ch2 is F8
model_arousal_url = './tools/model/model_2classes_arousal.h5'
model_valence_url = './tools/model/model_2classes_valence.h5'

# CNN models slightly changed from: https://github.com/siddhi5386/Emotion-Recognition-from-brain-EEG-signals-/
arousal_model = tf.keras.models.load_model(model_arousal_url)
valence_model = tf.keras.models.load_model(model_valence_url)

scaler = StandardScaler()

# Util functions -------------------------------------------------------------------------------------

# FFT processing function, modified version of code in https://github.com/siddhi5386/Emotion-Recognition-from-brain-EEG-signals-/blob/master/Emotion_recognition_using_CNN.ipynb
def FFT_Processing(data_batch, band, window_size, step_size, sample_rate):

    processed_data = []
    batch_size = data_batch.shape[0]

    for i in range(batch_size):

        data = data_batch[i]
        start = 0
        
        while start + window_size < data.shape[1]:
            meta_data = []  # meta vector for analysis

            for j in range(data.shape[0]):  # Iterate over channels
                X = data[j][start: start + window_size]  # Slice raw data over 2 sec
                Y = pe.bin_power(X, band, sample_rate)  # FFT over 2 sec of channel j
                meta_data = meta_data + list(Y[0])

            processed_data.append(np.array(meta_data, dtype=object))  
            start = start + step_size

    return np.array(processed_data)


# Async functions -------------------------------------------------------------------------------------
@app.post("/data/raw/")
async def receive_raw_data(initial_data: Item):

    #Data for the FFT
    band = [4,8,12,16,25,45] #5 bands
    window_size = 256 #Averaging band power of 2 sec
    step_size = 16 #Each 0.125 sec update once
    sample_rate = 128 #Sampling rate of 128 Hz

    eeg_data = ast.literal_eval(initial_data.data)

    np_eeg_data = np.array([np.array(x) for x in eeg_data])
    de_data = FFT_Processing(np_eeg_data, band, window_size, step_size, sample_rate)

    de_data = normalize(de_data)
    de_data = scaler.fit_transform(de_data)

    arousal = arousal_model.predict(de_data)
    valence = valence_model.predict(de_data)

    predicted_arousal = st.mode(np.argmax(arousal, axis=1))
    predicted_valence = st.mode(np.argmax(valence, axis=1))

    print(np.argmax(arousal, axis=1), np.argmax(valence, axis=1))
    print(predicted_arousal, predicted_valence)

    mode_result = [int(predicted_valence[0]), int(predicted_arousal[0])]

    return mode_result
