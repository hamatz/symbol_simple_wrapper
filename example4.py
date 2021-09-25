import sys
import datetime
import json
from utils.wallet import SimpleWallet

import secrets

def main(network_id, pass_phrase, key_file_name):
	'''
	モザイクの新規発行と初期供給総量の定義
	'''
    wallet = SimpleWallet(network_id, key_file_name, pass_phrase)
    address = wallet.get_my_address()
    pubkey = wallet.get_my_pubkey_string()

    deadline = (int((datetime.datetime.today() + datetime.timedelta(hours=2)).timestamp()) - 1616694977) * 1000
    fee = 1000000
    # モザイクの新規発行にあたっての各種定義
    duration = 365
    flags = 'transferable restrictable supply_mutable'
    divisibility = 2
    result = wallet.send_mosaic_def_transacton(deadline, fee, duration, flags, divisibility)
    print(result[0])

	# モザイクの発行総量を定義する。全てが発行者所有となる
    delta = 100000
    action = 'increase'
    result2 = wallet.send_mosaic_supply_change_tx(deadline, fee, delta, action)

	'''
	自分のアカウント情報の確認。通常、このタイミングではトランザクションの反映は行われておらず
	新規発行分は見えない
	'''
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