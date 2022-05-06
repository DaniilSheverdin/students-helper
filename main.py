import logging, requests, wolframalpha, sqlite3, re
from bs4 import BeautifulSoup
from lxml import html
from credits import API_TOKEN, WOLFRAM_TOKEN
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.utils import executor
import keyboard as kb



# Configure logging
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=storage)

wr_client = wolframalpha.Client(WOLFRAM_TOKEN)

url_group="https://schedule.tsu.tula.ru/?group="
url_exam="https://schedule.tsu.tula.ru/exam/?group="

coord={"Главный":[54.166896, 37.586329], "1":[54.172720, 37.596040],
       "2":[54.172583, 37.594019], "3":[54.171561, 37.589347], "4":[54.172415, 37.589222], "5":[54.173321, 37.592114],
       "6":[54.168409, 37.589320],"7":[54.172167, 37.597513], "8":[54.168045, 37.588925], "9":[54.166896, 37.586329],
       "10":[54.167866, 37.585143],"11":[54.167708, 37.586976],"12":[54.174185, 37.593686]}


# создаём форму и указываем поля
class Form(StatesGroup):
    group = State()
    group_ex = State()
    corpus=State()
    task=State()
    link=State()
    del_link=State()
    
#получение расписания пар
def getSchedule(group):
    url=url_group+group
    lst=[]
    s=requests.get(url)
    soup = BeautifulSoup(s.text, 'lxml')
    if len(soup.find_all('table', class_='tt'))==0:
        return "Такой группы не существует, или расписание еще не готово."
    table= soup.find_all('table', class_='tt')[1]
    rows=table.find_all('tr')
    days=[]
    classes=[]
    class__=[]
    for r in rows:      
        time= r.find('td',class_='time').text
        if "Вторник" in time or "Среда" in time or "Четверг" in time or "Пятница" in time or "Суббота" in time or "Понедельник" in time:  
            days.append(r.text)
            if len(class__)!=0:
                classes.append(class__)
                class__=[]
        else:
            class__.append(r.text.replace('\n\n',' '))
    schedule_list= list(zip(days, classes))
    schedule = {v: k for v,k in schedule_list}
    return schedule
#получение расписания экзаменов
def getExamSchedule(group):
    url=url_exam+group
    lst=[]
    s=requests.get(url)
    soup = BeautifulSoup(s.text, 'lxml')
    data=soup.find_all('table',{"class":'tt'})
    if len(data)==0:
        return "Такой группы не существует, или расписание еще не готово."
    else:
        for d in data:
            lst.append(d.text.replace('\n',' '))
        return lst

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ Бот Помощник для студентов ТулГу!", reply_markup=kb.greet_kb1)
    
@dp.message_handler(commands=['menu'])
async def send_welcome(message: types.Message):
    await message.reply("Окей, вот, что я могу:", reply_markup=kb.inline_kb1)
    
# Начинаем диалог по группе
@dp.message_handler(commands=['group'])
async def cmd_start(message: types.Message):
    await Form.group.set()
    await bot.send_message(callback_query.from_user.id, "Напиши номер группы")
    
# Добавляем возможность отмены, если пользователь передумал получить расписание
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')

# Сюда приходит ответ с группой
@dp.message_handler(state=Form.group)
async def process_group(message: types.Message, state: FSMContext):
    schdl=getSchedule(message.text)
    if type(schdl)==type("string"):
        await message.answer(schdl)
    else:
        for s in schdl:
            answer=s+'\n========================\n'
            for c in schdl[s]:
                answer+=c+"\n"
            await message.answer(answer)
    await state.finish()
    
# Начинаем диалог по экзаменам
@dp.message_handler(commands=['exam'])
async def cmd_exam_start(message: types.Message):
    await Form.group_ex.set()
    await message.reply("Напиши номер группы")
    

# Сюда приходит ответ с группой
@dp.message_handler(state=Form.group_ex)
async def process_exam(message: types.Message, state: FSMContext):
    schdl=getExamSchedule(message.text)
    if type(schdl)==type("string"):
        await message.answer(schdl)
    else:  
        for s in schdl:
            await message.answer(s)
    await state.finish()
    
# Начинаем диалог по адресу
@dp.message_handler(commands=['adress'])
async def cmd_adres(message: types.Message):
    await Form.corpus.set()
    m="Введите номер корпуса из спика ниже\n"
    for name in coord:
        m+=name+"\n"
    await message.answer(m)
    
# Сюда приходит ответ с названием корпуса
@dp.message_handler(state=Form.corpus)
async def process_exam(message: types.Message, state: FSMContext):
    name=message.text
    chat_id = message.chat.id
    if name in coord.keys():
        await bot.send_location(chat_id,coord[name][0],coord[name][1])
    await state.finish()
    
    
    
# Начинаем диалог по примеру
@dp.message_handler(commands=['solve'])
async def cmd_wolfram(message: types.Message):
    await Form.task.set()
    await message.reply("Ввод примера: ")

