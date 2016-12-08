import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sys

queue = Queue()


def run():
    arguments = sys.argv
    project_name = arguments[1]
    homepage = arguments[2]
    number_of_threads = int(arguments[3])

    domain_name = get_domain_name(homepage)
    queue_file = project_name + '/queue.txt'
    # crawled_file = project_name + '/crawled.txt'

    Spider(project_name, homepage, domain_name)
    create_workers(number_of_threads)
    crawl(queue_file)


# Create worker threads (will die when main exits)
def create_workers(number_of_threads):
    for _ in range(number_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs(queue_file):
    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()
    crawl(queue_file)


# Check if there are items in the queue, if so crawl them
def crawl(queue_file):
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(queue_file)


run()
