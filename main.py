import requests
from bs4 import BeautifulSoup
import smtplib
import os

my_email = os.environ.get("GMAIL_EMAIL")
password = os.environ.get("GMAIL_PASSWORD")

URL = "https://www.amazon.com/dp/B0CJYCP414/?coliid=I3OSBS7PLUDYY4&colid=8S93CBDPE3P9&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it_im"

header = {
    "User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(URL, headers=header)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

with smtplib.SMTP("smtp.gmail.com") as connection:
    if price_as_float <= 50:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject: Special Offer - Price is Low!\n"
            f"Price is {price_as_float} buy it now!\n\n{URL}"
        )
    else:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:UGLY ASS BITCH, you can't afford it!\n"
            f"Price is still too high\n\n{URL}!"
        )
