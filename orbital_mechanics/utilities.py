import numpy as np

def is_ND_vec(vec: np.ndarray, N: int) -> bool:
    return vec.shape == (N,)
