
ALPHAFOLD_PATH = "/mnt/alphafold"
ALPHAFOLD_DATA_DIR = "/mnt/data"
CALCULATIONS_CACHE = "/calculations-cache"
MAX_CONCURRENT_CALCULATIONS = 1

# Explanation of Alphafold outputs
# https://blog.biostrand.ai/explained-how-to-plot-the-prediction-quality-metrics-with-alphafold2

DownloadOptions = {
    # Download predicted structure files
    "ranked_pdb": r"^ranked_\d+\.pdb$",
    "ranked_cif": r"^ranked_\d+\.cif$",
    "unrelaxed_pdb": r"^unrelaxed_model_\d+.*\.pdb$",
    "unrelaxed_cif": r"^unrelaxed_model_\d+.*\.cif$",
    
    # Download single file with ordering and confidence of rankings
    "ranking_debug": r"^ranking_debug\.json",

    # Download confidence model files
    "confidence_model": r"^confidence_model_\d+.*\.json$",
    
    # Download structure model pkl files
    "model_pkl": r"^result_model_\d+.*\.pkl$",

    # Download misc metadata single files
    "features": r"^features\.pkl$",
    "msas": r"^msas$",
    "timings": r"^timings.json$",
    "relax_metrics": r"^relax_metrics.json$",

    # Download all files
    "all_data": r"^$",
}