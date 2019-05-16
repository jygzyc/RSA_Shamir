# -*- coding: utf-8 -*-
# %%

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

from Crypto.PublicKey import RSA

from .SecretSharing.sharing import PlaintextToHexSecretSharer
import threading
import os
import time
import base64
# %%


class RSA_Shamir(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        """
        This class contains RSA and Shamir methods.
        And this class is of singleton pattern.
        :param code: this is the secert key of generate RSA keys.
        :copyright: 2019
        :author: ZYC
        """
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(RSA_Shamir, "_instance"):
            with RSA_Shamir._instance_lock:
                if not hasattr(RSA_Shamir, "_instance"):
                    RSA_Shamir._instance = object.__new__(cls)
        return RSA_Shamir._instance

    def rsa_createRSAKeys(self, private_key_file, public_key_file):
        """
        Create RSA keys
        :param private_key_file: the file name of private key
        :param public_key_file: the file name of public key
        """
        code = "6a79677a"
        key = RSA.generate(2048)
        encrypted_key = key.exportKey(
            passphrase=code,
            pkcs=8,
            protection="scryptAndAES128-CBC"
        )
        # 生成私钥
        with open(private_key_file, 'wb') as f:
            f.write(encrypted_key)
        # 生成公钥
        with open(public_key_file, 'wb') as f:
            f.write(key.publickey().exportKey())

    def rsa_encrypt(self, filename, public_key_file):
        """
        RSA encrypt function
        :param filename: the file needed to be encrypted
        :param public_key_file: the RSA public key file
        """
        
        data = ''
        with open(filename, 'rb') as f:
            data = f.read()

        with open(filename, 'wb') as out_file:
            recipent_key = RSA.import_key(
                open(public_key_file).read()
            )
            session_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(recipent_key)
            out_file.write(cipher_rsa.encrypt(session_key))

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            out_file.write(cipher_aes.nonce)
            out_file.write(tag)
            out_file.write(ciphertext)

    def rsa_descrypt(self, filename, private_key_file):
        """
        RSA descrypt function
        :param filename: the file needed to be descrypted
        :param pwd: the secret RSA code
        :param private_key_file: the RSA private key file
        """
        code = "6a79677a"
        with open(filename, 'rb') as fobj:
            private_key = RSA.import_key(
                open(private_key_file).read(),
                passphrase=code
            )
            enc_session_key, nonce, tag, cipertext = [
                fobj.read(x)
                for x in (private_key.size_in_bytes(), 16, 16, -1)
            ]
            ciper_rsa = PKCS1_OAEP.new(private_key)
            session_key = ciper_rsa.decrypt(enc_session_key)
            ciper_aes = AES.new(session_key, AES.MODE_EAX, nonce)

            data = ciper_aes.decrypt_and_verify(cipertext, tag)
            
        with open(filename, 'wb') as wobj:
            wobj.write(data)

    def shamir_encrypt(self, key_file, num, sum):
        """
        secret sharing encrypting with shamir
        :param key_file: key file needed encrypt
        :param num: you can descrypt the file with "num" files
        :param sum: the sum of shamir files
        """
        def share_fn(x):
            """
            创建shamir密钥文件名
            """
            x = x + "_shamir_key.bin"
            return x

        sh_filen = [str(x) for x in range(1, sum + 1)]
        fi_filen = list(map(share_fn, sh_filen))
        for i in fi_filen:
            if os.path.exists(i) is True:
                os.remove(i)
        with open(key_file, 'rb') as kf:
            kf_file = kf.readline()
            while(kf_file):
                share_text = PlaintextToHexSecretSharer.\
                    split_secret(bytes.decode(kf_file), num, sum)
                i = 0
                for text in share_text:
                    with open(fi_filen[i], 'a+') as fi_file:
                        fi_file.write(text + "\n")
                    i = i + 1
                kf_file = kf.readline()

        os.remove(key_file)

    def shamir_descrypt(self, filename, sum):
        """
        secret sharing descrypting with shamir
        :param filename: the complete RSA key file name that you want
        :param sum: the share file sum number
        """
        def share_fn(x):
            """
            创建shamir密钥文件名
            """
            x = x + "_shamir_key.bin"
            return x

        sh_filen = [str(x) for x in range(1, sum + 1)]
        fi_filen = list(map(share_fn, sh_filen))

        if os.path.exists(filename) is True:
            os.remove(filename)

        try:
            sum_temp = []
            for sh_file in fi_filen:
                if os.path.exists(sh_file):
                    with open(sh_file, 'r') as f:
                        temp = []
                        for line in f.readlines():
                            temp.append(line.rstrip("\n"))
                        sum_temp.append(temp)
            for i in range(len(sum_temp[0])):
                text = []
                for j in range(len(sum_temp)):
                    text.append(sum_temp[j][i])
                text = PlaintextToHexSecretSharer.recover_secret(text)
                text = str.encode(text)
                with open(filename, 'ab') as f:
                    f.write(text)

        except:
            raise IOError
        
        for fn in fi_filen:
            if os.path.exists(fn) is True:
                os.remove(fn)


