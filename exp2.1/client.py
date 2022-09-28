from xmlrpc.client import ServerProxy
import slave_client

proxy = ServerProxy('http://localhost:3000')
cart = {}
items = {}

if __name__ == '__main__':
 sc = slave_client.initiateSlaveClient(port=8080)
 prices = proxy.load_data()
 for i, key in enumerate(prices):
  items[i + 1] = key
 print("Select medicine")
 while(True):
  for i, (k, v) in enumerate(prices.items()):
   print(i + 1, k + ": ", v)
  print(i + 2, "Generate bill")
  print("Enter your choices:")
  choice = int(input())
  if choice == i + 2:
   break
  print("Enter the quantity")
  quantity = int(input())
  cart[items[choice]] = quantity
  print("Do you want home delivery(Additional charges: Rs 50):")
  isDelivery = bool(input())

 print("Your order is confirmed. Bill is being generated...")
 print("Your total amount is:", proxy.calculate_total(cart, isDelivery))