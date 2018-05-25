from ctypes import *
from os import path
from exchange_app import app
import logging

###########################################################
#                  Types definitions
###########################################################

class GoString(Structure):
    _fields_ = [("p", c_char_p), 
                ("n", c_longlong)]    
    def __init__(self, string):
        self.p = c_char_p(string.encode(encoding = 'ansi'))
        self.n = len(string)
        
class GoSlice(Structure):
    _fields_ = [("data", c_void_p), 
                ("len", c_longlong), 
                ("cap", c_longlong)]

class cipher__Address(Structure):
    _fields_ = [("Version", c_ubyte), 
                ("Key", c_ubyte * 20)]
    
class cipher__PubKey(Structure):
    _fields_ = [("data", c_ubyte * 33)]

class cipher__SecKey(Structure):
    _fields_ = [("data", c_ubyte * 32)]    
    def __init__(self, string):
        self.data = (c_ubyte*32).from_buffer_copy('{:0>32}'.format(string[:32]).encode(encoding = 'ansi'))
    
class cipher__Sig(Structure):
    _fields_ = [("data", c_ubyte * 65)]
    
class cipher__SHA256(Structure):
    _fields_ = [("data", c_ubyte * 32)]    
    def __init__(self, string):
        self.data = (c_ubyte*32).from_buffer_copy('{:0>32}'.format(string[:32]).encode(encoding = 'ansi'))
  
class coin__Transaction(Structure):
    _fields_ = [("Length", c_int32), 
                ("Type", c_int8), 
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
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
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
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
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
    
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
    #Convert input to ctypes
    p0 = c_longlong(p0)
    p1 = GoString(p1)
    p2 = GoString(p2)
    p3 = GoString(p3)
    
    p5 = coin__Transaction()
    
    ret = skylib.SKY_cli_CreateRawTxFromAddress(p0, p1, p2, p3, p4, byref(p5))
    
    return ret


def CreateRawTxFromWallet(p0, p1, p2, p3):
    """
    Handle p0, GoString p1, GoString p2, GoSlice p3, coin__Transaction* p4
    """
    
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
    #Convert input to ctypes
    p0 = c_longlong(p0)
    p1 = GoString(p1)
    p2 = GoString(p2)

    p4 = coin__Transaction()
    
    ret = skylib.SKY_cli_CreateRawTxFromWallet(p0, p1, p2, p3, byref(p4))
    
    return ret

    
def CreateRawTx(p0, p1, p2, p3, p4):
    """
    Handle p0, wallet__Wallet* p1, GoSlice p2, GoString p3, GoSlice p4, coin__Transaction* p5
    """
    
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
    #Convert input to ctypes
    p0 = c_longlong(p0)
    p3 = GoString(p3)
    
    p5 = coin__Transaction()
    
    ret = skylib.SKY_cli_CreateRawTx(p0, byref(p1), p2, p3, p4, byref(p5))
    
    return ret
    
    
def SignHash(hash, secKey):
    """
    Sign the hash provided with the secKey, return the signed hash
    """
    
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
    
    signedHash = cipher__Sig()
    logging.debug(hash)
    logging.debug(secKey)
    skylib.SKY_cipher_SignHash(byref(cipher__SHA256(hash)), byref(cipher__SecKey(secKey)), byref(signedHash))
    
    return bytearray(signedHash).hex()
    
    
def GenerateDeterministicKeyPair(seed):
    """
    Generate a deterministic public/private key pair based on seed
    """
    
    skylib = cdll.LoadLibrary(path.relpath(app.config['LIBSKYCOIN_PATH']))
    
    string = c_char_p(seed.encode(encoding = 'ansi'))    
    length = len(seed)
    
    slice = GoSlice()
    slice.data = cast(string, c_void_p)
    slice.len = c_longlong(length)
    slice.cap = c_longlong(length)
    
    pubkey = cipher__PubKey()
    seckey = cipher__SecKey()
    
    skylib.SKY_cipher_GenerateDeterministicKeyPair(slice, byref(pubkey), byref(seckey))
    
    return (pubkey.data, seckey.data)
      
    
    
#extern void SKY_cipher_SignHash(cipher__SHA256* p0, cipher__SecKey* p1, cipher__Sig* p2);
#CreateRawTxFromAddress(40, "qwerrqwr", "dgdgdgdg", "hjhjhjhjh", GoSlice())

#CreateRawTxFromWallet(40, "qwerrqwr", "dgdgdgdg", GoSlice())

#CreateRawTx(40, wallet__Wallet(), GoSlice(), "dsdjfjdfdjfldjfljdf", GoSlice())

#(ret, result) = DecodeBase58Address("2HHjFnp8FgJzh87J36pCuDhDYtUBMPEgomZ")
#for bt in result:
#    print(hex(bt))
#    
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
#{'_id': ObjectId('5a866b13cf105916e4180cb9'), 'meta': {'coin': 'skycoin', 'filename': '2018_02_16_3fe6.wlt', 'label': 'wallet123', 'lastSeed': '83281765eccf5efed260b261d4c7ac621b202e95b6593680ba5662f0c2c5a274', 'seed': 'pass cactus woman shop lunch city ankle menu affair conduct column trade', 'tm': '1518758675', 'type': 'deterministic', 'version': '0.1'}, 'entries': [{'address': 'xTaXPcDrZjBPqjJA7Y9eC5SLK3fyHh1cMw', 'public_key': '02a30c94c8f1152f71b7a4fc2ee5e5fcdc697689a32aab1a77b6c7423bdba976e1', 'secret_key': '6724e307f28cb05802ddaafca64e92ebc4aed02ffa9c756dbc4b8b735db3e288'}]}

#(pubkey, seckey) = GenerateDeterministicKeyPair("pass cactus woman shop lunch city ankle menu affair conduct column trade");
#
#print(bytearray(pubkey).hex() )
#print(bytearray(seckey).hex() )






