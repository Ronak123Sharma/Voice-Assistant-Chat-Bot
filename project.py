import pyttsx3
import speech_recognition as sr
from datetime import datetime
import os 
import cv2
import random
from requests import get
import wikipedia
import webbrowser
from googlesearch import search 
import time
import pyautogui
import pywhatkit as kit
import smtplib
import pyjokes
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import instaloader
import google.generativeai as palm
import fitz
import subprocess
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil
from word2number import w2n
import re
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
import pyaudio
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api = getenv("gemi_api_key")




engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")

# print(voices[0].id)
engine.setProperty('voice', voices[3].id)






# text to speech:
def speak(audio):
    engine.say(audio)
    engine.runAndWait()





# voice to text:
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=7)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"\nUser Said: {query}")

    except Exception as e:
        speak("say that again please...")
        return "none"
    return query



# ==================================================


# TakeCommand2 for Wake Up Word:
def takecommand_wakeUP():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=7)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"\nUser Said: {query}")

    except Exception as e:
        # speak("say that again please...")
        return "none"
    query = query.lower()
    return query


# ==================================================


# Clap Detecion Function:

threshold = 35
Clap = False

def detect_clap(indata, frames, time, status):
    global Clap
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > threshold:
        print("Clapped!")
        Clap = True


def Listen_for_claps():
    with sd.InputStream(callback=detect_clap):
        return sd.sleep(1000)



# ==================================================






# wishing function:
def wish():
    hour = int(datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak(" good morning")
    elif hour > 12 and hour < 6:
        speak(" good afternoon")
    else:
        speak(" good evening")

    speak("i am jarvis sir. please tell me how can i help you")



# to send email :
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jarvis.36963@gmail.com','tbmr wvhz iifw ivav')
    server.sendmail('jarvis.36963@gmail.com', to, content)
    server.close()




# to fetch news results :

# api-key: 2586bbd4a3d3421d8849cbc1d4cad601

def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=2586bbd4a3d3421d8849cbc1d4cad601'
    
    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")
    



# Time Remaining for Next New Year :

def format_timedelta(td):
    days, seconds = td.days, td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Create a formatted string
    formatted_time = f"{days} days, {hours:02} hours, {minutes:02} minutes, and {seconds:02} seconds"
    
    return formatted_time

def time_until_new_year():
    # Get the current date and time
    current_datetime = datetime.now()

    # Get the start of the next year
    next_year = current_datetime.year + 1
    start_of_next_year = datetime(next_year, 1, 1)

    # Calculate the time remaining
    time_remaining = start_of_next_year - current_datetime

    # Format the time remaining in a human-readable way
    formatted_time_remaining = format_timedelta(time_remaining)

    it_is = f"Time remaining until the next New Year: {formatted_time_remaining}"
    
    # Print the time remaining
    # print(f"Time remaining until the next New Year: {formatted_time_remaining}")

    return it_is



# Read Pdf Function :

def pdf_reader_func():
    speak("Sir, please enter the location of the PDF file.")
    pdf_location = input("Enter the PATH of the PDF file: ")

    try:                                                                  # C:\Users\him96\Downloads\Documents\rich-dad-poor-dad.pdf
        with fitz.open(pdf_location) as pdf_document:
            total_pages = pdf_document.page_count                               
            speak(f"Total number of pages in this book are {total_pages}.")

            speak("Sir, please enter the number of the page you want me to read")
            page_number = int(input("Please enter the Page Number: "))

            if 0 < page_number <= total_pages:
                page = pdf_document[page_number - 1]
                text = page.get_text()

                speak("Sir, reading will start after a few seconds.")
                time.sleep(0.5)
                speak(text)
            else:
                speak("Invalid page number. Please enter a valid page number.")

    except FileNotFoundError:
        speak("File not found. Please check the file path and try again.")
    except Exception as e:
        speak(f"An Error Occured: {str(e)}") 





# Hide File Function :

def hide_folders(directory):
    # Hide all folders within the specified directory and its subdirectories
    subprocess.run(["attrib", "+h", os.path.join(directory, "*"), "/s", "/d"])

def make_folders_visible(directory):
    # Make all folders within the specified directory and its subdirectories visible
    subprocess.run(["attrib", "-h", os.path.join(directory, "*"), "/s", "/d"])

def hide_file_func():
    speak("sir, please enter the path where you want to hide files.")
    directory = input("Enter the directory location: ")
    speak("sir, please tell me what you want, hide this folder or make it visible for everyone.")

    condition = takecommand().lower()

    # Ask whether to hide or make visible

    if "hide" in condition:
        hide_folders(directory)
        print(f"All folders in {directory} are now hidden.")
        speak(f"All folders in {directory} are now hidden.")
    elif "visible" in condition:
        make_folders_visible(directory)
        print(f"All folders in {directory} are now visible to everyone.")
        speak(f"All folders in {directory} are now visible to everyone.")
    elif "leave it" in condition:
        print("Ok sir")
    else:
        speak("sir, you've given no response")






# Internet Speedtest Function :

def speedtest():
    # Run the speedtest-cli command and capture the output
    print("\nCalculating Internet Speed.....\n")
    speak("sir, please wait, it will take upto 10 to 15 seconds for the speedtest")

    result = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        # Split the output into lines
        lines = result.stdout.split('\n')

        # Extract download and upload speeds
        download_speed = lines[1].split()[1]
        upload_speed = lines[2].split()[1]

        download_speed_bytes = round(float(lines[1].split()[1]) / 8, 2)
        upload_speed_bytes = round(float(lines[2].split()[1]) / 8, 2)

        # Print the results
        print(f"Download: {download_speed} Mbps")
        print(f"Upload: {upload_speed} Mbps")
        speak("sir the internet's download speed is:" + download_speed + "and the upload speed is" + upload_speed)
        speak("and if you want to know the speed in bytes per second then it's" + str(download_speed_bytes) + "download and for upload it's" + str(upload_speed_bytes))
        print("\nDownload Speed in Bytes :\n")
        print(f"Download: {download_speed_bytes} MB/s")
        print(f"Upload: {upload_speed_bytes} MB/s")
    else:
        speak("sir, there is no internet to run the speed test or maybe there is an network error")
        print("Error Running Speedtest")




# take picture :

def capture_picture(duration_seconds):
    # Open a connection to the webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    start_time = time.time()

    while time.time() - start_time < duration_seconds:
        # Read a single frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame (optional, comment out if not needed)
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)

    # Save the last captured frame as an image file (you can change the filename as needed)
    filename = "captured_picture.jpg"
    cv2.imwrite(filename, frame)

    print(f"Picture captured and saved as {filename}")

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()




