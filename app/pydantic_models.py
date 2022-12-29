from pydantic import BaseModel
from typing import List, Optional
#import numpy as np

class ProcessingData(BaseModel):

    text_sentence : str = "I'm Andrew Huberman and I'm a professor of neurobiology and ophthalmology"
    audio_data : Optional[List[List]]
    voice_name : str = 'custom'
    preset : str = 'fast'
    fast_mode: bool = False

    class Config:
        arbitrary_types_allowed = True