#возвращает результат решения
def math(eq):
  res = wr_client.query(eq.strip(), params=(("format", "image,plaintext"),))
  data = {}
  for p in res.pods:
      for s in p.subpods:
          if s.img.alt.lower() == "root plot":
              data['rootPlot'] = s.img.src
          elif s.img.alt.lower() == "number line":
              data['numberLine'] = s.img.src
  data['results'] = [i.texts for i in list(res.results)][0]
  
  return data

# Сюда приходит ответ с примером для решения
@dp.message_handler(state=Form.task)
async def process_wolfram(message: types.Message, state: FSMContext):
    data=math(message.text)
    chat_id = message.chat.id
    if len(data)!=0:
        m=""
        if 'rootPlot' in data:
            m+="График: "+data['rootPlot']+"\n"
        if 'numberLine' in data:
            m+="Числовая прямая: "+data['numberLine']+"\n"
        if 'results' in data:
            m+="Корни: "+str(data['results'])
        else:
            m+="Уравнение не имеет решений"
        await message.answer(m)
    else:
        await message.answer("Уупс! Что-то пошло не так!")
    await state.finish()

#добавление записи в БД
async def link_writer(link, user_id):
    con = sqlite3.connect("tgbot2usefullinks.db")
    cur = con.cursor()

    cur.execute("""INSERT INTO links (link, userid) VALUES('{link}', {user_id});""".format(link=link, user_id=user_id))
    con.commit()
    cur.close()
    
#удаление записи из БД
async def link_remove(link, user_id):
    con = sqlite3.connect("tgbot2usefullinks.db")
    cur = con.cursor()

    cur.execute("""DELETE FROM links WHERE link='{link}' AND userid={user_id};""".format(link=link, user_id=user_id))
    con.commit()
    cur.close()
    

#возвращает записи из БД
async def send_base(user_id):
    con = sqlite3.connect("tgbot2usefullinks.db")
    cur = con.cursor()
    query = """SELECT link FROM links where userid={user_id};""".format(user_id=user_id)
    cur.execute(query)
    data = cur.fetchall()
    mm = []
    for i in data:
        mm.append(i)
    ww = len(data)
    g = []
    for i in range(ww):
        a = re.sub('|\(|\'|\,|\)', '', str(mm[i]))
        g.append(a)
    c = []
    for i in g:
        q = i + "\n"
        c.append(q)
    val = '\n'.join(c)
    return val

# Начинаем диалог по добавлению в БД
@dp.message_handler(commands=['add'])
async def cmd_link(message: types.Message):
    await Form.link.set()
    await message.answer("Отправьте ссылку")
    
# Начинаем диалог по удалению данных из БД
@dp.message_handler(commands=['del'])
async def cmd_del_link(message: types.Message):
    await Form.del_link.set()
    await message.answer("Отправьте ссылку для удаления")
    
# Сюда приходит ответ с ссылкой для добавления
@dp.message_handler(state=Form.link)
async def process_newlink(message: types.Message, state: FSMContext):
    link=message.text
    user_id = message.from_user.id
    await link_writer(link,user_id)
    await message.answer("Добавил!")
    await state.finish()
    
# Сюда приходит ответ с ссылкой для удаления
@dp.message_handler(state=Form.del_link)
async def process_dellink(message: types.Message, state: FSMContext):
    link=message.text
    user_id = message.from_user.id
    await link_remove(link,user_id)
    await message.answer("Удалил!")
    await state.finish()
    
#вывод данных из бд
@dp.message_handler(commands=['select'])
async def select_links(message: types.Message):
    user_id = message.from_user.id
    data = await send_base(user_id)
    if len(data)!=0:
        await message.answer(data)
    else:
        await message.answer("Вы не добавили ни одну ссылку")

    
    
#=====обработчики кнопок=====
@dp.callback_query_handler(lambda c: c.data == 'gr_button')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await Form.group.set()
    await bot.send_message(callback_query.from_user.id, "Напиши номер группы")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'ex_button')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await Form.group_ex.set()
    await bot.send_message(callback_query.from_user.id, "Напиши номер группы")
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data == 'cs_button')
async def process_callback_button3(callback_query: types.CallbackQuery):
    await Form.corpus.set()
    m="Введите номер корпуса из спика ниже\n"
    for name in coord:
        m+=name+"\n"
    await bot.send_message(callback_query.from_user.id, m)
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data == 'wf_button')
async def process_callback_button4(callback_query: types.CallbackQuery):
    await Form.task.set()
    await bot.send_message(callback_query.from_user.id, "Ввод примера: ")
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data == 'lnk_button')
async def process_callback_button4(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=kb.inline_kb2)
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data == 'select_button')
async def process_callback_button5(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = await send_base(user_id)
    if len(data)!=0:
        await bot.send_message(user_id, data)
    else:
        await bot.send_message(user_id, "Вы не добавили ни одну ссылку")
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data == 'add_button')
async def process_callback_button5(callback_query: types.CallbackQuery):
    await Form.link.set()
    await bot.send_message(callback_query.from_user.id, "Отправьте ссылку")
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data == 'del_button')
async def process_callback_button5(callback_query: types.CallbackQuery):
    await Form.del_link.set()
    await bot.send_message(callback_query.from_user.id, "Отправьте ссылку для удаления")
    await bot.answer_callback_query(callback_query.id)
#===========================

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)