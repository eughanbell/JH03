# Explanation of Alphafold outputs
# https://blog.biostrand.ai/explained-how-to-plot-the-prediction-quality-metrics-with-alphafold2

DownloadOptions = {
    # Download predicted structure files
    "ranked_pdb": "^ranked_\d+\.pdb$",
    "ranked_cif": "^ranked_\d+\.cif$",
    "unrelaxed_pdb": "^unrelaxed_model_\d+.*\.pdb$",
    "unrelaxed_cif": "^unrelaxed_model_\d+.*\.cif$",
    
    # Download single file with ordering and confidence of rankings
    "ranking_debug": "^ranking_debug\.json",

    # Download confidence model files
    "confidence_model": "^confidence_model_\d+.*\.json$",
    
    # Download structure model pkl files
    "model_pkl": "^result_model_\d+.*\.pkl$",

    # Download misc metadata single files
    "features": "^features\.pkl$",
    "msas": "^msas$",
    "timings": "^timings.json$",
    "relax_metrics": "^relax_metrics.json$",

    # Download all files
    "all_data": "^$",
}

