# -*- coding:utf-8 -*-
from django.shortcuts import render
from M2Crypto import RSA
import datetime
import random
from django.http import HttpResponse,HttpResponseRedirect
from Crypto.Cipher import AES
import time
import os

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def index(request):
    return render(request, "index.html")
def encryptupload(request):
    def get_key():
        s = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','s','y','z']
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        slice = random.sample(s, 6)
        dt = datetime.datetime.now()
        secret = str(dt.microsecond)+slice[0]+str(dt.year)+slice[1]+str(dt.minute)+slice[2]+str(dt.month)+slice[3]+str(dt.hour)+slice[4]+str(dt.second)+slice[5]+str(dt.day)
        b = 26-len(secret)
        slice = random.sample(s, b)
        for i in range(0, b):
            secret +=slice[i]
        print secret
        print len(secret)
        return secret
    def encrypt_file(f,key_value):
        key = get_key()
        name = f.name
        hz = name[-9:]
        rsa_pub = RSA.load_pub_key('./secret/rsa/keys/rsa_public_key.pem')
        ctxt = rsa_pub.public_encrypt(key+';'+hz, RSA.pkcs1_padding)
        ctxt64 = ctxt.encode('base64')
        print ctxt64
       
        cipher = AES.new(key+key_value)
        lines=''
        for line in f.readlines():
            lines+=line
        encrypted = cipher.encrypt(pad(lines)).encode('hex')
        #print encrypted
        return ctxt64+';'+encrypted
   
   
    #for chunk in f.chunks():
    #    destination.write(chunk)

    if request.method == 'POST':
        files = request.FILES.getlist('file')
        key = request.POST.get('key')

        print key
        i=0
        for file in files:
            i+=1
            string = encrypt_file(file,key)
            now = int(time.time())
            destination = open('./secret/static/upload/'+str(now)+str(i)+'.cfz', 'w')
            destination.write(string)
            destination.close()

        return HttpResponseRedirect('/list/')

def list(request):
    List=os.listdir(os.getcwd()+os.sep+'secret'+os.sep+'static'+os.sep+'upload'+os.sep)
    return render(request, 'list.html',{'List': List})

def decryptupload(request):
    def decrypt_file(s,key_value):
        List=[]
        ss=s.split(';')
        ctxt64=ss[0]
        encrypt_str=ss[1]
        rsa_pri = RSA.load_key('./secret/rsa/keys/rsa_private_key.pem')
        txt = rsa_pri.private_decrypt(ctxt64.decode('base64'), RSA.pkcs1_padding)
        #print '--------',list(txt.encode('base64'))
        s_txt = txt.decode('utf-32').encode('utf-8')
        #print list(s_txt)
       
        txts=s_txt.split(';')
        List.append(txts[1])
        print len(txts[0]+key_value)
        cipher = AES.new(txts[0]+key_value)
        decrypted = unpad(cipher.decrypt(encrypt_str.decode('hex')))
        List.append(decrypted)
        print decrypted
        return List
    if request.method == 'GET':
        name = request.GET.get('name')
        print name
        key='cfz123'
        string = ''
        destination = open('./secret/static/upload/'+name, 'r')
        lines=destination.readlines()
        for line in lines:
            string+=line
        destination.close()
        List=decrypt_file(string,key)
        destination = open('./secret/static/temp', 'w')
        destination.write(List[1])
        destination.close()
        return render(request, 'success.html',{'name':List[0]})
def delete(request):
    for i in range(0,35):
        destination = open('./secret/static/temp', 'w')
        destination.write(str(i))
        destination.close()

    os.remove(os.getcwd()+os.sep+'secret'+os.sep+'static'+os.sep+'temp')
    return HttpResponse('success')
def bigFileView(request):
    file_name = request.GET.get('name')
    string=''
    destination = open('./secret/static/temp', 'r')
    lines=destination.readlines()
    for line in lines:
        string+=line
    destination.close()

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = HttpResponse(string, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename='+file_name.encode('utf-8')#设定传输给客户端的文件名称


    #response = HttpResponse(readFile(file_name), content_type='APPLICATION/OCTET-STREAM')
    #response['Content-Disposition'] = 'attachment; filename='+file_name.encode('utf-8') + filetype_.encode('utf-8')#设定传输给客户端的文件名称
    #response['Content-Length'] = os.path.getsize(filepath_)#传输给客户端的文件大小
    return response