from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
import random
import os

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

# تنظیمات مرورگر با پروفایل برای جلوگیری از کپچا
options = webdriver.ChromeOptions()
profile_path = os.path.abspath("chrome-profile")
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# اجرای مرورگر
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# رفتن به دیوار
driver.get("https://divar.ir/")
time.sleep(5)

print("⏳ لطفاً در صورت نیاز لاگین کنید یا شهر را انتخاب کنید (۳۰ ثانیه)...")
time.sleep(30)

# انتخاب شهر (در صورت نیاز)
try:
    tehran_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "تهران")]')))
    tehran_btn.click()
    time.sleep(2)
except:
    pass

# جستجوی عبارت
search_term = "پژو ۲۰۶"
search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="جستجو در همهٔ آگهی‌ها"]')))
search_box.clear()
human_typing(search_box, search_term)
time.sleep(random.uniform(0.5, 1))
search_box.send_keys(Keys.ENTER)

# صبر و اسکرول برای بارگذاری کامل
wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/v/")]')))
time.sleep(5)
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))

# جمع‌آوری لینک‌ها
posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/v/")]')
links = [post.get_attribute('href') for post in posts if post.get_attribute('href')]
print(f"\n🔗 تعداد آگهی‌ها: {len(links)}")

# آماده‌سازی فایل CSV
file_exists = os.path.exists("divar_phones.csv")
with open("divar_phones.csv", "a", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:
        writer.writerow(["شماره تماس", "عنوان", "قیمت", "سال ساخت", "رنگ"])

    for index, link in enumerate(links):
        print(f"\n🟦 ({index+1}) آگهی: {link}")
        try:
            driver.get(link)
            time.sleep(random.uniform(2, 4))

            title = driver.find_element(By.CSS_SELECTOR, "h1.kt-page-title__title").text.strip()
            print("📌 عنوان:", title)

            try:
                price = driver.find_element(By.CSS_SELECTOR, "p.kt-unexpandable-row__value").text.strip()
            except:
                price = "—"

            try:
                year = driver.find_element(By.XPATH, '//span[contains(text(), "سال ساخت")]/following-sibling::span').text.strip()
            except:
                year = "—"

            try:
                color = driver.find_element(By.XPATH, '//span[contains(text(), "رنگ")]/following-sibling::span').text.strip()
            except:
                color = "—"

            try:
                contact_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".kt-button.kt-button--primary.post-actions__get-contact")))
                time.sleep(random.uniform(1, 2))  # ✅ تأخیر قبل از کلیک روی دکمه
                contact_btn.click()
                time.sleep(random.uniform(2, 3))  # ✅ تأخیر بعد از کلیک
                phone_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.kt-unexpandable-row__action")))
                phone_number = phone_element.text.strip()
            except:
                phone_number = "خطا در دریافت شماره"

            print("✅ شماره تماس:", phone_number)
            writer.writerow([phone_number, title, price, year, color])

        except Exception as e:
            print("❌ خطا:", e)
            writer.writerow(["خطا", "—", "—", "—", "—"])

        csvfile.flush()
        time.sleep(random.uniform(3, 6))

print("\n📁 شماره‌ها با موفقیت در فایل divar_phones.csv ذخیره شدند!")
driver.quit()
