# version_info.py

vMajor = 6  # Increments on a BREAKING change
vMinor = 0  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX / PATCH
vStage = "dev.5"
full_version = f"{vMajor}.{vMinor}.{vPatch}-{vStage}"  # Should be self explanatory
version = f"{vMajor}.{vMinor}.{vPatch}"  # Should be self explanatory

if vStage == "stable":
    current_version = version
else:
    current_version = full_version
