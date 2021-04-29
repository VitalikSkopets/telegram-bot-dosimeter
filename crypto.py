import rsa


def crypto() -> None:
    (pubkey, privkey) = rsa.newkeys(512, accurate=False)
    pubkey_pem = pubkey.save_pkcs1()
    privkey_pem = privkey.save_pkcs1()
    with open('private.pem', mode='wb') as privatefile, open(r'public.pem', mode='wb') as publicfile:
        privatefile.write(privkey_pem)
        publicfile.write(pubkey_pem)
    return None


def decoder(token: bytes) -> str:
    with open('private.pem', mode='rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    line = rsa.decrypt(token, privkey)
    return line.decode('utf8')


if __name__ == '__main__':
    # crypto()
    decoder()
