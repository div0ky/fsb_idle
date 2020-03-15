import http.client
import urllib
from time import sleep
import pytesseract
import requests
from PIL import Image
from .BotLog import log
from .DatabaseManager import database

# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

class CommonFunctions:
    def __init__(self):
        self.pause_length = 5

    def pause(self):
        sleep(self.pause_length)

    def is_num(self, num, v=1):
        if v == 1:
            check = num.partition(":")[0]
            try:
                check = int(check)
            except ValueError:
                pass
            return isinstance(check, int)
        if v == 2:
            check = num[1:]
            try:
                check = round(float(check), 2)
            except ValueError:
                pass
            return isinstance(check, float)
        if v == 3:
            print(len(num))
            check1 = num[0]

            try:
                check1 = round(int(check1))
            except ValueError:
                pass

            if isinstance(check1, int):
                return True
            else:
                return False

    def ocr(self, file):
        # CONVERTS AN IMAGE INTO A STRING
        log.info("Reading...")
        im = Image.open(file).convert("LA")
        base = int(float(im.size[0] * 1.5))
        wpercent = (base / float(im.size[0]))
        hsize = int(float(im.size[1]) * float(wpercent))
        im = im.resize((base, hsize), Image.ANTIALIAS)
        im.save(database.ocr_image)
        text = pytesseract.image_to_string(file, lang="eng", config='--psm 7')
        log.info(f"I think it says: {text}")
        return text

    def push(self, msg):
        ip = requests.get('https://api.ipify.org').text
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": "anj13d6adu8s3hm66pfmiwacjxwt36",
                         "user": "uGUQThApDAJfvscP5Levk419xn7yyx",
                         "message": f"{ip} - {msg}",
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        conn.getresponse()