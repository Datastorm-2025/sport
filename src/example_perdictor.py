import os
import random

VALID_BANDS = ['band_1_2', 'band_2_4', 'band_4_6', 'band_6_8', 'band_8_10']


def predictor(video_path: str) -> str:

    if not os.path.exists(video_path):
        return VALID_BANDS[2]
    
    return random.choice(VALID_BANDS)



