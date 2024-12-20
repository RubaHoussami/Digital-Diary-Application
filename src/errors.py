class DangerDetected(Exception):
    def __init__(self, message="Dangerous content detected"):
        super().__init__(message)
