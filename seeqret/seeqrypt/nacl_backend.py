from nacl.hash import sha256
from nacl.public import PrivateKey, Box, PublicKey
from nacl import encoding
from nacl.signing import SigningKey

from seeqret.utils import write_binary_file, read_binary_file


def generate_private_key(fname=None) -> PrivateKey:
    pkey = PrivateKey.generate()
    if fname:
        write_binary_file(
            fname,
            encoding.Base64Encoder.encode(pkey._private_key),
        )
    return pkey


def load_private_key(fname: str) -> PrivateKey:
    key = PrivateKey(read_binary_file(fname), encoder=encoding.Base64Encoder)
    return key


def load_public_key(fname: str) -> PublicKey:
    key = PublicKey(read_binary_file(fname), encoder=encoding.Base64Encoder)
    return key


def save_public_key(fname: str, pkey: PrivateKey) -> bytes:
    pubkey = encoding.Base64Encoder.encode(bytes(pkey.public_key))
    write_binary_file(fname, pubkey)
    return pubkey


def private_key(string: bytes) -> PrivateKey:
    return PrivateKey(string, encoder=encoding.Base64Encoder)


def public_key(string: str) -> PublicKey:
    return PublicKey(string.encode('ascii'), encoder=encoding.Base64Encoder)


def asymetric_encrypt_string(string: str,
                             sender_private_key: PrivateKey,
                             recipient_public_key: PublicKey) -> str:
    box = Box(
        private_key=sender_private_key,
        public_key=recipient_public_key
    )
    val = string.encode('utf-8')
    return encoding.Base64Encoder.encode(box.encrypt(val)).decode('ascii')


def asymetric_decrypt_string(string: str,
                             receiver_private_key: PrivateKey,
                             sender_public_key: PublicKey) -> str:
    box = Box(
        private_key=receiver_private_key,
        public_key=sender_public_key
    )
    val = string.encode('ascii')
    return box.decrypt(encoding.Base64Encoder.decode(val)).decode('ascii')


def sign_message(string: bytes):
    signing_key = SigningKey.generate()
    signed = signing_key.sign(string)
    verify_key = signing_key.verify_key
    verify_key_bytes = verify_key.encode()
    return verify_key_bytes, signed


def hash_message(string: bytes) -> str:
    return sha256(string, encoder=encoding.Base64Encoder).decode('ascii')
