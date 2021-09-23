import sys
from utils.wallet import SimpleWallet

def main(network_id, pass_phrase, key_file_name):
    wallet = SimpleWallet(network_id, None, pass_phrase)
    address = wallet.get_my_address()
    pubkey = wallet.get_my_pubkey_string()
    print('keyPair was created! Here is your address: ' , address)
    print('keyPair was created! Here is your pubkey: ' , pubkey)
    wallet.save_my_key(key_file_name)

if __name__ == '__main__':
    '''
    秘密鍵を生成し、指定されたパスフレーズで暗号化したのち指定されたファイル名で保存する

    #本コードは常に新規の鍵を生成するので大事な鍵ファイル名を上書きしてしまわないよう注意
    '''
    args = sys.argv

    if len(args) == 4:
        network_id = int(args[1])
        pass_phrase = args[2]
        key_file_name = args[3]
    else:
        print('Param Error')
        print('$ keygen_example.py <network_id> <pass_phrase> <key_file_name>')
        quit()

    main(network_id, pass_phrase, key_file_name)
