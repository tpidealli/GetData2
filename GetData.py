import requests
import bs4
import re
import json

def getLogo(url):
    r = requests.get(url)
    return r.text

def getPhone(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}  # This is chrome, you can set whatever browser you like
    r = requests.get(url, headers=headers)
    return r.text

phoneRegex = re.compile(r'''(
(\d{3}|\(\d{3}\))?              # Area Code(Optional)
(\s|-|\.)                       # Separator
(\d{3})                         # First Three Digits
(\s|-|\.)                       # Separator
(\d{4})                         # Last Four Digits
(\s*(ext|x|ext.)\s*(\d{2,5}))?  # Extension
)''', re.VERBOSE)

f = open("websites.txt", "r", encoding="utf-8")
msg = f.readlines()
contatos = {"contatos": []}
phone=''
for linha in msg:
    url = linha
    url = url.replace("\n", "")
    try:
        htmldata = getPhone(url)
        text = str(bs4.BeautifulSoup(htmldata, 'html.parser'))
        phone_groups = phoneRegex.findall(text)

        for group in phone_groups:
            print(group[0])
            phone = str(group[0])

        htmldata = getLogo(url)
        soup = bs4.BeautifulSoup(htmldata, 'html.parser')
        for item in soup.find_all('img'):
            print(item['src'])
            logo = str(item['src'])

        contatos["contatos"].append(
               {
                    "phone": phone,
                    "logo": logo,
                    "website": url
               }
        )


    except:
        print ('Not Found: ' + str(htmldata))
        continue

with open("contatos.json", "w") as arquivo:
    json.dump(contatos, arquivo, indent=4)
