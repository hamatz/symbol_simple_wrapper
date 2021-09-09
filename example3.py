import sys
import datetime
import json
from utils.wallet import SimpleWallet

def main(network_id, pass_phrase, key_file_name):
    wallet = SimpleWallet(network_id, key_file_name, pass_phrase)
    address = wallet.get_my_address()
    print('Here is your address: ' , address)
    pubkey = wallet.get_my_pubkey_string()
    print('Here is your pubkey: ' , pubkey)

    h_address = wallet.get_hex_address(address)
    print(h_address.decode())

    uh_address = wallet.get_unhexed_address(h_address)
    print(uh_address)

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