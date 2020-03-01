class version_info:
    def __init__(self):
        self.vMajor = 4  # Increments on a BREAKING change
        self.vMinor = 0  # Increments on a FEATURE change
        self.vPatch = 4  # Increments on a FIX / PATCH
        self.vStage = "dev.13"
        self.version = f"{self.vMajor}.{self.vMinor}.{self.vPatch}-{self.vStage}"  # Should be self explanatory