# Exact Volume Function :
try:
    def set_system_volume(volume_level):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(volume_level, None)


    def extract_integers_from_string(input_string):
        # Using regular expression to find all integer values in the string
        integers_in_words = re.findall(r'\b(?:[a-zA-Z]+\s*)+\b', input_string)

        # Replace words with numerical values
        for word in integers_in_words:
            try:
                num_value = w2n.word_to_num(word)
                input_string = input_string.replace(word, str(num_value))
            except ValueError:
                # Ignore words that are not convertible to numbers
                pass

        # Using regular expression to find all integer values in the modified string
        integers = re.findall(r'\b\d+\b', input_string)

        # Converting the extracted strings to actual integers
        integers = list(map(int, integers))
        
        return integers


except Exception as e:
    print(e)    









# ========================================================




def gimi(user):

        palm.configure(api_key = api)

        defaults = {
          'model': 'models/text-bison-001',
          'temperature': 0.7,
          'candidate_count': 1,
          'top_k': 40,
          'top_p': 0.95,
          'max_output_tokens': 1024,
          'stop_sequences': [],
          'safety_settings': [
              {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 4},
              {"category": "HARM_CATEGORY_TOXICITY", "threshold": 4},
              {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 4},
              {"category": "HARM_CATEGORY_SEXUAL", "threshold": 4},
              {"category": "HARM_CATEGORY_MEDICAL", "threshold": 4},
              {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 4},
            ],

          
        }
        prompt = f"""{user}"""

        response = palm.generate_text(
          **defaults,
          prompt=prompt
        )
        gen_response=(response.result)
        
        return gen_response







# ========================================================




def TaskExecution():

# if __name__ == "__main__":
    wish()

    # takecommand()
# speak("hello sir!")


    while True:         # use this to run the prgram in loop {use this while developing the code}.
