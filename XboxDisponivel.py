from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from termcolor import colored

print(colored("""
    Aplicativo utilizar Selenium para automatizar a pagina da web : https://www.xbox.com/pt-BR/consoles/xbox-series-x#purchase 
    buscando os precos e disponibilidades do Xbox Series X e envia para o email cadastrado.
    Vale ressaltar que a integracao apenas funciona com o gmail e com sua configuracao para permitir envio de email por app
    voce pode conferir como fazer neste link: https://support.google.com/accounts/answer/6010255

    Para mais informacoes veja o codigo no Github : https://github.com/GaberRB/Xbox_Series_X_Estoque
""", 'yellow'))

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


data = {}
if not checkFileExistance('credencial.json'):
    with open('credencial.json', 'w') as outfile:
        data['email'] = input(colored("Digite seu email: ", 'green')) 
        data['senha'] = input(colored("Digite sua senha: ",'green'))
        json.dump(data, outfile)   

with open('credencial.json', 'r') as json_file:
    try:
        data = json.load(json_file)
        print(len(json_file))
    except:
        data['email'] = input(colored("Digite seu email: ", 'green')) 
        data['senha'] = input(colored("Digite sua senha: ",'green'))
        with open('credencial.json', 'w') as outfile:
            json.dump(data, outfile)           

url = "https://www.xbox.com/pt-BR/consoles/xbox-series-x#purchase"
email = data['email']
emailTo = data['email']
senha = data['senha']

options = webdriver.ChromeOptions()
options.add_argument("--headless")


driver = webdriver.Chrome(ChromeDriverManager().install(), #chrome_options=options
)
driver.get(url)

sleep(5)
abrirModalDisponibilidade = driver.find_element_by_xpath('//*[@id="standalonePurch"]/div/a/span')
abrirModalDisponibilidade.click()
#Lojas Disponiveis
loja = []
for n in range(6):
    n = n + 1
    elemento = f'//*[@id="XB19_RRT-00006"]/div[2]/div/div[2]/div/div[{str(n)}]/span[1]/img'
    loja.append(driver.find_element_by_xpath(elemento).get_attribute('alt'))


#Precos
preco = []
for n in range(6):
    n= n + 1
    elemento = f'//*[@id="XB19_RRT-00006"]/div[2]/div/div[2]/div/div[{str(n)}]/span[2]'
    preco.append(driver.find_element_by_xpath(elemento).text)

# #Estoque
estoque = []
for n in range(6):
    n= n + 1
    elemento = f'//*[@id="XB19_RRT-00006"]/div[2]/div/div[2]/div/div[{str(n)}]/span[3]/span'
    estoque.append(driver.find_element_by_xpath(elemento).text)
  

driver.quit()


def sendEmail(loja, preco, estoque):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    subject = f"[BOT] Xbox Series X {loja} por R${preco}"
    
    message  = f"""
        <p>Xbox Series X</p>
        <ul>
        <li>Loja:{loja} Preco: R${preco} Disponivel: {estoque}</li>
        </ul>
        """
    server.login(email, senha)

    email_msg = MIMEMultipart()
    email_msg['From'] = email
    email_msg['To'] = emailTo
    email_msg['Subject'] = subject
    email_msg.attach(MIMEText(message, 'html'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

    print('Email enviado')

    server.quit()

x =0
for n in estoque:
    if n != 'ESGOTADO':
        sendEmail(loja[x], preco[x], estoque[x])
  
    x = x + 1



