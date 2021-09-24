import sys
import datetime
import json
from utils.wallet import SimpleWallet

def main(network_id, pass_phrase, key_file_name):
	'''
	1. 自分のアドレス、公開鍵の確認
	2. 自分のアカウント情報（残高等）の確認
	3. 受信した最新100までのトランザクションの確認
	4. 現在のトランザクションfeeの確認
	5. Thanks Meterへの「+1」メッセージの送信（自分宛）
	6. 送信トランザクション（最新100）の確認
	'''
    wallet = SimpleWallet(network_id, key_file_name, pass_phrase)
    address = wallet.get_my_address()
    print('Here is your address: ' , address)
    pubkey = wallet.get_my_pubkey_string()
    print('Here is your pubkey: ' , pubkey)
    print('Here is your account info')
    account_info = wallet.check_my_account_info_with_address()
    print(json.dumps(account_info, indent=2))
    print('Here is your received transactions (latest 100)')
    txs = wallet.get_received_transactions_with_address(address, 100)
    print(json.dumps(txs, indent=2))
    print('Here is current transaction fee')
    tx_fee = wallet.get_tx_fee_info()
    print(json.dumps(tx_fee, indent=2))

    deadline = (int((datetime.datetime.today() + datetime.timedelta(hours=2)).timestamp()) - 1616694977) * 1000
    fee = 1000000
    result = wallet.send_thanks_transacton(deadline, fee, address)
    print(result[0])
    tx_status = wallet.get_transaction_status(str(result[1]))
    print(json.dumps(tx_status, indent=2))

    sent_transactions = wallet.get_sent_transactions(pubkey, 100)
    print('Here is your sent transactions (latest 100)')
    print(json.dumps(sent_transactions, indent=2))

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 4:
        network_id = int(args[1])
        pass_phrase = args[2]
        key_file_name = args[3]
    else:
        print('Param Error')
        print('$ example2.py <network_id> <pass_phrase> <key_file_name>')
        quit()

    main(network_id, pass_phrase, key_file_name)