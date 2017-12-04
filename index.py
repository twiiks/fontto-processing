import argparse, logging, thread_worker, sys
from utils import set_logging


def parse_args():
    desc = "ttf/otf fonts to jpg images set (JUST KOREAN)"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--amqp-url', type=str, help='amqp url', required=True)
    parser.add_argument('--queue', type=str, help='queue name', required=True)
    parser.add_argument(
        '--log-path',
        type=str,
        default='output.log',
        help='log file path with filename',
        required=False)
    parser.add_argument(
        '--thread-num',
        type=int,
        default=3,
        help='number of thread',
        required=False)
    return parser.parse_args()


def main():
    # set args
    args = parse_args()
    amqp_url = args.amqp_url
    queue = args.queue
    log_path = args.log_path
    thread_num = args.thread_num

    # set log
    set_logging(log_path)

    # threading
    for i in range(0, thread_num):
        tw = thread_worker.ThreadWorker(amqp_url, queue,
                                        "Thread Number : " + str(i))
        tw.start()


if __name__ == '__main__':
    main()
