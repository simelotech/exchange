from ctypes import *
from os import path
#import logging


###########################################################
#                  Types definitions
###########################################################

class GoString(Structure):
    _fields_ = [("p", c_char_p), 
                ("n", c_int)]
    
    def __init__(self, string):
        self.p = c_char_p(string.encode(encoding = 'ansi'))
        self.n = len(string)
        
class GoSlice(Structure):
    _fields_ = [("data", c_void_p), 
                ("len", c_int), 
                ("cap", c_int)]

class cipher__Address(Structure):
    _fields_ = [("Version", c_ubyte), 
                ("Key", c_ubyte * 20)]
    
class cipher__PubKey(Structure):
    _fields_ = [("data", c_ubyte * 33)]

class cipher__SecKey(Structure):
    _fields_ = [("data", c_ubyte * 32)]
    
class cipher__Sig(Structure):
    _fields_ = [("data", c_ubyte * 65)]
    
class cipher__SHA256(Structure):
    _fields_ = [("data", c_ubyte * 32)]
  
class coin__Transaction(Structure):
    _fields_ = [("Length", c_int), 
                ("Type", c_char), 
                ("InnerHash", cipher__SHA256), 
                ("Sigs", GoSlice), 
                ("In", GoSlice), 
                ("Out", GoSlice)]

class wallet__Wallet(Structure):
    _fields_ = [("Meta", c_void_p), 
                ("Entries", GoSlice)]
    
    
    
###########################################################
#                  Business functions
###########################################################

def DecodeBase58Address(addr):
    """
    GoString p0, cipher__Address* p1
    """
    
    #skylib = cdll.LoadLibrary(path.relpath('./exchange_app/libskycoin.so'))
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    addr = GoString(addr)
    cypher_addr = cipher__Address()
    #print(addr.n)
    #print(addr.p)
    result = skylib.SKY_cipher_DecodeBase58Address(addr, byref(cypher_addr))
    
    #print(cast(cypher_addr.Key, c_char_p).value)
    
    return (result, cypher_addr.Key)
    
    
def GenerateKeyPair():
    """
    cipher__PubKey* p0, cipher__SecKey* p1
    """

    #skylib = cdll.LoadLibrary(path.relpath('./exchange_app/libskycoin.so'))
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    public_key = cipher__PubKey()
    private_key = cipher__SecKey()
    
    ret = skylib.SKY_cipher_GenerateKeyPair(byref(public_key), byref(private_key))
    #print(public_key.data)
    #print(private_key.data)
    
    return (ret, public_key.data, private_key.data)
    

def CreateRawTxFromAddress(p0, p1, p2, p3, p4):
    """
    Handle p0, GoString p1, GoString p2, GoString p3, GoSlice p4, coin__Transaction* p5
    """
    
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    #Convert input to ctypes
    p0 = c_longlong(p0)
    p1 = GoString(p1)
    p2 = GoString(p2)
    p3 = GoString(p3)
    
    p5 = coin__Transaction()
    
    ret = skylib.SKY_cli_CreateRawTxFromAddress(p0, p1, p2, p3, p4, byref(p5))
    
    print(ret)


def CreateRawTxFromWallet(p0, p1, p2, p3):
    """
    Handle p0, GoString p1, GoString p2, GoSlice p3, coin__Transaction* p4
    """
    
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    #Convert input to ctypes
    p0 = c_longlong(p0)
    p1 = GoString(p1)
    p2 = GoString(p2)

    p4 = coin__Transaction()
    
    ret = skylib.SKY_cli_CreateRawTxFromWallet(p0, p1, p2, p3, byref(p4))
    
    print(ret)

    
def CreateRawTx(p0, p1, p2, p3, p4):
    """
    Handle p0, wallet__Wallet* p1, GoSlice p2, GoString p3, GoSlice p4, coin__Transaction* p5
    """
    
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    #Convert input to ctypes
    p0 = c_longlong(p0)
    p3 = GoString(p3)
    
    p5 = coin__Transaction()
    
    ret = skylib.SKY_cli_CreateRawTx(p0, byref(p1), p2, p3, p4, byref(p5))
    
    print(ret)
    
    
def SignHash(p0, p1, p2):
    """
    cipher__SHA256* p0, cipher__SecKey* p1, cipher__Sig* p2
    """
    
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    skylib.SKY_cipher_SignHash(byref(p0), byref(p1), byref(p2))
    
    print(p2)
    
    
def GenerateDeterministicKeyPairsSeed(p0, p1):
    """
    GoSlice p0, GoInt p1, cipher__PubKeySlice* p2, cipher__PubKeySlice* p3
    """
    
    skylib = cdll.LoadLibrary(path.relpath('../libskycoin.so'))
    
    pubkey1 = GoSlice()
    pubkey2 = GoSlice()
    
    skylib.SKY_cipher_GenerateDeterministicKeyPairsSeed(p0, c_int(p1), byref(pubkey1), byref(pubkey2))
    
    print(pubkey1.cap)
    
    
    
    
#CreateRawTxFromAddress(40, "qwerrqwr", "dgdgdgdg", "hjhjhjhjh", GoSlice())

#CreateRawTxFromWallet(40, "qwerrqwr", "dgdgdgdg", GoSlice())

#CreateRawTx(40, wallet__Wallet(), GoSlice(), "dsdjfjdfdjfldjfljdf", GoSlice())

(ret, result) = DecodeBase58Address("2HHjFnp8FgJzh87J36pCuDhDYtUBMPEgomZ")
for bt in result:
    print(hex(bt))
    
#SignHash(cipher__SHA256(), cipher__SecKey(), cipher__Sig())
#(ret, public, private) = GenerateKeyPair()
#for pub in public:
#    print(hex(pub))
#print()
#for prv in private:
#    print(hex(prv))
#
#print(private.decode(encoding = 'ansi'))

#GenerateDeterministicKeyPairsSeed(GoSlice(), 5)

print("\n", ret)





