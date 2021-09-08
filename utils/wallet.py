import sys
import json
import random
import http.client
from binascii import hexlify
from .key_manager import KeyManager
from .network_manager import SymbolNetworkManager
from .message_builder import ThanksMessageBuilder
from .mosaic_util import MosaicUtil

# THanks Meter トランザクション蓄積用暫定アドレス
THANKS_METER_SERVICE_ADDRESS = 'TANHIM3MXBR7FL6ZGE7AMEFQNZVE7Y2R3IK5C2A'

class SimpleWallet:
    def __init__(self, network_id, key_file_name=None, pass_phrase=None):
        print('Initializing SimpleWallet...')
        self._nm = SymbolNetworkManager(network_id)
        self._facade = self._nm.get_facade()
        self._km = KeyManager(self._facade, '', pass_phrase, key_file_name)
        self._mosaic_util = MosaicUtil()

    def get_my_address(self):
        my_address = self._facade.network.public_key_to_address(self._get_my_pubkey())
        return str(my_address)

    def _get_my_pubkey(self):
        return self._km.get_my_pubkey()

    def get_my_pubkey_string(self):
        pubkey = self._km.get_my_pubkey()
        return str(pubkey)

    def get_network_address(self):
        my_address = self._facade.network.public_key_to_address(self._get_my_pubkey())
        return my_address

    def save_my_key(self, key_file_name):
        self._km.export_my_key(key_file_name)

    def set_mosaic_nonce(self, nonce):
        self._mosaic_util.setNonce(nonce)

    def check_my_account_info_with_address(self):
        req_msg = {
            "addresses": [
                self.get_my_address()
            ]
        }
        return json.loads(self._nm.send_accounts_info_req(req_msg))

    def check_account_info_with_address(self, address):
        req_msg = {
            "addresses": [
                address
            ]
        }
        return json.loads(self._nm.send_accounts_info_req(req_msg))

    def _build_thanks_tx(self, deadline, fee, recipient_address, msg_txt):
        tx = self._facade.transaction_factory.create({
            'type': 'transfer',
            'signer_public_key': self._km.get_my_pubkey(),
            'fee': fee,
            'deadline': deadline,
            'recipient_address': recipient_address,
            'message': bytes(1) + msg_txt.encode('utf8')
        })
        return tx

    def _build_mosaic_tx(self, deadline, fee, recipient_address, mosaics, msg_txt):
        tx2 = self._facade.transaction_factory.create({
            'type': 'transfer',
            'signer_public_key': self._km.get_my_pubkey(),
            'fee': fee,
            'deadline': deadline,
            'recipient_address': recipient_address,
            'mosaics': mosaics,
            'message': bytes(1) + msg_txt.encode('utf8')
        })
        return tx2

    def _build_mosaic_def_tx(self, deadline, fee, duration, flags, divisibility):
        tx3 = self._facade.transaction_factory.create({
            'type' : 'mosaicDefinition',
            'signer_public_key': self._km.get_my_pubkey(),
            'deadline': deadline,
            'fee': fee,
            'duration' : duration,
            'nonce' : self._mosaic_util.getNonce(),
            'flags' : flags,
            'divisibility' : divisibility
        })
        return tx3

    def _build_mosaic_supply_change(self, deadline, fee, delta, action):
        tx4 = self._facade.transaction_factory.create({
            'type' : 'mosaicSupplyChange',
            'signer_public_key': self._km.get_my_pubkey(),
            'deadline': deadline,
            'fee': fee,
            'mosaic_id' : self._mosaic_util.gen_mosaic_id(self.get_network_address()),
            'delta' : delta,
            'action' : action
        })
        return tx4
    def _build_req_tx_msg(self, tx):
        signature = self._km.compute_signature(tx)
        tx.signature = signature.bytes
        payload = {"payload": hexlify(tx.serialize()).decode('utf8').upper()}
        json_payload = json.dumps(payload)
        return json_payload

    def send_thanks_transacton(self, deadline, fee, target_address):
        tmb = ThanksMessageBuilder()
        msg_txt = tmb.build_tm_string(target_address)
        service_address = self._facade.Address(THANKS_METER_SERVICE_ADDRESS).bytes
        tx = self._build_thanks_tx(deadline, fee, service_address, msg_txt)
        json_payload = self._build_req_tx_msg(tx)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx)
        return (status, hash)

    def send_mosaic_transacton(self, deadline, fee, recipient_address, mosaics, msg_txt):
        tx2 = self._build_mosaic_tx(deadline, fee, recipient_address, mosaics, msg_txt)
        json_payload = self._build_req_tx_msg(tx2)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx2)
        return (status, hash)

    def send_mosaic_def_transacton(self, deadline, fee, duration, flags, divisibility):
        tx3 = self._build_mosaic_def_tx( deadline, fee, duration, flags, divisibility)
        json_payload = self._build_req_tx_msg(tx3)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx3)
        return (status, hash)

    def send_mosaic_supply_change_tx(self, deadline, fee, delta, action):
        tx4 = self._build_mosaic_supply_change(deadline, fee, delta, action)
        json_payload = self._build_req_tx_msg(tx4)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx4)
        return (status, hash)

    def get_received_transactions_with_address(self, address, page_size = 10, page_num = 1):
        return json.loads(self._nm.get_received_transactions_with_address(address, page_size, page_num))

    def get_sent_transactions(self, pubkey_string, page_size = 10, page_num = 1):
        return json.loads(self._nm.get_sent_transactions(pubkey_string, page_size, page_num))

    def get_tx_fee_info(self):
        return json.loads(self._nm.get_transaction_fee_info())

    def get_rental_fee_info(self):
        return json.loads(self._nm.get_rental_fee_info())

    def et_nw_properties_info(self):
        return json.loads(self._nm.get_nw_properties_info())

    def get_node_health_info(self):
        return json.loads(self._nm.get_node_health_info())

    def get_node_info(self):
        return json.loads(self._nm.get_node_info())

    def get_unconfirmed_txs_with_pubkey(self, pubkey_string, page_size = 10, page_num = 1):
        return json.loads(self._nm.get_unconfirmed_txs_with_pubkey(pubkey_string, page_size, page_num))

    def _get_transaction_hash(self, tx):
        return self._facade.hash_transaction(tx)

    def get_transaction_status(self, hash):
        return json.loads(self._nm.get_transaction_status(hash))