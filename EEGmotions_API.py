from fastapi import FastAPI
from pydantic import BaseModel
from torcheeg.transforms import BandDifferentialEntropy, Concatenate
from torcheeg.models import SSTEmotionNet
import ast

import numpy as np

class Item(BaseModel):
    data: str

app = FastAPI()

# Util functions -------------------------------------------------------------------------------------
def raw_to_de_data(data):
    
    len_data = data.shape[1]

    transform = BandDifferentialEntropy(sampling_rate = 256, band_dict = {'alpha': [8, 13], 'beta': [14, 30], 'gamma': [31, 50], 'theta': [4, 7], 'delta': [0.5, 3]})
    de_data = transform(eeg=data)['eeg']
    
    return de_data
        
# def test_model(data):
#     concat = Concatenate()
    
#     model = SSTEmotionNet(temporal_in_channels=2, spectral_in_channels=5, grid_size=(2, 2), num_classes=5)
#     print(model(data))

# Async functions -------------------------------------------------------------------------------------
@app.post("/data/raw/")
async def receive_raw_data(initial_data: Item):
    
    np_data = np.array(ast.literal_eval(initial_data.data), dtype = int)
    de_data = raw_to_de_data(np_data)
    
    print(f"Original data: {initial_data}\nDifferential entropy: {de_data}")
    
    # test_model()
    
    return 
