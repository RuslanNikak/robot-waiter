import os
import tempfile
import pygame
import speech_recognition as sr
from gtts import gTTS

pygame.init()

# Функция для синтеза речи с использованием Google TTS
def speak(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_audio_path = f.name
    tts = gTTS(text=text, lang='ru', slow=False)
    tts.save(temp_audio_path)
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # Ensure the file is not in use before deleting
    pygame.mixer.music.unload()
    os.remove(temp_audio_path)

# Функция для записи аудио
def speaks():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak("Скажите...")
        try:
            data = r.record(source, duration=3)
            text = r.recognize_google(data, language='ru')
            print(text)
            return text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Словари для распознавания ключевых слов
first = ['первое', 'первые', 'первый', 'первая']
second = ['второе', 'вторые', 'второй']
desert = ['десерт']
soup = ['суп', 'куриный', 'овощной']
salad = ['салат', 'цезарь', 'греческий']
meat = ['мясное', 'говядина', 'курица']
fish = ['рыбное', 'лосось', 'креветки']
ice = ['мороженое', 'сливочное', 'шоколадное']
cake = ['торт', 'тортик', 'банановый', 'малиновый']
finish = ['Завершить']
back = ['назад']
add = ['добавить']
dish = []

# Функция для обработки заказа
def process_order(text, state):
    if state == 'ordering':
        if text in first:
            speak("Прекрасно! Какое именно первое блюдо вас интересует? Ответьте пожалуйста: суп или салат. Если хотите вернуться скажите: назад.")
            return 'first'
        elif text in second:
            speak("Прекрасно! Какое именно второе блюдо вас интересует? Ответьте пожалуйста: мясное или рыбное. Если хотите вернуться скажите: назад.")
            return 'second'
        elif text in desert:
            speak("Прекрасно! Какой именно десерт вас интересует? Ответьте пожалуйста: мороженое или тортик. Если хотите вернуться скажите: назад.")
            return 'desert'
    elif state == 'first':
        if text in soup:
            speak("У нас есть несколько вариантов супов. Ответьте пожалуйста: куриный или овощной. Если хотите вернуться скажите: назад.")
            return 'first_soup'
        elif text in salad:
            speak("У нас есть несколько вариантов салатов. Ответьте пожалуйста: цезарь или греческий. Если хотите вернуться скажите: назад.")
            return 'first_salad'
    elif state == 'first_soup':
        if text == 'куриный' or text == 'овощной':
            speak(f"Ваш заказ: {text} суп. Чтобы завершить заказ скажите: завершить. Если хотите что-то добавить скажите: добавить.")
            dish.append(f'{text} суп')
            if text == 'добавить':
                speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
            elif text == 'завершить':
                return 'final'
    elif state == 'first_salad':
        if text == 'цезарь' or text == 'греческий':
            speak(f"Ваш заказ: салат {text}. Чтобы завершить заказ скажите: завершить. Если хотите что-то добавить скажите: добавить.")
            dish.append(f'{text}')
            if text == 'добавить':
                speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
            elif text == 'завершить':
                return 'final'
    elif state == 'second':
        if text in meat:
            speak("У нас есть несколько вариантов мясных блюд. Ответьте пожалуйста: говядина или курица. Если хотите вернуться скажите: назад.")
            return 'second_meat'
        elif text in fish:
            speak("У нас есть несколько вариантов рыбных блюд. Ответьте пожалуйста: лосось или креветки. Если хотите вернуться скажите: назад.")
            return 'second_fish'
    elif state == 'second_meat':
        if text == 'говядина' or text == 'курица':
            speak(f"Ваш заказ: {text}. Чтобы завершить заказ скажите: завершить. Если хотите что-то добавить скажите: добавить.")
            dish.append(f'{text}')
            if text == 'добавить':
                speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
            elif text == 'завершить':
                return 'final'
    elif state == 'second_fish':
        if text == 'лосось' or text == 'креветки':
            speak(f"Ваш заказ: {text}. Чтобы завершить заказ скажите: завершить. Если хотите что-то добавить скажите: добавить.")
            dish.append(f'{text}')
            if text == 'добавить':
                speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
            elif text == 'завершить':
                return 'final'
    elif state == 'desert':
        if text in ice:
            speak("У нас есть несколько вариантов мороженого. Ответьте пожалуйста: сливочное или шоколадное. Если хотите вернуться скажите: назад.")
            return 'desert_ice'
        elif text in cake:
            speak("У нас есть несколько вариантов тортиков. Ответьте пожалуйста: банановый или малиновый. Если хотите вернуться скажите: назад.")
            return 'desert_cake'
    elif state == 'desert_ice':
        if text == 'сливочное' or text == 'шоколадное':
            speak(f"Ваш заказ: {text} мороженое. Чтобы завершить заказ скажите: завершить. Если хотите что-то добавить скажите: добавить.")
            dish.append(f'{text} мороженое')
            if text == 'добавить':
                speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
            elif text == 'завершить':
                return 'final'
    elif state == 'desert_cake':
        if text == 'банановый' or text == 'малиновый':
            speak(f"Ваш заказ: тортик {text}. Чтобы завершить заказ скажите: завершить. Если хотите что-то добавить скажите: добавить.")
            dish.append(f'тортик {text}')
            if text == 'добавить':
                speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
            elif text == 'завершить':
                return 'final'
    if text in back or text in add:
        speak("Что бы вы хотели заказать? Ответьте пожалуйста: первое, второе или десерт?")
        return 'ordering'
    else:
        return state

# Главная логика программы
def main():
    speak("Добрый день! Меня зовут Моня! Я робот ассистент, который поможет вам с заказом. Для заказа скажите: заказ.")
    
    state = 'main'
    
    while True:
        user_input = speaks()
        if user_input is not None:
            user_input = user_input.lower()
            if state == 'main' and user_input == 'заказ':
                speak("Выберите какое блюдо вас интересует: первое, второе или десерт?")
                state = 'ordering'
            else:
                state = process_order(user_input, state)
            
            if state == 'final':
                speak(f"Заказ {dish} завершен. Спасибо за ваш заказ!")
                break

if __name__ == "__main__":
    main()