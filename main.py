from chatterbot import chatterbot
from chatterbot.trainers import ListTrainer
from tkinter import *
import pyttsx3 as pp
import speech_recognition as s
import threading
import nltk
from nltk.chat.util import Chat, reflections


engine=pp.init()

voices = engine.getProperty('voices')
print(voices)

engine.setProperty('voice', voices[0].id)
def speak(word):
    engine.say(word)
    engine.runAndWait()
bot = chatterbot.ChatBot(
    'CoronaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)


training_data_reflection = open('training_data/reflection').read().splitlines()
training_data_quesans = open('training_data/ques_ans').read().splitlines()
training_data_personal = open('training_data/personal_qs').read().splitlines()

training_data = training_data_reflection + training_data_quesans + training_data_personal

trainer = ListTrainer(bot)
trainer.train(training_data)

main = Tk()
main.geometry("500x650")
main.title("COVID CHATBOT")
img=PhotoImage(file="chat.png")
photoL=Label(main,image=img,width=650)
photoL.pack(pady=5)


def takeQuery():
    sr=s.Recognizer()
    sr.pause_threshold=1
    print("your bot is listening try to speak")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            textF.delete(0, END)
            textF.insert(0, query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print("voice not recognized")

def ask_from_bot():
    query=textF.get()
    answer_from_bot = bot.get_response(query)
    msg.insert(END,"you : "+"\n" + query)
    print(type(answer_from_bot))
    msg.insert(END, "\n\n"+"bot : " + str(answer_from_bot))
    speak(answer_from_bot)
    textF.delete(0,END)
    msg.yview(END)

frame=Frame(main)
sc=Scrollbar(frame)
msg=Listbox(frame,width=80,height=20,yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)

msg.pack(side=LEFT, fill=BOTH,pady=10)
frame.pack()

textF=Entry(main,font=("Verdana", 20))
textF.pack(fill=X, pady=10)
btn = Button(main, text="Ask", font=("Verdana",20), command=ask_from_bot)
btn.pack()

def enter_function(event):
    btn.invoke()

main.bind('<Return>',enter_function)
def repeatL():
    while True:
        takeQuery()

t = threading.Thread(target=repeatL)
t.start()

main.mainloop()
