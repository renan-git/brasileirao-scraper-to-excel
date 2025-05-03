from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests
import json

response = requests.get("https://ge.globo.com/futebol/brasileirao-serie-a/")
table_web_page = response.text

soup = BeautifulSoup(table_web_page, "html.parser")

tag_table = soup.select_one(selector="#scriptReact")
script_text = tag_table.getText()
split_classificacao = script_text.split("const classificacao")[1]
block_classificacao = split_classificacao.split(",\"edicao\"")[0]
json_data = block_classificacao.split("\"classificacao\":")[1]

brazilian_league = {
    "standings": json.loads(json_data)
}

standings_xlsx = Workbook()
first_page = standings_xlsx.active
column_names = ["Posição", "Time", "Pontos", "Jogos", "Vitórias", "Empates", "Derrotas", "Gols Pró", "Gols Contra", "Saldo de Gols", "Aproveitamento (%)"]
first_page.append(column_names)

for position_info in brazilian_league["standings"]:
    line = [position_info['ordem'], position_info['nome_popular'], position_info['pontos'], position_info['jogos'], position_info['vitorias'], position_info['empates'], position_info['derrotas'], position_info['gols_pro'], position_info['gols_contra'], position_info['saldo_gols'], position_info['aproveitamento']]
    first_page.append(line)

standings_xlsx.save("Brazilian_League_Standings.xlsx")