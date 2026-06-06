import re

def parse_expense(text):
    text = text.lower().strip()

    # ---------------- مبلغ هوشمند ----------------
    match = re.search(r'(\d[\d,]*)', text)

    amount = 0
    if match:
        amount = int(match.group(1).replace(",", ""))

    # ---------------- دسته‌بندی هوشمند ----------------
    categories = {
        "قهوه": ["قهوه", "کافه", "اسپرسو", "لاته"],
        "غذا": ["غذا", "ناهار", "شام", "پیتزا", "کباب"],
        "نوشیدنی": ["چای", "نوشابه", "آب", "دوغ"],
        "حمل‌ونقل": ["تاکسی", "اسنپ", "بنزین", "مترو"],
        "خرید": ["خرید", "سوپر", "فروشگاه"],
        "قبض": ["قبض", "برق", "آب", "اینترنت"],
    }

    category = "سایر"
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in text:
                category = cat
                break

    # ---------------- محل هوشمند ----------------
    location = ""

    location_keywords = ["از", "کافه", "رستوران", "فروشگاه", "مغازه", "در"]

    for kw in location_keywords:
        if kw in text:
            parts = text.split(kw)
            if len(parts) > 1:
                location = parts[-1].strip()

    return {
        "amount": amount,
        "category": category,
        "location": location,
        "note": text
    }