#   if 1:    # uncomment this to run the program only one time
        
        query = takecommand().lower()
        
        # open notepad :
        if "open notepad" in query:
            npath = "C:\\WINDOWS\\System32\\notepad.exe"
            os.startfile(npath)

        
        # open chrome :
        elif "open chrome" in query:
            cpath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(cpath)


        # open word :
        elif "open word" in query:
            wpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(wpath)
            

        # open powerpoint :
        elif "open powerpoint" in query:
            pptpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
            os.startfile(pptpath)


        # open whatsapp :
        elif "open whatsapp" in query:
            time.sleep(2)
            pyautogui.hotkey('win','6')              


        # open spotify :
        elif "open spotify" in query:
            spath = "C:\\Users\\him96\\AppData\\Roaming\\Spotify\\Spotify.exe"
            os.startfile(spath)
        

        # open nearby share :
        elif "open nearby share" in query:
            nspath = "C:\\Program Files\\Google\\NearbyShare\\nearby_share.exe"
            os.startfile(nspath)









































































        # open excel :
        elif "open excel" in query:
            epath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(epath)

        
        # open cmd :
        elif "open command prompt" in query:
            cmdpath = "C:\\WINDOWS\\system32\\cmd.exe"
            os.startfile(cmdpath)
        

        # open camera :
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)   # {use '0' for web camera and use  '1' for external camera}, gives error if the permission to access the camera is denied.
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k==27:               # use esc key to close the camera.
                    break;
            cap.release()
            cv2.destroyAllWindows()


        # play music :
        elif "play music" in query:
            music_dir = "C:\\Users\\him96\\Downloads\\Who Would Think That Love Radio"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))

            # for song in songs:
            #     if song.endswith('.mp3'):                          # to play only .mp3 files.   
            #         os.startfile(os.path.join(music_dir, rd))

            # os.startfile(os.path.join(music_dir, songs[0]))        # to play the list of songs in sequence.


        # get ip address :
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your ip address is {ip}")
            print(f"Your IP Address is : {ip}")

            
        # search results from wikipedia :
        elif "wikipedia" in query:
            speak("searching wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            print(f"\n{results}")


        # search results from google {type the query in terminal}, {opens the browser window}:
        elif "let me search google" in query:
            query = input("What do you want to search on Google? ")       # enables you to type your search query in terminal.
            search_url = f"https://www.google.com/search?q={query}"
            speak("Searching Google for " + query)
            webbrowser.open(search_url)                                   # make a prompt window 

        # search results form google, in form of text :
        # elif "google" in query:
        #     num_results = 1
        #     results = list(search(query, num_results=num_results))

        #     # Print and speak the search results
        #     for i, result in enumerate(results, start=1):
        #         print(f"{i}. {result}")
        #         # speak(f"Result {i}: {result}")


        # # 2. search on google :                 # opens an old internet explorer browser 
        # elif "open google" in query:
        #     speak("sir, what should i search on google")
        #     cm = takecommand().lower()
        #     webbrowser.open(f"{cm}")


        # 3. search on google :
        elif "open google" in query:
            speak("sir what should i search on google")
            tq = takecommand().lower()
            search_url = f"https://www.google.com/search?q={tq}"        # open chrome browser and search for the user requests.
            speak("Searching Google for " + tq)
            webbrowser.open(search_url) 


        # open youtube :
        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")


        # open instagram :
        elif "open instagram" in query:
            webbrowser.open("https://instagram.com")


        # open twitter "X" 
        elif "open twitter" in query:
            webbrowser.open("https://twitter.com")


#        # send whatsapp message :
#        elif "send message" in query:
#            # speak("sir, what message should i send ?")
#            # kit.sendwhatmsg_instantly("", "hello this is working.", tab_close=True, 15, 3)  
#
#            number = "+918209521532"
#
#            try:
#                # Search for the contact by name and send the message
#                kit.sendwhatmsg_instantly(number, "message_test_1",tab_close=True, 15, 3)
#                print(f"Message sent to {number} successfully!")
#            except Exception as e:
#                print(f"An error occurred: {str(e)}")
#
#            time.sleep(2)
#            pyautogui.hotkey('alt', 'f4')

            
        # close current app :
        elif "close app" in query:
            pyautogui.hotkey('alt', 'f4')


        # play youtube video by name :
        elif "play song on youtube" in query:
            kit.playonyt("baby got back")


        # play video on youtube :
        elif "play video on youtube" in query:
            speak("which video you wanna play on youtube")
            video_title = takecommand().lower()
            print(f"\nPlaying {video_title.title()} on Youtube")
            speak(f"playing {video_title} on youtube")
            kit.playonyt(video_title)



        # write in notepad :                     # {buggy} only give's 5 seconds of time to say the text.
        elif "wtie note" in query:
            os.startfile('notepad.exe')
            time.sleep(3)
            speak("sir what should i write ?")
            write = takecommand().lower()
            pyautogui.typewrite(f"{write}", interval = 0.02)



        # send email to anyone :
        elif "send email" in query:
            try:
                speak("what should i send") 
                content = takecommand().lower()
                to = "him96363@gmail.com"
                sendEmail(to, content)
                speak("the email has been sent to Himanshu")
            
            except Exception as e:
                print(e)
                speak("Sorry sir, I am unable to send an email.")



        # to end the loop :
        elif "sleep now" in query:
            speak("Okay Sir, I Am Putting My Self in Charging Mode.")
            thinking = "\n...... "
            for letters in thinking:
                time.sleep(1)
                print(letters, end='')
            print('Endgame')    
            time.sleep(0.5)
            break


        # ==============================================================

        # close apps by name :
        
        # close notepad :
        elif "close notepad" in query:
            speak("okay sir, closing notepad")
            os.system("taskkill /f /im notepad.exe")

        # close current app :
        elif "close current app" in query:
            pyautogui.hotkey('alt', 'f4')

        # to set an alarm :
        # elif "set alarm" in query:
        #     nn = int(datetime.now().hour())
        #     if nn==22:

        
        # Tell me a Joke:

        # elif "tell me a joke" in query:          # Buggy {sometimes crashes [don't use the multiple inputs with "or" like: 'tell me a joke' or 'tell a joke' or 'say a joke']}
        elif "tell me a joke" in query or "tell a joke" in query or "say a joke" in query:  
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)


        # Power Commands { shut-down, restart, sleep } :
        # shutdown :
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        # restart :
        elif "restart the system" in query:
            os.system("restart /r /t 5")

        # sleep :
        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        

        # ======================================================================

        
        
        # switch the tabs :
        elif "switch tab" in query or "switch the window" in query or "switch window" in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.keyUp('alt')

        
        # news :
        elif "news" in query or "latest news" in query or "tell me news" in query:
            speak("Sir, please wait. I am fetching the latest news.")
            news()


        # send email with attachment :
        elif "send mail" in query:

            speak("sir, what should i say")
            query = takecommand().lower()
            if "send file" in query:
                email = "jarvis.36963@gmail.com"       # your mail
                password = "tbmr wvhz iifw ivav"        # your password
                send_to_email = "receiver@gmail.com"      # receivers email
                speak("okay sir, what is the subject for this email")
                query = takecommand().lower()
                subject = query     # subject of the email 
                speak("and sir, what is the message for this email")
                query2 = takecommand().lower()
                message = query2    # the message in the mail
                speak("sir, please enter the correct path of the file into the shell")        
                file_location = input("Enter the File PATH Here: ")         # the file path for the attachment 

                speak("please wait, i am sending email now")

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject 

                msg.attach(MIMEText(message, 'plain'))
                
                # Setup the attachment 
                filename = os.path.basename(file_location)
                attachment = open(file_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment: filename= %s " % filename)

                # Attach the attachment to the MIMEMultipart object 
                msg.attach(part)

                server = smtplib.SMTP('smtp.google.com', 587)
                server.start()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()
                speak("email has been sent to Ronak")

            else:
                email = 'jarvis.36963@gmail.com'
                password = 'tbmr wvhz iifw ivav'
                send_to_email = 'receiver@gmail.com'
                message = query       # the message in the email

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                server.sendmail(email, send_to_email, message)
                server.quit()
                speak("email has been sent ronak")



        # ==========================================================================

        # twitter bot {that tweet's} :

        

        # ==========================================================================


        # to find my location using IP Address :
        elif "where i am" in query or "where we are" in query:
            try:
                speak("wait sir let me check")
                ipAdd = get('https://api.ipify.org').text
                # print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                # print(url)
                geo_requests = get(url)
                geo_data = geo_requests.json()
                # print(geo_data)
                city = geo_data['city']
                # state = geo_data['state']
                country = geo_data['country']
                print(f"\n{city}, {country}")
                speak(str("sir i am not sure, but i think we are in"+ city+ " a city of"+ country))
                print(f"\nSir I am not Sure, But I Think We are in, {city} a City of, {country}")           
            except Exception as e :
                print(str(e))
                speak("sorry sir, due to network issue i am not able to find where we are.")
                pass


        
        # ------- to check instagram profile -------- :
        elif "instagram profile" in query or "profile on instagram" in query :              # say: search for instagram profile {for it to work correctly}
            speak("sir, please enter the Username of the profile to search on instagram")
            name = input("Enter Username Here: ")
            webbrowser.open(f"https://www.instagram.com/{name}")
            speak(f"Sir, here is the profile of the user {name}")
            time.sleep(5)
            speak("sir would you like to download the profile picture of this account.")
            condition = takecommand().lower()
            
            if "yes" in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only = True)
                speak("sir, the profile picture is downloaded and saved in the main folder. i am ready for next command.")
            else:
                pass


        # Take Screenshot :
        elif "take screenshot" in query:
            speak("please wait sir, taking screenshot...")
            speak("please sir hold the screen for few seconds, i am taking screenshot")
            time.sleep(5)
            img = pyautogui.screenshot()
            file_name = "ScreenShot " + datetime.now().strftime("%Y-%m-%d %H%M%S")
            img.save(f"{file_name}.png")
            speak("i am done sir, the screenshot is saved in our main folder. now i am ready for next command.")

            
        # Tell Time :
        elif "what's the time" in query or "tell me the time" in query:
            current_time = datetime.now().strftime("%I:%M %p")
            print(f"\n{current_time}")
            speak(f"sir, it's {current_time}")


        # Tell Date :
        elif "today's date" in query or "what's the date today" in query or "tell me the date" in query:
            current_date = datetime.now().strftime("sir, its %dth %B, today is %A, and if you want to know the year it's %Y")
            # print(current_date)
            short_date = datetime.now().strftime("%a, %dth-%b %Y")
            print(f"\n{short_date}")
            speak(current_date)



        # Time Remaining Until Next New Year :
        elif "how much time left until next new year in query" in query or "when is new year" in query or "how much time left for new year" in query:
            new_year_in = time_until_new_year()
            print(new_year_in)
            speak(new_year_in)


        # ai chat mode :
        elif "chat mode" in query or "chat mod" in query:
            speak("AI chat mode is Activated")
            while True:
                speak("speak your query after the beep,,,,,,,\"Beeeep\"")
                user = takecommand().lower()
                try:
                    if "exit" in user or "close" in user:
                        speak("okay sir, AI chat mode is Deactivated")
                        break
                    else:
                        response_from_AI = gimi(user)
                        # time.sleep(10)
                        print(response_from_AI)
                        speak(response_from_AI)
                except Exception as e:
                    speak("sorry sir, i am not able to find that")


        # Read PDF :
        elif "read pdf" in query:
            pdf_reader_func()



        # ====================================================

        # To Hide Files or Folder :

        # elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
        #     speak("sir, please tell me you want to hide this folder or make it visible for everyone")
        #     condition = takecommand().lower()
            
        #     if "hide" in condition:
        #         os.system("attrib +h /s /d")
        #         speak("sir, all files in this folder are now hidden.")

        #     elif "visible" in condition:
        #         os.system("attrib -h /s /d")
        #         speak("sir, all files in this folder are now visible to everyone. i wish you are taking this decision in your own peace.")
            
        #     elif "leave it" in condition or "leave for now" in condition:
        #         speak("Ok sir")


        # -------------------- To Hide Files and Folder of a Specific Directory -------------------- :
        
        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            hide_file_func()


        # ====================================================

        # Mathematical Calculations :
        elif "do some calculations" in query or "can you calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Say, what you want to calculate, example: 3 plus 3")
                print("\nSay, what you want to calculate, example: 3 plus 3")
                print("\nListning......\n")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                    '+' : operator.add,  # add
                    '-' : operator.sub,  # subtract
                    '*' : operator.mul, # multiply
                    'divided' : operator.__truediv__,  # divided
                }[op]

            def eval_binary_expr(op1, oper, op2):      # 5 plus 4 
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak(" sir, your result is")
            result = eval_binary_expr(*(my_string.split()))
            speak(result)
            print("\nResult: ", result)

            

        # Tells the Weather Forecast :
        elif "temperature" in query:
            search = "weather in jaipur"
            url = f"https://www.google.com/search?q={search}"
            r   = get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            print(f"\nCurrent {search} is {temp}")
            speak(f"\nCurrent {search} is {temp}")



        # How to Mode :
        elif "activate how to mode" in query or "activate how to mod" in query:
            speak("How to mode is activated")
            while True:
                speak("sir, please tell me what you want to know")
                how = takecommand().lower()
                try:
                    if "exit" in how or "close" in how:
                        speak("okay sir, how to mode is closed")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("sorry sir, i am now able to find that")



        # Check Battery Percentage :
        elif "how much power left" in query or "how much power we have" in query or "battery" in query:
            
            battery = psutil.sensors_battery()
            percentage = battery.percent
            
            def charging_status():
                
                if battery.power_plugged:
                    return True
                else:
                    return False

            
            if charging_status():
                print(f"\System is on Charging, Current Battery Percentage is: {percentage}%.")
                speak(f"sir, our system is on charging, current battery percentage is {percentage} percent")
            
            else:
                print(f"\nBattery Percentage: {percentage}%.")
                speak(f"sir, our system have {percentage} percent battery")

                if percentage >= 75:
                    speak("it look's like we are having enough power to continue our work")
                elif percentage >= 40 and percentage <= 75:
                    speak("sir, we should connect our system to charging point to charge our battery")
                elif percentage <= 15 and percentage <= 30:
                    speak("sir, we don't have enough power to work, please connect to charging")
                elif percentage <= 15:
                    speak("sir, we have very low power, please connect to charging the system will shutdown very soon")
                elif percentage <= 10:
                    speak("sir, leave everything, in 5 seconds i am going to put the system sleep mode")
                    time.sleep(0.5)
                    speak("five")
                    time.sleep(1)
                    speak("four")
                    time.sleep(1)
                    speak("three")
                    time.sleep(1)
                    speak("two")
                    time.sleep(1)
                    speak("one")
                    time.sleep(0.5)
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")



        # Check Internet Speed :
        elif "internet speed" in query or "speedtest" in query:
            speak("just wait....")
            print("\njust wait....")
            speedtest()


        # Take Picture :
        elif "take a photo" in query or "take a selfie" in query or "take a picture" in query:
            capture_picture(duration_seconds=6)


        
        # Control Volume :
        # Volume UP: 
        elif "volume up" in query:
            pyautogui.press("volumeup")

        # Volume Down:
        elif "volume down" in query:
            pyautogui.press("volumedown")

        # Volume Mute:
        elif "mute" in query or "mute volume" in query:
            pyautogui.press("volumemute")
        


        # Set Exact Volume Percentage :
        elif "volume level" in query:
            speak("sir, please tell me what volume level you want to set. For example you can say, set volume to 30% ")
            input_string = takecommand().lower()

            result = extract_integers_from_string(input_string)

            con_v = result[0] / 100.0
            set_system_volume(con_v) 



        # Set Alarm :
        elif "alarm" in query:
            speak("sir, please tell me the time to set alarm, 'for example set for 5:30 am' ")

            tt = takecommand().lower()       # set alarm for 5:30 am
            
            tt = tt.replace("set alarm for ", "")   # 5:30 a.m.
            tt = tt.replace(".", "")   # 5:30 am
            tt = tt.upper()   # 5:30 AM
            import SetAlarm
            SetAlarm.alarm(tt)



        # Open Mobile Camera :
        elif "open mobile camera" in query or "phone camera" in query:
            import urllib.request
            import cv2
            import numpy as np
            ip_address_received_from_IPCamera = "http://192.168.149.159:8080/shot.jpg"
            URL = ip_address_received_from_IPCamera
            while True:
                img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
                img = cv2.imdecode(img_arr, -1)
                cv2.imshow('IPWebcam', img)
                q = cv2.waitKey(1)
                if q == ord("q"):               # Press q to quit
                    break

            cv2.destroyAllWindows()



# HotWord Detection:
if __name__=="__main__":
    while True:
        permission = takecommand_wakeUP()
        if "priya" in permission or "wake up" in permission or "bhabhi" in permission or "breakup" in permission:
            TaskExecution()
        elif "goodbye" in permission or "good bye" in permission:
            speak("thanks for using me, have a good day")
            sys.exit()



# # Clap Detection :
# if __name__ == '__main__':
#     while True:
#         Listen_for_claps()
#         if Clap==True:
#             TaskExecution()
#             break
#         else:
#             pass




