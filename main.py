import os
from pytube import YouTube
import moviepy.editor
import telebot
from auth_data import token


def get_video(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    video_name = youtubeObject.title
    
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")

    return video_name


def conversion(video_name):
    try:
        with moviepy.editor.VideoFileClip(f'{video_name}.mp4') as video:
            audio = video.audio
            audio.write_audiofile(f'{video_name}.mp3')
    except Exception as e:
        print("An error has occurred during conversion:", str(e))


def closer(video_name):
    os.remove(f'{video_name}.mp4')
    os.remove(f'{video_name}.mp3')


def manufactorer(link):
    video_name = get_video(link)
    video_name = ''.join(symbol for symbol in video_name if symbol.isalnum() or symbol == ' ')
    conversion(video_name)

    return video_name


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет! Пришли мне ссылку на YouTube-видео, а я пришлю тебе файл видео и файл аудио!")

    
    @bot.message_handler(content_types=["text"])
    def send_message(message):
        if 'yout' in message.text:
            try:
                bot.send_message(message.chat.id, "Отлично! Я получил твою ссылку! Теперь подожди немного, я скачаю твоё видео.")
                video_name = manufactorer(message.text)
                bot.send_message(message.chat.id, "Видео уже у меня! Сейчас достану из него аудио и всё пришлю!")
                
                try:
                    with open(f"{video_name}.mp4", 'rb') as video:
                        bot.send_video(message.chat.id, video, timeout=120)
                        bot.send_message(message.chat.id, "Держи видео!")
                        video.close()
                except Exception as ex:
                    print(ex)
                
                
                try:
                    with open(f"{video_name}.mp3", 'rb') as audio:
                        bot.send_audio(message.chat.id, audio, timeout=120)
                        bot.send_message(message.chat.id, "Держи аудио!")
                        audio.close()
                except Exception as ex:
                    print(ex)

                
                closer(video_name) 

            except Exception as ex:
                print(ex)
        else:
            bot.send_message(message.chat.id, "Это не ссылка на YouTube-видео!")      
    
    bot.polling()



if __name__ == '__main__':
    telegram_bot(token)