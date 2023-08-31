from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import re

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

pagename = "https://www.imobiliare.ro/vanzare-apartamente/bucuresti?id=217430108"

driver.get(pagename)

time.sleep(5)

driver.implicitly_wait(5)

final_vector = []
total_linkuri = []
ok = 0
i = -1
ind = 1

lista_finala = open("lista_anunturi.txt", "w")


while ind <= 37:
    driver.implicitly_wait(7)
    time.sleep(7)

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    total_anunturi = driver.find_element_by_class_name("container-box-anunturi")

    anunturi = total_anunturi.find_elements_by_class_name("border-box")
    preturi = total_anunturi.find_elements_by_class_name("pret-mare")
    caracs = total_anunturi.find_elements_by_class_name("caracteristici")
    linkuri = total_anunturi.find_elements_by_class_name("img-block")
    total_linkuri.extend(linkuri)
    i = -1

    for anunt in anunturi:
        try:
            anunt.find_element_by_class_name("caracteristici")
            i += 1
            try:
                anunt.find_element_by_class_name("metrou")
                results = []
                results = re.findall(r"[-+]?\d*\.\d+|\d+", caracs[i].text)
                results.append("1")
                rap = float(float(preturi[i].text) * 1000 / float(results[1]))
                metri = []
                metri = re.findall(r"[-+]?\d*\.\d+|\d+", anunt.find_element_by_class_name("metrou").text)
                link = linkuri[i].get_attribute("href")
                final_vector.append((rap, int(results[2]), int(results[3]), int(metri[0]), link))
            except:
                ok = 1
        except:
            ok = 1
    ind += 1
    if ind == 38:
        break
    driver.get(pagename + "&pagina=" + str(ind))

final_vector.sort()
for elem in final_vector:
    lista_finala.write(elem[4])
    lista_finala.write("\n")
    #print(total_linkuri[elem[4]].get_attribute("href"))

lista_finala.close()

driver.quit()