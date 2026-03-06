import telebot
from telebot import types
import json
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

WORKERS = ["Murolim", "Imron", "Abduvali", "Nurmuhammad", "Bilol", "MuhammadalI"]

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

def add_record(name, status):
    if name not in data:
        data[name] = {"worked":0,"missed":0,"late":0,"leave":0}

    if status == "worked":
        data[name]["worked"] += 1
    elif status == "missed":
        data[name]["missed"] += 1
    elif status == "late":
        data[name]["late"] += 1
    elif status == "leave":
        data[name]["leave"] += 1

    save_data(data)

def calculate_salary(name):
    base = 1200
    day_price = 46
    missed_penalty = 56
    late_penalty = 10

    d = data.get(name, {})
    missed = d.get("missed",0)
    late = d.get("late",0)

    salary = base - (missed*missed_penalty) - (max(0,late-3)*late_penalty)

    return salary

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg,"Davomat botga xush kelibsiz")

@bot.message_handler(commands=["chiqdi"])
def chiqdi(msg):
    try:
        name = msg.text.split()[1]
        add_record(name,"worked")
        bot.reply_to(msg,f"{name} bugun ishladi")
    except:
        bot.reply_to(msg,"/chiqdi Ism yozing")

@bot.message_handler(commands=["chiqmadi"])
def chiqmadi(msg):
    try:
        name = msg.text.split()[1]
        add_record(name,"missed")
        bot.reply_to(msg,f"{name} chiqmagan deb belgilandi")
    except:
        bot.reply_to(msg,"/chiqmadi Ism yozing")

@bot.message_handler(commands=["kechikdi"])
def kechikdi(msg):
    try:
        name = msg.text.split()[1]
        add_record(name,"late")
        bot.reply_to(msg,f"{name} kechikdi")
    except:
        bot.reply_to(msg,"/kechikdi Ism yozing")

@bot.message_handler(commands=["ruxsat"])
def ruxsat(msg):
    try:
        name = msg.text.split()[1]
        add_record(name,"leave")
        bot.reply_to(msg,f"{name} ruxsat oldi")
    except:
        bot.reply_to(msg,"/ruxsat Ism yozing")

@bot.message_handler(commands=["oylik"])
def oylik(msg):
    try:
        name = msg.text.split()[1]
        salary = calculate_salary(name)
        bot.reply_to(msg,f"{name} oyligi: {salary}$")
    except:
        bot.reply_to(msg,"/oylik Ism yozing")

bot.infinity_polling()
