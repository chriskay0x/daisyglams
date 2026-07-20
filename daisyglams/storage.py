from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    # This tells WhiteNoise to ignore missing referenced files instead of crashing
    manifest_strict = False