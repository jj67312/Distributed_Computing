from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
server = SimpleXMLRPCServer(('localhost',3000), allow_none=True)
prices = {'medicine1': 100, 'medicine2': 200, 'medicine3': 300, 'medicine4': 350, 'medicine5': 250}
def load_data():
 return prices

def calculate_total(cart, isDelivery):
 total = 0
 delivery = 50
 for k, v in cart.items():
  total += prices[k] * v

 if(isDelivery) :
  total += delivery

 return total

server.register_function(load_data)
server.register_function(calculate_total)

if __name__ == '__main__':
 try:
  print('Serving...')
  server.serve_forever()
 except KeyboardInterrupt:
  print('Exiting')