import time

class FlowControllers():

    def wait_seconds(seconds):
        print("\n #################### Waiting... ####################")
        print("\nWaiting for {} seconds...".format(seconds))
        time.sleep(int(seconds))