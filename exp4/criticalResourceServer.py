import sys
from xmlrpc.server import SimpleXMLRPCServer
import argparse
from time import time


class CRS:
    quantities = {'medicine1': 100, 'medicine2': 200,
              'medicine3': 300, 'medicine4': 350, 'medicine5': 250}

    def load_data(self):
        return self.quantities

    def execute_task_in_critical(self, rpid, cart):
        print('quantities = ', self.quantities)
        print('Cart = ', cart)

        # quantities - cart:
        for k, v in cart.items():
            self.quantities.update({k: self.quantities.get(k) - v})

        print('Quantities after recent transaction = ', self.quantities)

        print(f"[{round(time() * 1000)}] --> Backup Done By {rpid}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", type=str, help="Enter IP Address of Server", default="127.0.0.1")
    parser.add_argument("port", type=int, help="Enter Port Number")

    args = parser.parse_args()

    HOST = args.ip
    PORT = args.port

    # create a RPC server running on a node
    server = SimpleXMLRPCServer(
        (HOST, PORT), allow_none=True, logRequests=False)
    server.register_instance(CRS())

    try:
        print("Starting RPC Server...")
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
