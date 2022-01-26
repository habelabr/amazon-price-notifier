import requests
from bs4 import BeautifulSoup
import smtplib
import os
import datetime as dt
import time

EMAIL = os.environ["DUMMY_EMAIL"]
PASS = os.environ["PASSWORD"]
RECIPIENT = os.environ["TO_EMAIL"]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99"
                  " Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

AMAZON_URL = "https://www.amazon.com/Oculus-Quest-Advanced-All-One-Virtual/dp/B09B8DQ26F/ref=lp_16225009011_1_4"


# ---------------------------------------------------------------------------------------------------------------------#

def time_checker(the_time):
    if 0 < the_time < 12:
        return "morning!"
    elif 12 < the_time < 17:
        return "afternoon!"
    elif 17 < the_time < 21:
        return "evening!"
    else:
        pass


# ---------------------------------------------------------------------------------------------------------------------#
# GET THE DATA FROM AMAZON
response = requests.get(url=AMAZON_URL, headers=headers)
amazon_html = response.text

# MAKING THE SOUP
soup = BeautifulSoup(amazon_html, "lxml")

# GET BS4 TO HOLD THE PRICE OF THE GOOD
price_str = soup.find(name="span", class_="a-size-medium a-color-price priceBlockBuyingPriceString",
                      id="priceblock_ourprice").getText()
price = int(float(price_str.split("$")[1]))

# GET BS4 TO HOLD THE TITLE OF THE GOOD
title_raw = soup.find(name="span", class_="a-size-large product-title-word-break", id="productTitle").getText()
split1 = title_raw.split("        ")[1]
replace_1 = split1.replace("       ", "")
the_subject = replace_1.replace(" — ", " - ")

# HOUR CHECKER
time_now = dt.datetime.now().strftime("%H")
time_int = int(time_now)

# MESSAGES
TIME = time_checker(time_int)
MESSAGES = f"Good {TIME}\nThere's a change in price that would favor you right now. \n\nThe price is now only " \
           f"${price}! \n\nCheck {AMAZON_URL}"

# EMAIL
while True:
    if price < 400:
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASS)
            connection.sendmail(from_addr=EMAIL, to_addrs=RECIPIENT,
                                msg=f"Subject:{the_subject} has changed!\n\n{MESSAGES}")
        time.sleep(3600)

