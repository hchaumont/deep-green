from requests import get
from bs4 import BeautifulSoup
from time import sleep


FILE_NAME = 'fit_green.txt'
BOARD_URL = 'http://boards.4chan.org/fit/archive'
BASE_URL = 'http://boards.4chan.org/'
MIN_LINES = 4


def get_threads(board_url):
    r = get(board_url)
    soup = BeautifulSoup(r.content)
    threads = soup.find_all("a", "quotelink")
    return [BASE_URL + t['href'] for t in threads]


def traverse_thread(page_url):
    r = get(page_url)
    soup = BeautifulSoup(r.content)
    post_list = soup.find_all('div', 'postContainer')

    for post in post_list:
        greentext = post.find_all('span', 'quote')
        if len(greentext) >= MIN_LINES:
            with open(FILE_NAME, 'a') as file:
                for g in greentext:
                    if g.string: file.write(g.string + '\n')
                file.write('\n')
    print('Page traversed.')


if __name__ == '__main__':
    skip = int(input('Skip count: '))
    thread_urls = get_threads(BOARD_URL)
    thread_count = len(thread_urls)
    current_count = 1
    while thread_urls:
        if skip:
            current_count += 1
            skip -= 1
            thread_urls.pop()
            continue
        url = thread_urls.pop()
        traverse_thread(url)
        print(f'{current_count} of {thread_count}.')
        current_count += 1
        sleep(1)

    print("Success!")
