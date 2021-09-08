import secrets
import sha3

NAMESPACE_FLAG = 1 << 63

class MosaicUtil:

    def __init__(self):
        self._nonce = int(secrets.randbits(32))

    def getNonce(self):
        return self._nonce

    def setNonce(self, nonce):
        self._nonce = nonce

    def _generate_mosaic_id(self, owner_address):
        hasher = sha3.sha3_256()
        hasher.update(self._nonce.to_bytes(4, 'little'))
        hasher.update(owner_address.bytes)
        digest = hasher.digest()
        result = int.from_bytes(digest[0:8], 'little')
        if result & NAMESPACE_FLAG:
            result -= NAMESPACE_FLAG
        return result

    def gen_mosaic_id(self, address):
        return self._generate_mosaic_id(address)
