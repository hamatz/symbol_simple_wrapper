import sys
import datetime
import time
from binascii import hexlify, unhexlify
from utils.wallet import SimpleWallet

def main(network_id, pass_phrase, key_file_name):
	'''
	アグリゲートトランザクション送信のサンプル
	中継サーバがトランザクション取り込みのfeeを払ってクライアントから受け取ったデータを
	書き込むような流れをイメージ
	'''

    wallet = SimpleWallet(network_id, key_file_name, pass_phrase)
    address = wallet.get_my_address()
    print('Here is your address: ' , address)
    pubkey = wallet.get_my_pubkey_string()
    print('Here is your pubkey: ' , pubkey)

    wallet2 = SimpleWallet(network_id, None, pass_phrase)
    address2 = wallet2.get_my_address()
    pubkey2 = wallet2.get_my_pubkey_string()
    second_key_file = key_file_name + '2'
    wallet2.save_my_key(second_key_file)

    bobPubkey = wallet.get_pubkey_from_str(pubkey2)
    alicePubkey = wallet.get_pubkey_from_str(pubkey)

	# ユーザが指定した相手に「+1」するためのトランザクションの素を作る
    bobTx = wallet2.get_thanks_tx_base(bobPubkey, address)
    # システム側が接続してきたユーザを「+1」するためのトランザクションの素を作る
    aliceTx = wallet2.get_thanks_tx_base(alicePubkey, address2)
    txs = [aliceTx, bobTx]
    merkle_hash = wallet.get_merkle_hash(txs)

    deadline = (int((datetime.datetime.today() + datetime.timedelta(hours=2)).timestamp()) - 1616694977) * 1000
    fee = 1000000

    aggregate = wallet.get_aggregate_tx_base(deadline, fee, merkle_hash, txs)
    signature = wallet.sign_tx(aggregate)
    aggregate.signature = signature.bytes

    hash = wallet.hash_transaction(aggregate).bytes
    hexlifiedHash = hexlify(hash)
    #本当はこのハッシュ値をユーザに送信するイメージ 
    print(hexlifiedHash)

	#ハッシュ値を受け取ったユーザ側で行うデジタル署名のイメージ 
    hexlifiedSignedHash = str(wallet2.compute_signature(unhexlify(hexlifiedHash)))
    print(hexlifiedSignedHash)

	#ユーザから送付されたデジタル署名をアグリゲートトランザクションに付与 
    cosignature = (0, bobPubkey.bytes, unhexlify(hexlifiedSignedHash))
    aggregate.cosignatures.append(cosignature)

    print(aggregate)

    (result, tx_hash) = wallet.send_tx(aggregate)
    print(result)

    # すぐ確認しようとすると no resource exists になるのでちょっと待ったらステータスが見えるようになった
    time.sleep(3.0)

    status = wallet.get_transaction_status(str(tx_hash))
    print(status)

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 4:
        network_id = int(args[1])
        pass_phrase = args[2]
        key_file_name = args[3]
    else:
        print('Param Error')
        print('$ example6.py <network_id> <pass_phrase> <key_file_name>')
        quit()

    main(network_id, pass_phrase, key_file_name)