from datetime import datetime
import calendar

def to_shamsi(year, month, day):
    """تبدیل میلادی به شمسی"""
    # فرمول تقریبی
    year = year - 621 if month > 3 or (month == 3 and day > 20) else year - 622
    month = month + 9 if month <= 3 else month - 3
    day = day + 10 if month > 9 else day + 20 if month > 3 else day + 11
    
    # تنظیم ماه و روز
    if month > 12:
        month -= 12
        year += 1
    
    return f"{year}/{month:02d}/{day:02d}"

def get_today_shamsi():
    """تاریخ امروز شمسی"""
    now = datetime.now()
    return to_shamsi(now.year, now.month, now.day)

def get_today_miladi():
    """تاریخ امروز میلادی"""
    return datetime.now().strftime("%Y-%m-%d")
