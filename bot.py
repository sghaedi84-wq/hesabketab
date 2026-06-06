import os
import asyncio
import uuid
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from openai import OpenAI

from ai_enhancer import enhance_text
from database import init_db, add_expense, get_user_expenses
from ai_parser import parse_expense
from persian_date import get_today_shamsi
from excel_handler import export_to_excel
from voice_handler import voice_to_text


# ---------------- ENV ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables")


# ---------------- CLIENTS ----------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)


# ---------------- START ----------------
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "سلام 👋\n\n"
        "ربات حسابداری هوشمند (AI + Voice)\n\n"
        "مثال:\n"
        "25000 قهوه از کافه ونک\n\n"
        "🎙 میتونی ویس هم بفرستی"
    )


# ---------------- TEXT ----------------
@dp.message(F.text)
async def expense_handler(message: Message):

    corrected_text = enhance_text(message.text)
    data = parse_expense(corrected_text)

    transaction_id = str(uuid.uuid4())[:8]

    add_expense(
        user_id=message.from_user.id,
        amount=data["amount"],
        category=data["category"],
        location=data["location"],
        date_shamsi=get_today_shamsi(),
        date_miladi=datetime.now().strftime("%Y-%m-%d"),
        note=f"{data['note']} | ID:{transaction_id}"
    )

    await message.answer(
        f"✅ ثبت شد\n\n"
        f"📝 متن: {corrected_text}\n"
        f"💰 مبلغ: {data['amount']:,}\n"
        f"📂 دسته: {data['category']}\n"
        f"📍 محل: {data['location'] or '-'}\n"
        f"🆔 کد: {transaction_id}"
    )


# ---------------- VOICE ----------------
@dp.message(F.voice)
async def voice_handler(message: Message):

    file = await bot.get_file(message.voice.file_id)

    file_path = f"voice_{message.from_user.id}_{uuid.uuid4().hex[:6]}.ogg"

    await bot.download_file(file.file_path, file_path)

    text = voice_to_text(file_path)
    corrected_text = enhance_text(text)
    data = parse_expense(corrected_text)

    transaction_id = str(uuid.uuid4())[:8]
    now = datetime.now().strftime("%H:%M:%S")

    add_expense(
        user_id=message.from_user.id,
        amount=data["amount"],
        category=data["category"],
        location=data["location"],
        date_shamsi=get_today_shamsi(),
        date_miladi=datetime.now().strftime("%Y-%m-%d"),
        note=f"{data['note']} | ID:{transaction_id}"
    )

    await message.answer(
        f"🎙 پردازش ویس\n\n"
        f"📝 متن: {corrected_text}\n"
        f"💰 مبلغ: {data['amount']:,}\n"
        f"📂 دسته: {data['category']}\n"
        f"📍 محل: {data['location'] or '-'}\n"
        f"🆔 کد: {transaction_id}\n"
        f"🕒 ساعت: {now}"
    )


# ---------------- DASHBOARD ----------------
@dp.message(Command("dashboard"))
async def dashboard(message: Message):
    data = get_user_expenses(message.from_user.id)

    total = sum(x[2] for x in data) if data else 0
    count = len(data)

    await message.answer(
        f"📊 داشبورد\n\n"
        f"💰 مجموع: {total:,}\n"
        f"📌 تعداد: {count}"
    )


# ---------------- REPORT ----------------
@dp.message(Command("report"))
async def report(message: Message):
    data = get_user_expenses(message.from_user.id)

    today = datetime.now().strftime("%Y-%m-%d")
    today_data = [x for x in data if x[6] == today]

    total = sum(x[2] for x in today_data)
    count = len(today_data)

    await message.answer(
        f"📊 گزارش امروز\n\n"
        f"💰 مجموع: {total:,}\n"
        f"📌 تعداد: {count}"
    )


# ---------------- EXCEL ----------------
@dp.message(Command("excel"))
async def excel_handler(message: Message):
    filename = export_to_excel(message.from_user.id)

    await message.answer_document(
        FSInputFile(filename),
        caption="📊 خروجی اکسل"
    )


# ---------------- MAIN ----------------
async def main():
    init_db()
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())