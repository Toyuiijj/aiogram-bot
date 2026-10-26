from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    Message, 
    KeyboardButton,
    CallbackQuery, 
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import aiosqlite

router = Router()

from aiogram import Bot
from aiogram.types import FSInputFile
import asyncio 

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="почати")],
            [KeyboardButton(text="допомога")],
            [KeyboardButton(text="про бота")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=" відкрити сторінку моїх робіт", url="https://www.instagram.com/yelyzarrr?vrfl=Mjc2aWY0amMwdXdq")],
            [InlineKeyboardButton(text="більше ", callback_data="more_info")]
]
    )
    return keyboard


@router.callback_query(lambda c: c.data == "more_info")
async def  process_more_info(callback: CallbackQuery):
    await callback.message.answer(" телеграм канал розробника:https://t.me/liveuser4"  )
    await callback.answer()


import aiohttp

async def get_product(product_id):
    url=f"https://fakestoreapi.com/products/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return None

            data = await response.json()
            return data
        

DB_Name =  'liza_sql'

async def init_db():
    async with aiosqlite.connect(DB_Name) as db:
        await db.execute("""
             CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY,
                          full_name TEXT,
                          age INTEGER 
                           )
                          """)
        await db.commit()


async def add_user(full_name,age):
    async with aiosqlite.connect(DB_Name) as db:
        await db.execute('INSERT INTO users (full_name,age) VALUES (?, ?)',(full_name,age))
        await db.commit()

   
async def get_users():
    async with aiosqlite.connect(DB_Name) as db:
       cursor=await db.execute('SELECT full_name, age  FROM users ')
       result= await cursor.fetchall()
       return result 
      
subscribes= set()

async def notifier(bot: Bot):
    while True:
        if subscribes:
            for user_id in list(subscribes):
                try:
                    await bot.send_message(user_id," сіла баба на горох і сказала діду оп")
                except Exception:
                    pass
               
                await asyncio.sleep(0.5)

               
        await asyncio.sleep(10)




@router.message(Command("start"))
@router.message(F.text.lower() =="почати")
async def start(message: Message):
    await init_db()
    await message.answer("привіт👋 я *Ліза*💄\n\n Я можу _допомогти_ тобі з пошуком інформації, відповідати на твої запитання та надавати корисні поради. Щоб дізнатися більше про мої можливості, скористайся командою /help.\nStore function:/product ID\n\nПриклад: /product 1\nregistration function: Пропишіть команду: /reg Age\nmessage distribution function:Команди:\n\n /subscribe - підписатися на повідомлення\n\n /unsubscribe -  відпискa\n\n/subscribers - список підписників", parse_mode="Markdown")

@router.message(Command("subscribe"))
async def subscribe(message:Message):
    user_id = message.from_user.id

    subscribes.add(user_id)

    await message.answer("ти підписався 🦁 ")

@router.message(Command("unsubscribe"))
async def unsubscribe(message:Message):
    user_id = message.from_user.id
    subscribes.discard(user_id)
    await message.answer("ти  впідписався 😭 ")

@router.message(Command("subscribers"))
async def subscribers_cmd(message:Message):
   if not subscribes:
      await message.answer('пока нікого немає')
      return

   text="Підписники:\n"
   for uid in subscribes:
       text += f"{uid}\n"
   await message.answer(text)
     
    






@router.message(Command("reg"))
async def reg(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1]:
     await message.answer("Ведіть команду правильно")
     return
    await add_user(message.from_user.full_name, int(parts[1]))

    await message.answer(" Все готово !")


@router.message(Command("users"))
async def users(message: Message):
    users= await get_users ()
    if not users:
        await message.answer(" В базі немає користувача")
        return

    text=" Користувач в базі:\n\n"
    for full_name, age in users:
        text += f'{full_name}- <code>{age}</code>\n'
        await message.answer(text, parse_mode="HTML")



@router.message(Command("product"))
async def get_product_cmd(message: Message):
    parts=message.text.strip().split()

    if len(parts) != 2:
        await message.answer(" використовуйте:/product 1")
        return

    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer("ID продукту має бути числом.")
        return

    await message.answer(f"шукаю товар... id: {product_id}")

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer("Виникла помилка при отриманні даних про продукт.")
        return

    if product is None:
        await message.answer("Товар не знайдено.")
        return

    title = product.get("title", "Немає назви")
    price = product.get("price", "0.00")
    description = product.get("description", "Немає опису")
    category = product.get("category", "Немає категорії")
    image = product.get("image")

    text=(
        f"<b>{title}</b>\n\n"
        f"Ціна: <b>{price}</b>\n"
        f"Категорія: <i>{category}</i>\n"
        f"Опис: <i>{description}</i>\n"
    )

    photo = FSInputFile("photo_2026-10-24_17-42-42.jpg")
    await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")




    #if image:
        #await message.answer_photo(photo=image, caption=text,parse_mode="HTML")
    #else:
      #await message.answer(text, parse_mode="HTML")





@router.message(Command("help"))
@router.message(F.text.lower() =="допомога")
async def help_cmd(message: Message):
    await message.answer("Команди:\n<b>/start</b> - почати спілкування\n<i>/help</i> - отримати список команд\n<b>/about</b> - дізнатися про бота\n<b>/file</b> - секретна функція😱\n<b>/users</b> - збережені корситувачі", parse_mode="HTML",reply_markup=get_main_keyboard())
@router.message(Command("about"))
@router.message(F.text.lower() =="про бота")
async def about_cmd(message: Message):
    await message.answer(
    f"Це команда про бота, бот створений на основі реальної людини, тому прошу не ображати мене, це дуже поранить моє серце 🫀 і прошу дотримуватися певної субординації. Твоє ім'я: {message.from_user.first_name} 👠",
    reply_markup=get_main_inline_keyboard()
)
        

@router.message(F.video)
async def process_video(message: Message):
    video = message.video
    file_id = video.file_id

    await message.answer(f"Ви надіслали відео!\nID video: <code>{file_id}</code>\nДлительность: <code>{video.duration}</code>", parse_mode="HTML")
    await message.answer_video(file_id, caption="Твоє відео бандіт 😈 ") 


@router.message(F.document)
async def process_document(message: Message, bot: Bot):
    document = message.document
    file_id= document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f"downloads/{document.file_name}"
    await bot.download_file(file_path=file_path, destination=local_path)
    await message.answer("Документ завантажено!")


@router.message(Command("file")) 
async def send_file(message: Message):
    file = FSInputFile("files/example.txt")
    await message.answer_document(file)


@router.message()
async def mess(message: Message):
    await message.answer("Як справи?")


