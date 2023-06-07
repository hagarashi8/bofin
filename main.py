import logging
import time
from aiogram import Bot, Dispatcher, executor, types
import os
import aiogram.dispatcher.filters 
TOKEN=os.environ["BOT_TOKEN"] or ""
def Botyara():

    bot = Bot(TOKEN)  # Объект бота
    dp = Dispatcher(bot)  # не диспетчер, а диспатчер - штука, котораязанимается эвентами

    @dp.message_handler(commands=['start', 'help'])
    async def process_start_command(message: types.Message):
        await message.reply("""
Бофин - растущий бот для (пока ещё не совсем) всех ваших финансовых нужд!
/weeks <Стартовый капитал> <Инкремент> - рассчитайте, сколько вы сможете получить, сыграв в 52 недели богатства
/credit <Сумма займа> <Годовой процент> <Срок займа в месяцах> рассчитает показатели кредита)
/deposit <Сумма> <Годовая ставка> <Количество месяцев> Рассчитает доход по займу с простыми процентами
/compound_deposit <Сумма> <Годовая ставка> <Количество месяцев> Рассчитает доход по займу со сложными процентами
""")

    @dp.message_handler(commands=['weeks'])
    async def calculate_weeks(message):
        cur_command = message.text.split()
        try:
            starting_pay = int(cur_command[1])
            increment = int(cur_command[2])
        except:
            return await message.reply("Неверные аргументы! Использование: /weeks <Стартовый капитал> <Инкремент>")
        last_week_pay = starting_pay + (51) * increment
        total = (starting_pay + last_week_pay)/2 * 52
        await message.reply(f"""
        Плата за последнюю неделю: {last_week_pay}
Итоговая сумма: {total}
              """)
    @dp.message_handler(commands=["credit"])
    async def calculate_credit(message):
        cur_command = message.text.split()
        try:
            total = int(cur_command[1])
            percent = float(cur_command[2])
            payments_count=int(cur_command[3])
        except:
            return await message.reply("Неверные аргументы! Использование: /credit <Сумма займа> <Годовой процент> <Срок займа в месяцах>")
        monthly_percent = percent/12/100
        monthly_multiplier = 1 + monthly_percent
        coefficent = (monthly_percent * monthly_multiplier**payments_count) / (monthly_multiplier**payments_count - 1)
        monthly_payment = coefficent * total
        await message.reply(f"""Ежемесячный платёж: {monthly_payment}
Итого переплата: {monthly_payment*payments_count - total}
""")
    @dp.message_handler(commands=["deposit"])
    async def deposit(message):
        cur_command = message.text.split()
        try:
            total = int(cur_command[1])
            percent = float(cur_command[2])
            pays_count=int(cur_command[3])
        except:
            return await message.reply("Неверные аргументы! Использование: /deposit <Сумма> <Годовая ставка> <Количество дней вклада>")
        profit = (total*percent*pays_count/12/100)
        await message.reply(f"Доход составит: {profit}")
    @dp.message_handler(commands=["compound_deposit"])
    async def deposit(message):
        cur_command = message.text.split()
        try:
            total = int(cur_command[1])
            percent = float(cur_command[2])
            pays_count=int(cur_command[3])
        except:
            return await message.reply("Неверные аргументы! Использование: /compound_deposit <Сумма> <Годовая ставка> <Срок вклада в месяцах>")
        profit = (total*(percent/100/12 +1)**pays_count) - total
        await message.reply(f"Доход составит: {profit}")
    executor.start_polling(dp, skip_updates=False)
Botyara()
