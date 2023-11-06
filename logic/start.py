from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from aiogram import types
from logic.scrap.main_state import *
from logic.scrap.keyboards import *


# ETC
RETURN_TO_QUEST = "Вернемся к квесту"
GOOD_WORDS = "Перед тем как ответить на вопрос, хотелось бы передать поздравления от меня (Степана). Игорь Олегович, с днем рождения! Желаю счастья, здоровья, что бы студенты и школьники учились, чтобы работники ИВЦ работали хорошо (они вроде бы и так работают неплохо) и всего самого наилучшего!"
ERROR = 'Неправильно!'

# START
SECOND_START_MESSAGE = "Первую подсказку можно найти на нашей любимой *****, Она помогает нам искать репозитории. Далеко прятать не стали, лежит на видном месте"
START_MESSAGE = '''Игорь Олегович, мы хотим поздравить вас с днем рождения и пожелать всего самого наилучшего, любви, счастья, самое главное здоровья, мы приготовили для вас подарок, но чтоб его получить нужно пройти квест!
'''

# FIRST
FIRST_ANSWER = "2021"
SECOND_QUESTION = '''Следующий вопрос заключается в знании вай-фай сетей.
Какая вай-фай сеть существует на нашем этаже кроме скайнета?'''

# SECOND
SECOND_ANSWER = "MacLab"
THIRD_QUESTION = '''Ура, вы ответили правильно, хотим заметить, что вы хорошо знаете топологию сетей нашего этажа( в отличии от нас)'''
WELLCOME_TO_THE_CLUB_BUDDY = "Давайте перейдем в 233 аудиторию!"
LAZZY = "Тут мы уже обленились и не смогли придумать загадку, поэтому просто спрятали правильный ответ на бумажке))"

# THIRD
THIRD_ANSWER = "Сейф"
THIRD_HELP = "Как называется несгораемый ящик для хранения денег"
SUCCESS = 'Правильно!'
FOURTH_QUESTION = "Раньше данная аудитория находилась под нашей ответственностью"
HELP_FOR_THIRD_MESSAGE = "Если Вы догадались что это за аудитория, то было бы классно в неё зайти, ведь там можно найти ответ для перехода к следующему вопросу"

# FOURTH
FOURTH_ANSWER = "ФИЛФАК"
FIFTH_QUESTION = "Следующим помещением будет место, где вы обучаете детей информационным технологиям."

# FIFTH
FIFTH_ANSWER = "PascalABC"
FIFTH_HELP = "Новоиспеченный склад техники"
SIXTH_QUESTION = "Вот мы и подходим к завершению квеста и плавно передвигаемся в аудиторию 232"

# SIXTH
SIXTH_ANSWER = "Я тут!"
SEVENTH_QUESTION = "Скажем только одно.\nСогласно уставу, солдат должен стойко переносить тяготы и лишения воинской службы."


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(START_MESSAGE)
    await message.answer(
        SECOND_START_MESSAGE, reply_markup=first_keyboard())
    await MainState.first.set()


@dp.message_handler(state=MainState.first)
async def first_question(message: types.Message, state: FSMContext):
    # keyboard
    await question_markup(message=message,
                          next_state=MainState.second,
                          answer=FIRST_ANSWER, help_message=None, questions=[SECOND_QUESTION], error=ERROR,
                          state=state, question_keyboard=ReplyKeyboardRemove())


@dp.message_handler(state=MainState.second)
async def second_question(message: types.Message, state: FSMContext):
    await question_markup(message=message, next_state=MainState.third, answer=SECOND_ANSWER, help_message=None,
                          questions=[THIRD_QUESTION, WELLCOME_TO_THE_CLUB_BUDDY, LAZZY], error=ERROR, state=state,
                          question_keyboard=help_keyboard())


@dp.message_handler(state=MainState.third)
async def third_question(message: types.Message, state: FSMContext):
    await question_markup(message=message, next_state=MainState.fourth, answer=THIRD_ANSWER, help_message=THIRD_HELP,
                          questions=[SUCCESS, FOURTH_QUESTION,
                                     HELP_FOR_THIRD_MESSAGE],
                          error=ERROR, state=state, question_keyboard=ReplyKeyboardRemove())


@dp.message_handler(state=MainState.fourth)
async def fourth_question(message: types.Message, state: FSMContext):
    await question_markup(message=message, next_state=MainState.fifth, answer=FOURTH_ANSWER, help_message=None,
                          questions=[FIFTH_QUESTION], error=ERROR, state=state,
                          question_keyboard=help_keyboard())


@dp.message_handler(state=MainState.fifth)
async def fifth_question(message: types.Message, state: FSMContext):
    await question_markup(message=message, next_state=MainState.sixth, answer=FIFTH_ANSWER, help_message=FIFTH_HELP,
                          questions=[SIXTH_QUESTION], error=ERROR,
                          state=state, question_keyboard=i_am_there())


@dp.message_handler(state=MainState.sixth)
async def sixth_question(message: types.Message, state: FSMContext):

    await question_markup(message=message, next_state=MainState.seventh, answer=SIXTH_ANSWER, help_message=None,
                          questions=[GOOD_WORDS, RETURN_TO_QUEST, SEVENTH_QUESTION], error=ERROR,
                          state=state, question_keyboard=ReplyKeyboardRemove())


async def question_markup(message: types.Message, next_state: MainState, answer, help_message, questions: list, error,
                          state: FSMContext, question_keyboard: ReplyKeyboardMarkup):
    user_answer = message.text.upper()
    if user_answer == "Дай подсказку!".upper():
        await message.answer(help_message) if help_message is not None else await message.answer(
            "Для этого вопроса нет подсказки :(")
        return
    if user_answer == answer.upper():
        for question in questions:
            await message.answer(question, reply_markup=question_keyboard)
        await state.set_state(next_state)
        return
    await message.answer(error)
    return
