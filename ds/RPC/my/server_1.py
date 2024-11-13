from xmlrpc.server import SimpleXMLRPCServer

def addition(a,b):
	return a+b

port=7000
server=SimpleXMLRPCServer(('localhost',7000))

server.register_function(addition,'addition_rpc')

try:
	print('listening')
	server.serve_forever()

except:
	print('exit')