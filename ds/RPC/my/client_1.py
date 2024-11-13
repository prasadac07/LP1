import xmlrpc.client

proxy=xmlrpc.client.ServerProxy("http://localhost:7000/")

print('addition',proxy.addition_rpc(2,3))