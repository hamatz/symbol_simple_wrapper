import sys
import json
import random
import http.client
from binascii import hexlify, unhexlify
from symbolchain.core.sym.MerkleHashBuilder import MerkleHashBuilder
from symbolchain.core.CryptoTypes import Hash256
from symbolchain.core.CryptoTypes import PublicKey
import sha3

from .key_manager import KeyManager
from symbolchain.core.sym.Network import Address
from .network_manager import SymbolNetworkManager
from .message_builder import ThanksMessageBuilder
from .mosaic_util import MosaicUtil

# THanks Meter トランザクション蓄積用暫定アドレス
THANKS_METER_SERVICE_ADDRESS = 'TANHIM3MXBR7FL6ZGE7AMEFQNZVE7Y2R3IK5C2A'

class SimpleWallet:
    """
    Symbol SDK-Pythonを簡易に利用するための各種ヘルパー関数を保持する。
    """
    def __init__(self, network_id, key_file_name=None, pass_phrase=None):
        """
        Parameters
        ----------
        network_id : int
            現在は testnetとmainnetを区別するために利用する。0であればtestnet。1であればmainnet
        key_file_name : string
            秘密鍵が格納されているファイル名。パスワード暗号がかけられているpem形式のファイルであることを想定
        pass_phrase : string
            秘密鍵復号用のパスフレーズ
        """
        print('Initializing SimpleWallet...')
        self._nm = SymbolNetworkManager(network_id)
        self._facade = self._nm.get_facade()
        self._km = KeyManager(self._facade, '', pass_phrase, key_file_name)
        self._mosaic_util = MosaicUtil()

    def get_my_address(self):
        """
        自分のアドレス情報を取得する。

        Parameters
        ----------
        なし

        Returns
        -------
        my_address : string
            自分のアドレス情報
        """
        my_address = self._facade.network.public_key_to_address(self._get_my_pubkey())
        return str(my_address)

    def get_network_address(self):
        """
        バイナリ状態の自分のアドレス情報を取得する。

        Parameters
        ----------
        なし

        Returns
        -------
        my_address : binary
            バイナリ状態の自分のアドレス情報
        """
        my_address = self._facade.network.public_key_to_address(self._get_my_pubkey())
        return my_address

    def _get_my_pubkey(self):
        return self._km.get_my_pubkey()

    def get_my_pubkey_string(self):
        """
        自分の公開鍵情報を取得する。

        Parameters
        ----------
        なし

        Returns
        -------
        pubkey : string
            自分の公開鍵情報を文字列化したもの
        """
        pubkey = self._km.get_my_pubkey()
        return str(pubkey)

    def get_hex_address(self, address):
        """
        入力されたアドレスに対してbase32ToHexAddress処理した結果の文字列を取得する。

        Parameters
        ----------
        address : string
            Symbolネットワーク上のアドレス

        Returns
        -------
        hexlify_address : string
            base32ToHexAddress処理した結果の文字列
        """
        target = Address(address)
        return hexlify(target.bytes)

    def get_unhexed_address(self, target):
        """
        入力された文字列に対してbase32ToHexAddressの逆変換処理した結果の文字列を取得する。

        Parameters
        ----------
        target : string
            base32ToHexAddress処理されたアドレス情報

        Returns
        -------
        address : string
            入力に対してbase32ToHexAddressの逆変換処理した結果の文字列
        """
        return Address(unhexlify(target))

    def save_my_key(self, key_file_name):
        """
        秘密鍵を暗号化してファイル保存する。

        Parameters
        ----------
        key_file_name : string
            秘密鍵を格納するファイルの名前

        Returns
        -------
        なし

        Notes
        -------
        初期化時にpass_phraseを指定している場合、それを利用してパスワード暗号をかけて保存される

        See Also
        --------
        __init__ : ここで pass_phrase を指定する必要がある。
        """
        self._km.export_my_key(key_file_name)

    def get_pubkey_from_str(self, pubkey_str):
        """
        入力された文字列から公開鍵オブジェクトを取得する。

        Parameters
        ----------
        pubkey_str : string
            文字列化された公開鍵情報

        Returns
        -------
        pubkey : PublicKey
            公開鍵オブジェクト
        """
        return PublicKey(unhexlify(pubkey_str))

    def sign_tx(self, tx):
        """
        トランザクションに対して署名を実施する。

        Parameters
        ----------
        tx : transaction
            トランザクションデータ

        Returns
        -------
        signed_tx : transaction
            署名付きとなったトランザクションデータ
        """
        return self._km.sign_tx(tx)

    def verify_tx(self, tx, signature):
        """
        トランザクションに対して行われている署名の検証を実施する。

        Parameters
        ----------
        tx : transaction
            トランザクションデータ
        signature : signature
            署名データ

        Returns
        -------
        result : boolean
            署名の検証結果
        """
        return self._km.verify_tx(tx, signature)

    def compute_signature(self, target):
        """
        与えられたデータに対してデジタル署名を実施する。

        Parameters
        ----------
        target :
            署名対象となるデータ

        Returns
        -------
        signed_data :
            署名データ
        """
        return self._km.compute_signature(target)

    def verify_signature(self, target, signature, pubkey):
        """
        与えられたデータに対して行われている署名を指定された公開鍵を用いて検証する。

        Parameters
        ----------
        target :
            検証に使うデータ
        signature : signature
            署名データ
        pubkey : publickey
            公開鍵データ

        Returns
        -------
        result : boolean
            署名の検証結果
        """
        return self/_km.verify_signature(target, signature, pubkey)

    def hash_transaction(self, tx):
        """
        与えられたトランザクションのハッシュ値を取得する

        Parameters
        ----------
        tx : transaction
            ハッシュ値をとる対象となるトランザクションデータ

        Returns
        -------
        result :
            ハッシュ化されたデータ
        """
        return self._facade.hash_transaction(tx)

    def set_mosaic_nonce(self, nonce):
        '''
        MosaicUtilのNonceを外部から指定する。モザイク発行後に総量を変更したい場合等、これを利用することでモザイクIDを算出出来るようにする
        '''
        self._mosaic_util.setNonce(nonce)

    def check_my_account_info_with_address(self):
        '''
        自分のアドレス情報を利用してSymbolネットワークからアカウント情報を取得する
        '''
        req_msg = {
            "addresses": [
                self.get_my_address()
            ]
        }
        return json.loads(self._nm.send_accounts_info_req(req_msg))

    def check_account_info_with_address(self, address):
        '''
        指定したアドレス情報を利用してSymbolネットワークからアカウント情報を取得する
        '''
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

    def get_thanks_tx_base(self, pubkey, target_address):
        '''
        Thanks Transactionのベースを生成する
        '''
        tmb = ThanksMessageBuilder()
        msg_txt = tmb.build_tm_string(target_address)
        service_address = self._facade.Address(THANKS_METER_SERVICE_ADDRESS)
        ttx = self._facade.transaction_factory.create_embedded({
            'type': 'transfer',
            'signer_public_key': pubkey,
            'recipient_address': service_address,
            'message': bytes(1) + msg_txt.encode('utf8')
        })
        return ttx

    def get_mosaic_tx_base(self, pubkey, target_address, mosaics, msg_txt):
        '''
        モザイク送信のためのTransactionのベースを生成する
        '''
        t_address = self._facade.Address(target_address)
        mtx = self._facade.transaction_factory.create_embedded({
            'type': 'transfer',
            'signer_public_key': pubkey,
            'recipient_address': t_address,
            'mosaics': mosaics,
            'message': bytes(1) + msg_txt.encode('utf8')
        })
        return mtx

    def get_aggregate_tx_base(self, deadline, fee, transactions_hash, txs):
        '''
        アグリゲートトランザクションのベースを生成する
        '''
        atx = self._facade.transaction_factory.create({
            'type': 'aggregateComplete',
            'signer_public_key': self._km.get_my_pubkey(),
            'fee': fee,
            'deadline': deadline,
            'transactions_hash': transactions_hash,
            'transactions': txs
        })
        return atx

    def get_merkle_hash(self, target_txs):
        '''
        配列で与えられたトランザクションからmerkle_hashを生成する
        '''
        hash_builder = MerkleHashBuilder()
        for tx in target_txs:
            hash_builder.update(Hash256(sha3.sha3_256(tx.serialize()).digest()))
        return hash_builder.final()

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
        signature = self._km.sign_tx(tx)
        tx.signature = signature.bytes
        payload = {"payload": hexlify(tx.serialize()).decode('utf8').upper()}
        json_payload = json.dumps(payload)
        return json_payload

    def send_tx(self, tx):
        '''
        指定されたトランザクションをSymbolネットワークに対して送信する
        '''
        payload = {"payload": hexlify(tx.serialize()).decode('utf8').upper()}
        json_payload = json.dumps(payload)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx)
        return (status, hash)

    def send_thanks_transacton(self, deadline, fee, target_address):
        '''
        指定されたアドレスの相手を「+1」するThanks TransactionをSymbolネットワークに対して送信する
        '''
        tmb = ThanksMessageBuilder()
        msg_txt = tmb.build_tm_string(target_address)
        service_address = self._facade.Address(THANKS_METER_SERVICE_ADDRESS).bytes
        tx = self._build_thanks_tx(deadline, fee, service_address, msg_txt)
        json_payload = self._build_req_tx_msg(tx)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx)
        return (status, hash)

    def send_mosaic_transacton(self, deadline, fee, recipient_address, mosaics, msg_txt):
        '''
        指定されたアドレスの相手にモザイクを送るためのトランザクションをSymbolネットワークに対して送信する
        '''
        tx2 = self._build_mosaic_tx(deadline, fee, recipient_address, mosaics, msg_txt)
        json_payload = self._build_req_tx_msg(tx2)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx2)
        return (status, hash)

    def send_mosaic_def_transacton(self, deadline, fee, duration, flags, divisibility):
        '''
        モザイク定義を行う
        '''
        tx3 = self._build_mosaic_def_tx( deadline, fee, duration, flags, divisibility)
        json_payload = self._build_req_tx_msg(tx3)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx3)
        return (status, hash)

    def send_mosaic_supply_change_tx(self, deadline, fee, delta, action):
        '''
        モザイク供給量の変更を行う
        '''
        tx4 = self._build_mosaic_supply_change(deadline, fee, delta, action)
        json_payload = self._build_req_tx_msg(tx4)
        status = self._nm.send_tx(json_payload)
        hash = self._get_transaction_hash(tx4)
        return (status, hash)

    def get_received_transactions_with_address(self, address, page_size = 10, page_num = 1):
        '''
        与えられたアドレスが受信したトランザクションを取得する
        '''
        return json.loads(self._nm.get_received_transactions_with_address(address, page_size, page_num))

    def get_sent_transactions(self, pubkey_string, page_size = 10, page_num = 1):
        '''
        自分が送信済のトランザクションを取得する
        '''
        return json.loads(self._nm.get_sent_transactions(pubkey_string, page_size, page_num))

    def get_tx_fee_info(self):
        '''
        トランザクション取り込み料金に関する情報を取得する
        '''
        return json.loads(self._nm.get_transaction_fee_info())

    def get_rental_fee_info(self):
        '''
        ネームスペースのレンタル料金に関する情報を取得する
        '''
        return json.loads(self._nm.get_rental_fee_info())

    def get_nw_properties_info(self):
        '''
        ネームスペースのレンタル料金に関する情報を取得する
        '''
        return json.loads(self._nm.get_nw_properties_info())

    def get_node_health_info(self):
        '''
        ネットワーク関連情報を取得する
        '''
        return json.loads(self._nm.get_node_health_info())

    def get_node_info(self):
        '''
        接続先ノードに関する情報を取得する
        '''
        return json.loads(self._nm.get_node_info())

    def get_unconfirmed_txs_with_pubkey(self, pubkey_string, page_size = 10, page_num = 1):
        '''
        指定した公開鍵を用いて生成された未承認のトランザクションデータを取得する
        '''
        return json.loads(self._nm.get_unconfirmed_txs_with_pubkey(pubkey_string, page_size, page_num))

    def _get_transaction_hash(self, tx):
        return self._facade.hash_transaction(tx)

    def get_transaction_status(self, hash):
        '''
        指定したトランザクションの状態を取得する
        '''
        return json.loads(self._nm.get_transaction_status(hash))