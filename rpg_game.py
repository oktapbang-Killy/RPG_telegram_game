import telebot
from telebot import types
import random
import json
TOKEN = '6542089143:AAHs1A07twSiAzSr1kSIM7GV1Zk8YH05mS4'
bot = telebot.TeleBot(TOKEN)
class Character:
    def __init__(self, name):
        self.name = name
        self.lives = 5
        self.coins = 30
    def display_info(self):
        return f"Имя: {self.name}\nЖизни: {self.lives}\nМонеты: {self.coins}"
    def encounter_enemy(self):
        enemy_chance = random.random()
        if enemy_chance < 0.8:
            if random.random() < 0.3:
                self.coins += 20
                self.lives += 1
                return f"Ты победил врага, собрав лут, ты обнаружил 20 монет!\n{self.display_info()}"
            else:
                self.lives -= 1
                return f"Враг оказался сильнее. Ты погиб.\n{self.display_info()}"
        else:
            return f"Врага не обнаружено. Тебе повезло!\n{self.display_info()}"
player_data_file = "player_info.json"
@bot.message_handler(commands=['start', 'newgame'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Добро пожаловать в игру!")
    bot.send_message(chat_id, "Приветствую тебя авантюрист!")
    player_name = message.from_user.first_name
    player = Character(player_name)
    bot.send_message(chat_id, f"Приветствую, {player.name}!")
    bot.send_message(chat_id, "Игра началась!")
    while player.lives > 0:
        bot.send_message(chat_id, player.encounter_enemy())
    bot.send_message(chat_id, "Game OVER. Твои жизни закончились.")
    player_info = {
        "name": player.name,
        "lives": player.lives,
        "coins": player.coins
    }
    with open(player_data_file, "w") as file:
        json.dump(player_info, file)
@bot.message_handler(commands=['status'])
def handle_status(message):
    chat_id = message.chat.id
    try:
        with open(player_data_file, "r") as file:
            player_info = json.load(file)
            status_message = f"Статус игрока:\nИмя: {player_info['name']}\nЖизни: {player_info['lives']}\nМонеты: {player_info['coins']}"
            bot.send_message(chat_id, status_message)
    except FileNotFoundError:
        bot.send_message(chat_id, "Используйте команду /newgame, чтобы начать.")
if __name__ == "__main__":
    bot.polling(none_stop=True)
