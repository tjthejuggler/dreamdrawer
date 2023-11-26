from huggingface_hub import cached_download

# Clear cache by downloading a small file
cached_download("", cache_dir=None, force_download=True)
