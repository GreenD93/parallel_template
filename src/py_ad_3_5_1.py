"""
Section 3
Concurrency, CPU Bound vs I/O Bound - I/O Bound(2) - threading vs asyncio vs multiprocessing


Keyword - I/O Bound, requests, threading

"""
# I/O-Bound Threading 예제(https://realpython.com/python-concurrency/#synchronous-version)

import concurrent.futures
import threading
# pip install requests
import requests
import time

# 같은 naming 독립적인 영역
# 각 스레드에 생성되는 객체(독립적)
thread_local = threading.local()

# 세션 제공
def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

# 실행함수1(다운로드)
def request_site(url):
    # 세션 획득
    session = get_session()

    # 세션 확인
    print(session)
    # print(session.headers)

    with session.get(url) as response:
        print(f"[Read Contents : {len(response.content)}, Status Code : {response.status_code}] from {url}")

    return {'url': url,
            'content': response.content}


# 실행함수2
def request_all_site(urls):
    # 멀티스레드 실행
    # 반드시 max_worker 개수 조절 후 session 객체 확인
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        pool_output = executor.map(request_site, urls)

    for pool in pool_output:
        print(pool['url'])

def main():
    # 테스트 URLS
    urls = [
            "https://www.jython.org",
            "http://olympus.realpython.org/dice",
            "https://realpython.com/",
            "https://www.inflearn.com/",
            "https://fastcampus.co.kr/",
            "https://www.naver.com/",
            "https://www.daum.net/",
            "https://www.musinsa.com/",
            "https://www.daangn.com/",
            "https://namu.wiki/",
            "https://finance.naver.com/",
            "https://finance.naver.com/sise/",
            "https://finance.naver.com/world/",
            "https://finance.naver.com/marketindex/"
    ]

    # 실행시간 측정
    start_time = time.time()

    # 실행
    request_all_site(urls)

    # 실행 시간 종료
    duration = time.time() - start_time

    print()

    # 결과 출력
    print(f"Downloaded {len(urls)} sites in {duration} seconds")

if __name__ == "__main__":
    main()
