import hashlib,json
from datetime import datetime, timedelta
import time

class Block:
    def __init__(self, data,prev_hash=""):
        self.data = data
        self.nonce = 0
        self.prev_hash = prev_hash
        self._hash = ""  
        self.create_time = datetime.now()
        self.total_time = timedelta()

    def calculate_hash(self):
        data = json.dumps(self.data) + self.prev_hash + str(self.nonce)
        data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    def mine_block(self, difficulty=10):
        start = time.time()
        while self.calculate_hash()[:difficulty] != '0' * difficulty:
            self.nonce += 1
        end = time.time()
        self.total_time = timedelta(seconds=(end - start))
        self._hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = []

        genesis_block = Block("Genesis Block")
        genesis_block.mine_block()
        self.chain.append(genesis_block)

    def add_block(self, data):
        block = Block(data, self.chain[-1]._hash) 
        block.mine_block()
        self.chain.append(block)

    def print_blocks(self):
        for block in self.chain:
            print("")
            print("Data: ",block.data)
            print("Previous hash:", block.prev_hash)
            print("Hash: ",block._hash)
            print("Nonce: ",block.nonce)
            print("Created time: ",block.create_time)
            print("Total time: ",block.total_time)
            print("")

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if current_block.calculate_hash() != current_block._hash:
                return False
            if prev_block._hash != current_block.prev_hash:
                return False
        return True

    def get_balance(self, person):
        balance = 0
        for block in self.chain:
            if isinstance(block.data, list):
                for transfer in block.data:
                    if transfer["from"] == person:
                        balance -= transfer["amount"]
                    if transfer["to"] == person:
                        balance += transfer["amount"]
        return balance

blockchain = Blockchain()
blockchain.add_block([{"from":"Hieu", "to":"Jame","amount":1000},
                      {"from":"Marry", "to":"Judy","amount":3000},
                      {"from":"Judy", "to":"Jame","amount":1000}])


blockchain.add_block([{"from":"Jame", "to":"Harry","amount":20},
                     {"from":"Jame", "to":"Potter","amount":100},
                     {"from":"Jame", "to":"Batman","amount":100}])
print("Balance of Jame: ", blockchain.get_balance("Jame"), "HIU")
blockchain.print_blocks()
print("Is blockchain valid?", blockchain.is_valid())