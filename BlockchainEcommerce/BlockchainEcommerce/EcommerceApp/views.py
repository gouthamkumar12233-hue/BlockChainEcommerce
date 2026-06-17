from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
import ipfsApi
import os
from django.core.files.storage import FileSystemStorage
import pickle

global details, username
details=''
global contract

api = ipfsApi.Client(host='http://127.0.0.1', port=5001)

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract code
    deployed_contract_address = '0xB52110D630E83f7E8373eAca575981292b9745bC' #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'addproduct':
        details = contract.functions.getProduct().call()
    if contract_type == 'bookorder':
        details = contract.functions.getOrder().call()    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract file
    deployed_contract_address = '0xB52110D630E83f7E8373eAca575981292b9745bC' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'addproduct':
        details+=currentData
        msg = contract.functions.addProduct(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'bookorder':
        details+=currentData
        msg = contract.functions.bookOrder(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def updateQuantityBlock(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #student contract file
    deployed_contract_address = '0xB52110D630E83f7E8373eAca575981292b9745bC' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.addProduct(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def BrowseProducts(request):
    if request.method == 'GET':
        output = '<tr><td><font size="" color="black">Product&nbsp;Name</font></td><td><select name="t1">'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'addproduct':
                output+='<option value="'+arr[2]+'">'+arr[2]+'</option>'
        output+="</select></td></tr>"
        context= {'data1':output}
        return render(request, 'BrowseProducts.html', context)

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})
    
def ViewOrders(request):
    if request.method == 'GET':
        global details
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Customer Name</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Ordered Date</font></th></tr>'
        readDetails("bookorder")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'bookorder':
                print(arr[2]+" "+user)
                details = arr[3].split(",")
                pid = arr[1]
                user = arr[2]
                book_date = arr[4]
                output+='<tr><td><font size=3 color=black>'+pid+'</font></td>'
                output+='<td><font size=3 color=black>'+user+'</font></td>'
                output+='<td><font size=3 color=black>'+details[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+details[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+details[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(book_date)+'</font></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewOrders.html', context)     

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def AddProduct(request):
    if request.method == 'GET':
       return render(request, 'AddProduct.html', {})

def BookOrder(request):
    if request.method == 'GET':
        global details
        pid = request.GET['crop']
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == user:
                    details = arr[3]+","+arr[4]+","+arr[5]
                    break
        today = date.today()            
        data = "bookorder#"+pid+"#"+user+"#"+details+"#"+str(today)+"\n"
        saveDataBlockChain(data,"bookorder")
        output = 'Your Order details Updated<br/>'
        context= {'data':output}
        return render(request, 'ConsumerScreen.html', context)      

def UpdateQuantity(request):
    if request.method == 'GET':
        output = ''
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()        
        output = '<tr><td><font size="" color="black">Product&nbsp;Name</font></td><td><select name="t1">'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == user:
                    output+='<option value="'+arr[2]+'">'+arr[2]+'</option>'
        output+="</select></td></tr>"
        context= {'data':output}
        return render(request, 'UpdateQuantity.html', context)       
        

def SearchProductAction(request):
    if request.method == 'POST':
        ptype = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Supplier Name</font></th>'
        output+='<th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Purchase Product</font></th></tr>'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            print("my=== "+str(arr[0])+" "+arr[1]+" "+arr[2]+" "+ptype)
            if arr[0] == 'addproduct':
                if arr[2] == ptype:
                    output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                    output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                    output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                    output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                    output+='<td><font size=3 color=black>'+arr[5]+'</font></td>'
                    content = api.get_pyobj(arr[6])
                    content = pickle.loads(content)
                    if os.path.exists(r"C:\Users\rajsh\OneDrive\Desktop\BlockchainEcommerce\BlockchainEcommerce\EcommerceApp\static\product.png"):
                        os.remove(r"C:\Users\rajsh\OneDrive\Desktop\BlockchainEcommerce\BlockchainEcommerce\EcommerceApp\static\product.png")
                    with open(r"C:\Users\rajsh\OneDrive\Desktop\BlockchainEcommerce\BlockchainEcommerce\EcommerceApp\static\product.png", "wb") as file:
                        file.write(content)
                    file.close()
                    output+='<td><img src="/static/product.png" width="200" height="200"></img></td>'
                    output+='<td><a href=\'BookOrder?farmer='+arr[1]+'&crop='+arr[2]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'SearchProducts.html', context)              
        
    
def QuantityUpdateAction(request):
    if request.method == 'POST':
        pname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        index = 0
        record = ''
        readDetails("addproduct")
        rows = details.split("\n")
        tot_qty = 0
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == user and arr[2] == pname:
                    tot_qty = int(arr[4])
                    tot_qty = tot_qty + int(qty)
                    index = i
                    record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+str(tot_qty)+"#"+arr[5]+"#"+arr[6]+"\n"
                    break
        for i in range(len(rows)-1):
            if i != index:
                record += rows[i]+"\n"
        updateQuantityBlock(record)
        context= {'data':"Quantity details updated & new available quantity: "+str(tot_qty)}
        return render(request, 'SupplierScreen.html', context)
          
                    
      

def AddProductAction(request):
    if request.method == 'POST':
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        image = request.FILES['t5'].read()
        imagename = request.FILES['t5'].name
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        myfile = pickle.dumps(image)
        hashcode = api.add_pyobj(myfile)
        data = "addproduct#"+user+"#"+cname+"#"+price+"#"+qty+"#"+desc+"#"+hashcode+"\n"
        saveDataBlockChain(data,"addproduct")
        context= {'data':"Product details saved and IPFS image storage hashcode = "+hashcode}
        return render(request, 'AddProduct.html', context)
        
   
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        usertype = request.POST.get('type', False)
        record = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username:
                    record = "exists"
                    break
        if record == 'none':
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+usertype+"\n"
            saveDataBlockChain(data,"signup")
            context= {'data':'Signup process completd and record saved in Blockchain'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Register.html', context)    



def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        usertype = request.POST.get('type', False)
        status = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username and arr[2] == password and arr[6] == usertype:
                    status = 'success'
                    break
        if status == 'success' and usertype == 'Supplier':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':"Welcome "+username}
            return render(request, 'SupplierScreen.html', context)
        elif status == 'success' and usertype == 'Consumer':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':"Welcome "+username}
            return render(request, 'ConsumerScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)            


        
        



        
            
