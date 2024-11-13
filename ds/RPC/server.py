from xmlrpc.server import SimpleXMLRPCServer

# Define the functions

# Addition of two numbers
def addition(n1, n2):
    return n1 + n2

# Square of a number
def square(n):
    return n * n

# Factorial of a number 
def factorial(n):
    fact = 1
    for i in range(1, n+1):
        fact = fact * i
    return fact

# Set host and port
host = '127.0.0.1'  # Server's IP address
port = 12345        # Server's port

# Create an instance of SimpleXMLRPCServer that listens on host and port
server = SimpleXMLRPCServer(('localhost', port))

# Register functions with the server
server.register_function(factorial, 'factorial_rpc')
server.register_function(square, 'square_rpc')
server.register_function(addition, 'addition_rpc')

# Start the server
try:
    print(f"Starting and listening on {host}:{port}")
    server.serve_forever()
except :
    print("Exit")
