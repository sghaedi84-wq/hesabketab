from openai import OpenAI

# ⚠️ کلید API خودت رو اینجا بذار
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")


def enhance_text(text: str) -> str:
    """
    اصلاح متن فارسی + تصحیح غلط تایپی + استانداردسازی جمله هزینه
    """

    prompt = f"""
تو یک دستیار هوشمند حسابداری هستی.

این متن کاربر ممکن است غلط تایپی، ناقص یا محاوره‌ای باشد.

وظیفه تو:
1. اصلاح غلط‌های املایی
2. استاندارد کردن جمله
3. نگه داشتن مبلغ، محل، نوع خرید
4. خروجی فقط یک جمله تمیز و قابل پردازش باشد

متن:
{text}

خروجی فقط متن اصلاح شده باشد، بدون توضیح اضافی.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception:
        # اگر AI قطع بود، متن اصلی برگرده
        return text