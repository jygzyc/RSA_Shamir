# -*- coding:utf-8 -*-
import sys
import os
from rsa_shamir import RSA_Shamir
import time

def main():
    print(" _______ ______  _____ _______  ")
    print("|__   __|  ____|/ ____|__   __| ")
    print("   | |  | |__  | (___    | |    ")
    print("   | |  |  __|  \___ \   | |    ")
    print("   | |  | |____ ____) |  | |    ")
    print("   |_|  |______|_____/   |_|    ")
    print("\n\n")
    print("2. encrypt\n3. descrypt")
    choice = str(input("choose:  "))

    if choice == '2':
        filen = input("Please input the file name: ")
        # private_key = input("Please input the private key file name(.bin): ")
        public_key = input("Please input the public key file name(.pem): ")
        private_key = "temp.bin"
        rs = RSA_Shamir.RSA_Shamir()
        rs.rsa_createRSAKeys(private_key, public_key)
        rs.rsa_encrypt(filen, public_key)
        rs.shamir_encrypt(private_key, 7, 10)
    elif choice == '3':
        filen = input("Please input the file name: ")
        private_key = input("Please input the private key file name(.bin): ")
        rw = RSA_Shamir.RSA_Shamir()
        rw.shamir_descrypt(private_key, 10)
        rw.rsa_descrypt(filen, private_key)
    else:
        print("Goodbye!")
        exit(0)




def test():


    print(" _______ ______  _____ _______  ")
    print("|__   __|  ____|/ ____|__   __| ")
    print("   | |  | |__  | (___    | |    ")
    print("   | |  |  __|  \___ \   | |    ")
    print("   | |  | |____ ____) |  | |    ")
    print("   |_|  |______|_____/   |_|    ")
    print("\n\n")

    print("Please input the file name: ")
    filen = "head.jpg"
    # private_key = input("Please input the private key file name(.bin): ")
    print("Please input the public key file name(.pem): ")
    public_key = "pub.pem"
    private_key = "temp.bin"
    rs = RSA_Shamir.RSA_Shamir()
    rs.rsa_createRSAKeys(private_key, public_key)
    rs.rsa_encrypt(filen, public_key)
    rs.shamir_encrypt(private_key, 7, 10)
    time.sleep(20)
    print("Please input the file name: ")
    filenx = "head.jpg"
    print("Please input the private key file name(.bin): ")
    private_keyx = "pri.bin"
    rw = RSA_Shamir.RSA_Shamir()
    rw.shamir_descrypt(private_keyx, 10)
    rw.rsa_descrypt(filenx, private_keyx)


if __name__ == "__main__":
    main()
