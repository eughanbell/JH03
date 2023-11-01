
########## PDBe Scoring Weights ##########
PDBe_SCORE_WEIGHTS = {
    "resolution": 0.02,
    "method": 1,
    "chain_length": 1,
}

PDBe_METHOD_WEIGHTS = {
    "X-ray": 1,   
}

PDBe_RESOLUTION_WEIGHTS = {
    "interpolation": "exponential",
    # Weight at 0 is assumed to be 1 (infinite resolution scores 1)
    "weight_at_1": 0.9
}
