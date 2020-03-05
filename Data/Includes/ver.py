#! python3
class version_info:
    def __init__(self):
        self.vMajor = 4  # Increments on a BREAKING change
        self.vMinor = 1  # Increments on a FEATURE change
        self.vPatch = 2  # Increments on a FIX / PATCH
        self.vStage = "dev.1"
        self.full_version = f"{self.vMajor}.{self.vMinor}.{self.vPatch}-{self.vStage}"  # Should be self explanatory
        self.version = f"{self.vMajor}.{self.vMinor}.{self.vPatch}"  # Should be self explanatory