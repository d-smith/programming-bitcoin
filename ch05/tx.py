
from helper import (
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    encode_varint,
    read_varint
)

from script import Script


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime  = locktime
        self.testnet = testnet
    
    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime:{}'.format(
            self.id(), self.version, tx_ins, tx_outs, self.locktime)
    
    def id(self):
        '''Human readable version of tx hash'''
        return self.hash().hex()
    
    def hash(self):
        return hash256(self.serialize())[::-1]
    
    @classmethod
    def parse(cls, stream,testnet=False):
        version = little_endian_to_int(stream.read(4))
        num_inputs = read_varint(stream)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(stream))
        return cls(version, inputs, None, None, testnet=testnet)
    
class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:  # <1>
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_input at the start
        return a TxIn object
        '''
        # prev_tx is 32 bytes, little endian
        # prev_index is an integer in 4 bytes, little endian
        # use Script.parse to get the ScriptSig
        # sequence is an integer in 4 bytes, little-endian
        # return an instance of the class (see __init__ for args)
        prev_tx = s.read(32)[::-1]
        prev_index = little_endian_to_int(s.read(4))
        script_sig = Script.parse(s)
        sequence = little_endian_to_int(s.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)
    
class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)
    # end::source3[]

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_output at the start
        return a TxOut object
        '''
        # amount is an integer in 8 bytes, little endian
        # use Script.parse to get the ScriptPubKey
        # return an instance of the class (see __init__ for args)
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)

    # tag::source4[]
    def serialize(self):  # <1>
        '''Returns the byte serialization of the transaction output'''
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result
        