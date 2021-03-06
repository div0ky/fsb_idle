# version_info.py

vMajor = 0  # Increments on a BREAKING change
vMinor = 9  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX / PATCH
vStage = "stable"
full_version = f"{vMajor}.{vMinor}.{vPatch}-{vStage}"  # Should be self explanatory
version = f"{vMajor}.{vMinor}.{vPatch}"  # Should be self explanatory

if vStage == "stable":
    current_version = version
else:
    current_version = full_version
