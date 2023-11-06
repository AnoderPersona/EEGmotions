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
model_arousal_url = './tools/model/model_2classes_arousal_best.h5'
model_valence_url = './tools/model/model_2classes_valence_best.h5'

# CNN models slightly changed from: https://github.com/siddhi5386/Emotion-Recognition-from-brain-EEG-signals-/
arousal_model = tf.keras.models.load_model(model_arousal_url)
valence_model = tf.keras.models.load_model(model_valence_url)

# Variables for the FFT 
band = [4,8,12,16,25,45] #5 bands
window_size = 256 #Averaging band power of 2 sec
step_size = 16 #Each 0.125 sec update once
sample_rate = 128 #Sampling rate of 128 Hz
scaler = StandardScaler()

# Util functions -------------------------------------------------------------------------------------

# FFT processing function, modified version of code in https://github.com/siddhi5386/Emotion-Recognition-from-brain-EEG-signals-/blob/master/Emotion_recognition_using_CNN.ipynb
def FFT_Processing(data_batch):

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

def model_processing(data):

    # Neutral threshold for calibrating the model
    neutral_threshold = [0.5, 0.62]#[0.5, 0.7]

    # Normalising data
    data = np.array(normalize(data)[:])
    data = scaler.fit_transform(data)
    data = data.reshape(data.shape[0],data.shape[1], 1)

    # Get prediction
    arousal = arousal_model.predict(data)
    valence = valence_model.predict(data)

    # Valence needs calibration, so a neutral state is added to minimize false negatives
    predicted_valence = np.array([2 if (x[0] > neutral_threshold[0] and x[0] < neutral_threshold[1]) else np.argmax(x) for x in valence])
    #predicted_valence = np.argmax(valence, axis=1)
    predicted_arousal = np.argmax(arousal, axis=1)

    print(valence, arousal)
    print(predicted_valence, predicted_arousal)

    # Get most repeated value in time windows
    predicted_valence = st.mode(predicted_valence)
    predicted_arousal = st.mode(predicted_arousal)

    print(predicted_valence, predicted_arousal)

    return [int(predicted_valence[0]), int(predicted_arousal[0])]
    


# Async functions -------------------------------------------------------------------------------------
@app.post("/data/raw/")
async def receive_raw_data(initial_data: Item):

    # Receives data
    eeg_data = ast.literal_eval(initial_data.data)

    # Turns python list into np.array 
    np_eeg_data = np.array([np.array(x) for x in eeg_data])
    fft_data = FFT_Processing(np_eeg_data)

    # Get and send final result
    mode_result = model_processing(fft_data)
    return mode_result
