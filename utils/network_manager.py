import json
import http.client
from symbolchain.core.facade.SymFacade import SymFacade

PUBLIC_TEST = 'public_test'
PUBLIC = 'public'

TETNET_HOST = 'sym-test-01.opening-line.jp'
TESTNET_TARGET_PORT = '3000'
MAINTET_HOST = 'node.xembook.net'
MAINNET_TARGET_PORT = '3000'

class SymbolNetworkManager:
    """
    class for managing the endpoint and calling APIs
    """
    def __init__(self, network_id):
        print('Initializing SymbolNetworkManager...')
        if network_id == 0:
            self._facade = SymFacade(PUBLIC_TEST)
            self._host_name = TETNET_HOST
            self._target_port = TESTNET_TARGET_PORT
        else:
            self._facade = SymFacade(PUBLIC)
            self._host_name = MAINTET_HOST
            self._target_port = MAINNET_TARGET_PORT

    def get_facade(self):
        return self._facade

    def send_accounts_info_req(self, req_msg):
        json_req_msg = json.dumps(req_msg)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("POST", "/accounts", json_req_msg, headers)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def send_tx(self, json_payload):
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("PUT", "/transactions", json_payload,headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        print(data.decode())
        return response.status

    def get_received_transactions_with_address(self, address, page_size = 10, page_num = 1):
        req_path = '/transactions/confirmed?recipientAddress=' + address + '&pageSize=' + str(page_size) + '&pageNumber=' + str(page_num)
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_sent_transactions(self, pubkey_string, page_size = 10, page_num = 1):
        req_path = '/transactions/confirmed?signerPublicKey=' + pubkey_string + '&pageSize=' + str(page_size) + '&pageNumber=' + str(page_num)
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_transaction_fee_info(self):
        req_path = '/network/fees/transaction'
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_rental_fee_info(self):
        req_path = '/network/fees/rental'
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_nw_properties_info(self):
        req_path = '/network/properties'
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_node_health_info(self):
        req_path = '/node/health'
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_node_info(self):
        req_path = '/node/info'
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_unconfirmed_txs_with_pubkey(self, pubkey_string, page_size = 10, page_num = 1):
        req_path = '/transactions/unconfirmed?signerPublicKey=' + pubkey_string + '&pageSize=' + str(page_size) + '&pageNumber=' + str(page_num)
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()

    def get_transaction_status(self, hash):
        req_path = '/transactionStatus/' + hash
        conn = http.client.HTTPConnection(self._host_name, self._target_port)
        conn.request("GET", req_path)
        response = conn.getresponse()
        data = response.read()
        return data.decode()