from bs4 import BeautifulSoup, element
import requests
import json


def generate_response(response:str) -> dict:
    soup = BeautifulSoup(response, 'lxml')
    a= [i.findChildren() for i in soup.find_all("table", {"class": "menu-tbl"})]
    b= [i.findChildren() for i in soup.find_all("table", {"class": "questionRowTbl"})]
    # if (len(a)!= len(b)): raise Exception
    out = dict()
    for i, (elt, tbl) in enumerate(zip(a,b)):
        subject = ""
        if (i<17): subject = "Mathamatics"
        elif (i>=17 and i<34): subject = "Physics"
        else: subject = "Chemsitry" 
        if elt[2].get_text() != "SA":
            chosen_opt = (elt[7].get_text())
            if chosen_opt != " -- ": chosen_opt = chosen_opt.strip().split(',')
            else: chosen_opt = []
            options = convertToIndex(chosen_opt)
            answers = getImages(tbl, options)
            out[int(elt[5].get_text())] = {
                "chosen_option": chosen_opt,
                "question_type": elt[2].get_text(),
                "subject": subject,
                "option_ids": answers
            }

        else:
            if ((tbl[-1].get_text()).isdigit()):

                out[int(elt[5].get_text())] = {
                    "chosen_option": str(tbl[-1].get_text()), 
                    "question_type": "SA", 
                    "subject": subject,
                    "option_ids": [str(tbl[-1].get_text())]
                    }
            else: out[int(elt[5].get_text())] = {
                    "chosen_option": [], 
                    "question_type": "SA", 
                    "subject": subject,
                    "option_ids": []
                    }
        
    return out

def getShiftData(response) -> dict:
    soup = BeautifulSoup(response, 'lxml')
    parent = soup.find("table", {"border": "1", "cellpadding": "1", "cellspacing":"1", "style":"width:500px"}).findChildren()
    shift = int(parent[-1].get_text().strip()[-1])
    roll_no = (parent[3].get_text())
    name = (parent[6].get_text())
    return {'shift': shift, "roll_no": roll_no, "name": name}


def getImages(iterable:element.ResultSet, indices:list) -> list:
    out = list()
    out_final = list()
    for elt in iterable:
        if elt.find("img"):
            out.append("https://cdn3.digialm.com//" + elt.find("img")['src'])
    out.pop(0)
    out.pop(1)
    out.pop(2)
    out.pop(3)
    out.pop(4)
    for index in indices:
        out_final.append(out[index].split('///')[-1].split('.')[0])
    # print(out_final)
    return out_final

def convertToIndex(options:list) -> list:
    out = list()
    for option in options:
        if option == "A":
            out.append(1)
        elif option == "B":
            out.append(2)
        elif option == "C":
            out.append(3)
        elif option == "D":
            out.append(4)
    return out

