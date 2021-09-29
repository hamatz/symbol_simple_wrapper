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

    #  base32ToHexAddress変換
    h_address = wallet.get_hex_address(address)
    print(h_address.decode())

    #  base32ToHexAddress逆変換
    uh_address = wallet.get_unhexed_address(h_address)
    print(uh_address)


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
