from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from threading import Timer
from time import time, sleep
import argparse
import sys

NETWORK = {
    "node_1": ("127.0.0.1", 5000),
    "node_2": ("127.0.0.1", 6000),
    "node_3": ("127.0.0.1", 7000),
}
CRS = ("127.0.0.1", 4000)


class RPCServer:
    def __init__(self, pid, pid_node_mapping, CRS, exetute_after=None):
        # this nodes pid
        self.pid = pid
        # set of all nodes pid in the network
        # so that we can judge whether to execute or not
        # this mapping is a dict and has "pid" as a key
        # and proxy RPC objects as values
        self.pid_node_mapping = pid_node_mapping
        # CRS (Critical Resource Server) rpc proxy
        self.CRS = CRS
        # this queue will save to whom we have to send request
        # after out execution in critical section is finished
        self.request_queue = []
        # reply set to store pids from whom this node has

        # got reply
        self.reply_set = set()
        # time in seconds after which this process
        # indent to execute critical section
        # if "None" then this process doesn't want
        # to execute
        self.execute_at = None
        self.task_done = True
        if exetute_after:
            self.execute_at = time() + exetute_after
            # schedule task to execute after given amount of time
            self.timer = Timer(exetute_after, self.execute)
            self.timer.start()
            self.task_done = False

    def request(self, timestamp: float, remote_node_pid: str):
        """
        RPC method to request access for shared resource
        accross the resource
        Params:
        timestamp: seconds passed since an epoch
        pid: process id which requested access
        """
        print(
            f"[{round(time() * 1000)}] REQUEST --> {remote_node_pid} ({round(timestamp*1000)})")

        # first check if this node wants to execute critical section
        # if yes then compair timestamps
        # if timestamp < self.execute_at then send reply
        if self.task_done or timestamp < self.execute_at:
            node = self.pid_node_mapping[remote_node_pid]
            # network latency
            sleep(1)
            node.reply(self.pid)
            return

        # else don't send reply just now
        # add remote_pid in queue and wait till this nodes
        # execution is finished,
        # for now add remote_pid in queue
        self.request_queue.append(remote_node_pid)

    def reply(self, rpid):
        # add rpid to self.reply_set
        self.reply_set.add(rpid)
        print(f"[{round(time() * 1000)}] REPLY --> {rpid}")
        # check if this process is wating for critical
        # section and if yes then check if all reply's
        # are received
        if self.execute_at:
            if set(self.pid_node_mapping.keys()) == self.reply_set:
                # if True then continue execute
                self.execute(after_replay=True)

    def execute(self, after_replay=False):
        # first send request to all nodes
        if not after_replay:
            for rpid, node in self.pid_node_mapping.items():
                if rpid == self.pid:
                    continue
                # request all nodes
                timestamp = time()
                node.request(timestamp, self.pid)

        # now wait for all reply's
        cart = {}

        if set(self.pid_node_mapping.keys()) == self.reply_set:
            # now we are allowed to execute in critical section

            prices = self.CRS.load_data()
            items = {}

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

            print("Your order is confirmed!")

        self.CRS.execute_task_in_critical(self.pid, cart)
        self.task_done = True
        print(f"[{round(time()*1000)}] Critical Section Resource Released\n\n")

        # after this process has completed execution
        # reply to everyone in queue
        for rpid in self.request_queue:
            self.pid_node_mapping[rpid].reply(self.pid)

        # clear reply_set after execution
        self.reply_set = set()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pid", type=str, help="Enter pid (node_1, node_2, node_3)")
    # --time_offset
    parser.add_argument("--time_offset", type=int, default=None,
                        help="time in seconds after which task starts to execute")

    args = parser.parse_args()

    PID = args.pid
    # print(PID)
    TIME_OFFSET = args.time_offset
    # create a RPC server running on a node
    server = SimpleXMLRPCServer(
        NETWORK[PID], allow_none=True, logRequests=False)

    # get all server proxy's
    pid_mapping = dict()

    for pid, addr in NETWORK.items():
        if pid == PID:
            continue
        pid_mapping[pid] = ServerProxy(f"http://{addr[0]}:{addr[1]}")

    crs_proxy = ServerProxy(f"http://{CRS[0]}:{CRS[1]}")
    server.register_instance(
        RPCServer(PID, pid_mapping, crs_proxy, TIME_OFFSET))

    try:
        print("Starting RPC Server...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
