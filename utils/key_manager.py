from symbolchain.core.CryptoTypes import PrivateKey
from symbolchain.core.sym.KeyPair import KeyPair
from symbolchain.core.PrivateKeyStorage import PrivateKeyStorage
from symbolchain.core.facade.SymFacade import SymFacade

class KeyManager:

	def __init__(self, facade, dir_name='', pass_phrase= None, privatekey_path = None):
		print('Initializing KeyManager...')
		self._facade = facade
		self._p_storage = PrivateKeyStorage(dir_name, pass_phrase)

		if privatekey_path:
			self._private_key = self._p_storage.load(privatekey_path)
		else:
			self._private_key = PrivateKey.random()

		self._keypair = SymFacade.KeyPair(self._private_key)
		self._public_key = self._keypair.public_key

	def get_my_pubkey(self):
		return self._public_key

	def export_my_key(self, key_file_name):
		"""
		秘密鍵をファイルとして保存。ファイル保存する際はpem形式。初期化時にpass_phraseを指定していたらそれを使って保護する
		"""
		self._p_storage.save(key_file_name, self._private_key)

	def compute_signature(self, transaction):
		"""
		現状は抽象化が不完全でトランザクションへの署名とイコール
		"""
		return self._facade.sign_transaction(self._keypair, transaction)

	def verify_signature(self, transaction, signature):
		"""
		現状は抽象化が不完全でトランザクションへの署名の検証とイコール
		"""
		return self._facade.verify_transaction(transaction, signature)