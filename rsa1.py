import hashlib
from base64 import b64decode, b64encode

from Crypto.PublicKey import RSA
from hashlib import sha256

#keyPair = RSA.generate(bits=1024)
#exp = keyPair.exportKey
#print("exp:",str(exp))
#print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
#print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")
from Crypto.Signature import PKCS1_v1_5
from cryptography.hazmat.primitives.hashes import SHA256


def sign(message, private_key):
    key = RSA.importKey(private_key)
    hash = int.from_bytes(sha256(message).digest(), byteorder='big')
    signature = pow(hash, key.d, key.n)
    print("Signature:", signature)
    print("Signature HEX:",hex(signature))
    return signature

def verify(message, signature, key):
    print("Verifying:", signature)

    hash = int.from_bytes(sha256(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, key.e, key.n)
    print("Signature valid:", hash == hashFromSignature)


pkhex='30820153020100300d06092a864886f70d01010105000482013d30820139020100024100e707d1061a59536eede05c2bfa33e1e9551cb309327bbcf3cf67d2e477952188167e75dc1f1484092ddf795fd4e7522d7f1a3442231655bde543edc7ceff72030203010001024032fdedabbc2b151839d6b8615883150ccc255e7adc32a57ce6bd52b5ec92f4e84a39a5e083a77f38f972992230d7769a0f14147025cbe635e34c2bcdc2b195d1022100f63ca2f7d5966908323a8a129a81efc2f81dc4e33e5ee28c86b23fbe6a676a49022100f030d4feb35c76c6d9eb6ed19750eaf6bc53376362710c31e42fe5ae1931d9eb02201acbe6804a022054000356db476d34866731f62734b666b91c3f71a86b33ede102202abad53996990d7c64ca5085b2e0af5c43b69e34ed0f6576febc52a4fd50740f0220588138b9e15a015b4130c4176467e683ab194901a404eea48533ab6f1a556775'
print("PKHEX:",pkhex)
pkb = bytes.fromhex(pkhex)
print("PKB:",pkb)
privKeyObj = RSA.import_key(pkb)
print(privKeyObj.size_in_bytes())
print(privKeyObj.size_in_bits())
print(privKeyObj.can_sign())



msg = b'A message for signing'
print("____________________________")
print(msg)

sig = sign(msg,pkb)
print("Sig type:", type(sig))

verify(msg, sig, privKeyObj)


if "BUY" in ("SELL","BUY"): print("Status not supported")

