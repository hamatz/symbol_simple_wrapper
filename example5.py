import sys
import datetime
import json
from utils.wallet import SimpleWallet

import secrets

def main(network_id, pass_phrase, key_file_name):
	'''
	時間が経ってからモザイクの総量を変更したい場合のサンプル
	'''
    wallet = SimpleWallet(network_id, key_file_name, pass_phrase)
    address = wallet.get_my_address()
    pubkey = wallet.get_my_pubkey_string()

    deadline = (int((datetime.datetime.today() + datetime.timedelta(hours=2)).timestamp()) - 1616694977) * 1000
    fee = 1000000
    delta = 500000000
    action = 'increase'
    # 前回発行時に利用した nonce を確認（or記録）しておく必要がある
    nonce = 1716914431
    wallet.set_mosaic_nonce(nonce)
    result = wallet.send_mosaic_supply_change_tx(deadline, fee, delta, action)
    print(result[0])

    account_info = wallet.check_my_account_info_with_address()
    a_info = account_info[0]['account']
    print(json.dumps(account_info, indent=2))

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 4:
        network_id = int(args[1])
        pass_phrase = args[2]
        key_file_name = args[3]
    else:
        print('Param Error')
        print('$ example3.py <network_id> <pass_phrase> <key_file_name>')
        quit()

    main(network_id, pass_phrase, key_file_name)