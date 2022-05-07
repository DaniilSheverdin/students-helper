# students-helper / Бот помощник для студентов ТулГу
<p>Данный телеграм бот написан с использованием aiogram.</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651827531/img/1_dzyoek.png" width=45%/>
</p>
<p>При запуске бот предоставляет пользователю Inline клавиатуру для управления</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651827741/img/2_rcwol3.png" width=45%/>
</p>

### Расаписание занятий

<p>Рассмотрим работу фукции предоставления расписания занятий (для существующей и не существующей группы):</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651828191/img/1_a76cgk.gif" width=60%/>
</p>
<p>Бот получает расписание по id группы с <a href="https://tsu.tula.ru/education/timetable/">официального сайта ТулГУ</a>
  
### Расаписание экзаменов

<p>Аналогичным образом работает функция по предоставлению расписания экзаменов:</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651828775/img/2_zvwtpa.gif" width=60%/>
</p>

### Адреса корпусов

<p>Рассмотрим функцию отправки адреса корпуса университета</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651829039/img/3_bdoxzp.gif" width=60%/>
</p>

### Wolfram
<p>Бота так-же можно использовать для решения уравнений и математических выражений.</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651829556/img/4_ydhfmy.gif" width=60%/>
</p>
<p>Для этого бот использует API Wolfram Alpha</p>

### Менеджер ссылок
<p>Бота можно использовать для хранения полезных ссылок.</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651829556/img/5_hedsox.gif" width=60%/>
</p>
<p>Для этого бот исползует sqlite3. Ссылки хранятя в таблице со следующими атрибутами:</p>

```
"id"	integer,
"name"	text NOT NULL,
"userid"	integer,
PRIMARY KEY("id" AUTOINCREMENT)
```
### Отказ-отмена
<p>Из любого начатого диалога можно выйти с помощью команды /cancel</p>
<p align="center">
  <img src="https://res.cloudinary.com/duhxeavu0/image/upload/v1651829556/img/6_bqvzne.gif" width=60%/>
</p>
<hr/>
<p>P.S.</p>
<p> Бот создавался посреди горящих дедлайнов по учебе и творческого кризиса (не знаю, что тут добавить на 500+ строк)...</p>




