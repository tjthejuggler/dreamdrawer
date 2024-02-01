from transformers.file_utils import cached_path, TRANSFORMERS_CACHE

print("Transformer's cache directory:", TRANSFORMERS_CACHE)

# Example model to check the cache
model_name = "stabilityai/stable-diffusion-xl-base-1.0"

# Get the cached file path
model_cache = cached_path(model_name, cache_dir=TRANSFORMERS_CACHE)
print("Cached path for the model:", model_cache)
