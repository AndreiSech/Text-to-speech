from pydantic import BaseModel
from Typing import List, Tuple, Optional, dictionary
import torch

class ProcessingData(BaseModel):

    text_sequence : str = "I'm Andrew Huberman and I'm a professor of neurobiology and ophthalmology"
    audio_data : Optional[List[torch.FloatTensor]]
    voice_name : str = 'custom'
	preset : str = 'fast'
    fast_mode: bool