import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"action": "genesis"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, prev.hash)
        self.chain.append(new_block)

    def to_dict(self):
        return [vars(b) for b in self.chain]
