# EncryFile
encrypt/decrypt files

you need:
1.Django

RSA私钥及公钥生成

Linux用户（以Ubuntu为例）
$ openssl 进入OpenSSL程序
OpenSSL> genrsa -out rsa_private_key.pem 1024 生成私钥
OpenSSL> pkcs8 -topk8 -inform PEM -in rsa_private_key.pem -outform PEM -nocrypt Java开发者需要将私钥转换成PKCS8格式
OpenSSL> rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem 生成公钥
OpenSSL> exit ## 退出OpenSSL程序

Windows用户在cmd窗口中进行以下操作：
C:\Users\Hammer>cd C:\OpenSSL-Win32\bin 进入OpenSSL安装目录
C:\OpenSSL-Win32\bin>openssl.exe 进入OpenSSL程序
OpenSSL> genrsa -out rsa_private_key.pem 1024 生成私钥
OpenSSL> pkcs8 -topk8 -inform PEM -in rsa_private_key.pem -outform PEM -nocrypt Java开发者需要将私钥转换成PKCS8格式
OpenSSL> rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem 生成公钥
OpenSSL> exit ## 退出OpenSSL程序

*.pem 放到 /secret/rsa/keys/

Ubuntu:
python manage.py runserver

