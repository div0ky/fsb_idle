# version_info.py

vMajor = 5  # Increments on a BREAKING change
vMinor = 0  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX / PATCH
vStage = "dev.5"
full_version = f"{vMajor}.{vMinor}.{vPatch}-{vStage}"  # Should be self explanatory
version = f"{vMajor}.{vMinor}.{vPatch}"  # Should be self explanatory