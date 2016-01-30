# -*- coding:utf-8 -*-
__author__ = 'john'
from M2Crypto import RSA



msg = 'aaaa-aaaa'

rsa_pub = RSA.load_pub_key('./keys/rsa_public_key.pem')

rsa_pri = RSA.load_key('./keys/rsa_private_key.pem')

print '*************************************************************'

print '公钥加密，私钥解密'


ctxt = rsa_pub.public_encrypt(msg, RSA.pkcs1_padding)

ctxt64 = ctxt.encode('base64')

print ('密文:%s'% ctxt64)

rsa_pri = RSA.load_key('./keys/rsa_private_key.pem')

txt = rsa_pri.private_decrypt(ctxt, RSA.pkcs1_padding)

print('明文:%s'% txt)



print '*************************************************************'

print '私钥加密，公钥解密'

ctxt_pri = rsa_pri.private_encrypt(msg, RSA.pkcs1_padding)

ctxt64_pri = ctxt.encode('base64')

print ('密文:%s'% ctxt64_pri)

txt_pri = rsa_pub.public_decrypt(ctxt_pri, RSA.pkcs1_padding)

print('明文:%s'% txt_pri)