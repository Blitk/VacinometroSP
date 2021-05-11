from time import sleep
from bs4 import BeautifulSoup
from csv import DictWriter, DictReader
import requests
import datetime
import os
import pandas as pd

if os.path.exists('vacina.csv'):
	pass
else:
	f = open("vacina.csv", "x")
	f.close()


def Recupera():
	with open("vacina.csv") as arquivo:
		leitor = DictReader(arquivo)
		lista = []
		for linha in leitor:
			lista.append(linha)
		return lista


def Guarda(data, horario, vacinados, pDose, sDose, dados):

	with open("vacina.csv", 'w') as arquivo:

		falta = vacinados - sDose
		faltaPrimeira = população - vacinados

		dados.append({"Data":data, "Horario":horario, "Vacinados":vacinados, "P_Dose": pDose, "S_Dose":sDose, "Falta S_Dose": falta, "Falta P_Dose": faltaPrimeira})
		
		cabecalho = ["Data", "Horario", "Vacinados", "P_Dose", "S_Dose", "Falta S_Dose", "Falta P_Dose"]
		
		escritor = DictWriter(arquivo, fieldnames=cabecalho)
		escritor.writeheader()

		for item in dados:
			escritor.writerow(item)

		print(pd.DataFrame.from_dict(dados).tail(1))


url ="https://vacinaja.sp.gov.br/"

população = 44840384

print("\n")

while True:
	dados = Recupera()

	hora = datetime.datetime.now()
	data = f"{hora.day}/{hora.month}/{hora.year}"
	horario = f"{hora.hour}:{hora.minute}"

	pagina = requests.get(url)
	crawler = BeautifulSoup(pagina.text, "html.parser")

	vacinados, pDose, sDose = '', '', ''

	vacinados = str(crawler.find_all("div", {"class":"pane"}))
	vacinados = vacinados.replace("[<div class=\"pane\">", '')
	vacinados = vacinados.replace("</div>]", '')
	vacinados = vacinados.replace(".", '')
	vacinados = int(vacinados)
	
	

	buscaP = crawler.find_all("p")

	pDose = str(buscaP[5])
	pDose = pDose.replace("<p class=\"vac-doses\">", "")
	pDose = pDose.replace("</p>", '')
	pDose = pDose.replace(".", '')
	pDose = int(pDose)

	sDose = str(buscaP[7])
	sDose = sDose.replace("<p class=\"vac-doses\">", "")
	sDose = sDose.replace("</p>", '')
	sDose = sDose.replace(".", '')
	sDose = int(sDose)


	Guarda(data, horario, vacinados, pDose, sDose, dados)

	sleep(300)
	print("\n")


