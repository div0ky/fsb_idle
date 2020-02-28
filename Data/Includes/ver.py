class version_info:
    def __init__(self):
        self.vMajor = 3  # Increments on a BREAKING change
        self.vMinor = 1  # Increments on a FEATURE change
        self.vPatch = 0  # Increments on a FIX / PATCH
        self.vStage = "alpha.3"
        self.version = f"{self.vMajor}.{self.vMinor}.{self.vPatch}-{self.vStage}"  # Should be self explanatory