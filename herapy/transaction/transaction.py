class Transaction:
    def __init__(self, payload):
        self.payload = payload
        self.signature = None
        self._signed = False

    def sign_with_key_manager(self, km):
        self.signature = km.sign_message(self.payload)
        self.mark_signed()

    def mark_signed(self):
        self._signed = True

    def is_signed(self):
        return self._signed and self.signature is not None