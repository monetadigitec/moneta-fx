from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

# Generate 1024-bit RSA key pair (private + public key)

pkhex='30820155020100300d06092a864886f70d01010105000482013f3082013b020100024100f4bb75e5ab8d9cade26b3a519940bccf3abad9b1b5bd4d3aec1aff4e4680020110f2a0e64728da798004633deadbeada08963cc54e93f65cc4d725fb5967a60502030100010241009d9503622267a9e6512f883ab87a75d8ddd12891841b635a38635dd7321004b916a3debe01dac98bc86410e0f12373cedf43429adfefd96ab18de6269714c5a1022100fe9abba3267204e83d1da8e400b553a87bfdc41a703ff2c3396e40def07e767d022100f612dfee362152b4203855314036b5a8531d607ddd2a43262a84a6a5bac51c2902210099425754dc5da22a922f7a6cd5285195881db7a01a95c3f2546dd3cadf85a099022063a77f32ac8f503c0c7463e3ff3a68d5135be950efb986da350be5a5667f1f09022018bb11a92ef6bdeecc366a01df2e4681b3e47428e7d35fd6ddc45c7dba378b9d'
print("PKHEX:",pkhex)
pkb = bytes.fromhex(pkhex)
print("PKB:",pkb)
privKeyObj = RSA.import_key(pkb)

pubKeyn = privKeyObj.publickey()

# Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
msg = b'A message for signing'
hash = SHA256.new(msg)
signer = PKCS115_SigScheme(privKeyObj)
signature = signer.sign(hash)
print("SIG RAW:", signature)
print("SIG RAW HEX:", signature.hex())
print("Signature:", binascii.hexlify(signature))
print("SIG HEX:",binascii.hexlify(signature).hex())

# Verify valid PKCS#1 v1.5 signature (RSAVP1)
msg = b'A message for signing'
hash = SHA256.new(msg)
verifier = PKCS115_SigScheme(pubKeyn)
try:
    verifier.verify(hash, signature)
    print("Signature is valid.")
except:
    print("Signature is invalid.")

# Verify invalid PKCS#1 v1.5 signature (RSAVP1)
msg = b'A tampered message'
hash = SHA256.new(msg)
verifier = PKCS115_SigScheme(pubKeyn)
try:
    verifier.verify(hash, signature)
    print("Signature is valid.")
except:
    print("Signature is invalid.")