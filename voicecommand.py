import time
import speech_recognition as sr
import os
import pyautogui

command_db = {
	"open terminal": "exec xfce4-terminal",
	"open browser": "exec firefox",
	"open editor": "exec code"
}

def callback(recognizer, audio):
	try:
		text = recognizer.recognize_whisper(audio, language="english").lower().strip()
		print(text) # for debugging
		
		if text.startswith("type"):
			type_text = text.replace("type", "", 1)
			print(f"typing: {type_text}")
			pyautogui.write(type_text, interval=0.1)
		else:
			for key, value in command_db.items():
				if key in text:
					print(f"running '{value}'")
					os.system(value)
					break
				
	except sr.UnknownValueError:
		print("could not understand audio")
	except sr.RequestError as e:
		print("an error occurred: {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()

# adjust for ambient noise for 1 second
with m as source:
	r.adjust_for_ambient_noise(source, duration=1.0)

stop_listening = r.listen_in_background(m, callback)


for _ in range(360): 
	time.sleep(1)

stop_listening(wait_for_stop=True)
