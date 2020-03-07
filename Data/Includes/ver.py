#! python3
class version_info:
    def __init__(self):
        self.vMajor = 5  # Increments on a BREAKING change
        self.vMinor = 0  # Increments on a FEATURE change
        self.vPatch = 0  # Increments on a FIX / PATCH
        self.vStage = "dev.4"
        self.full_version = f"{self.vMajor}.{self.vMinor}.{self.vPatch}-{self.vStage}"  # Should be self explanatory
        self.version = f"{self.vMajor}.{self.vMinor}.{self.vPatch}"  # Should be self explanatory