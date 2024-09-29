import re
import requests
from bs4 import BeautifulSoup
import csv
import os

class InfoJobs:
    def __init__(self, url):
        self.url = url

    def get_info(self) -> str:
        # Fazer a requisição
        response = requests.get(self.url)
        # Caso retorne com sucesso
        if response.status_code == 200:
            # Extrair o site
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extrair dados úteis
            # Cinco campos que buscamos estão na mesma lista, com spans da mesma classe
            # Encontrar a tag <ul> que possui itens que buscamos
            ul = soup.find('ul', class_='advisor-tabs advisor-tabs4 jsTabs')
            # Campos que vamos salvar dessa ul
            fields_dict = {
                'quantidade_avaliacoes': 0,
                'quantidade_salarios': 0,
                'quantidade_vagas': 0,
                'quantidade_entrevistas': 0,
                'quantidade_beneficios': 0
                }
            # Extrair os valores dos <span> que estão dentro de <li> na <ul>
            spans = [li.find('span').text.strip() for li in ul.find_all('li') if li.find('span')]
            spans = spans[1:] # O primeiro valor não é um número, será ignorado
            # Atualizar o dicionário
            for i, field in enumerate(fields_dict.keys()):
                if i <len(spans):
                    fields_dict[field] = spans[i]
            
            # Outros campos
            # Campo avaliação Geral
            avaliacao_geral = soup.find('span', id='ctl00_phMasterPage_cHeader_spanAnswer1_Average')
            fields_dict['avaliacao_geral'] = avaliacao_geral.text.strip() 
            # Campo Avaliação 2 (quantos % recomendaria)
            quantidade_avaliacoes2 = soup.find_all('div', class_='advisor-position-icon')
            fields_dict['quantidade_avaliacoes2'] = quantidade_avaliacoes2[0].text.strip()
            # Campo Avaliação Cultura (Ambiente de Trabalho)
            cultura_div = soup.find('div', id='ctl00_phMasterPage_cEvaluations_cEvaluations_divAnsw3')
            chosen = cultura_div.find('div', class_='advisor-evaluations-num')
            if chosen:
                fields_dict['avaliacao_cultura'] = chosen.text.strip()       
            # Campo Oportunidades
            oportunidades_div = soup.find('div', id='ctl00_phMasterPage_cEvaluations_cEvaluations_divAnsw2')
            chosen = oportunidades_div.find('div', class_='advisor-evaluations-num')
            if chosen:
                fields_dict['avaliacao_oportunidades'] = chosen.text.strip()
            # Campo Qualidade de Vida
            qualidade_vida_div = soup.find('div', id='ctl00_phMasterPage_cEvaluations_cEvaluations_divAnsw4')
            chosen = qualidade_vida_div.find('div', class_='advisor-evaluations-num')
            if chosen:
                fields_dict['avaliacao_qualidade_vida'] = chosen.text.strip() 

            print(fields_dict)

            # Gerar o CSV
            csv_file = 'sprint03_rpa_dados.csv'
            file_exists = os.path.isfile(csv_file)

            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fields_dict.keys())
                # Escrever o cabeçalho apenas se o arquivo for novo
                if not file_exists:
                    writer.writeheader()
                writer.writerow(fields_dict)

        else:
            print(f'Erro ao acessar a página. {response.status_code}')

get_itau_data = InfoJobs('https://www.infojobs.com.br/itau-unibanco')
itau_data = get_itau_data.get_info()

get_bradesco_data = InfoJobs('https://www.infojobs.com.br/banco-bradesco-sa')
bradesco_data = get_bradesco_data.get_info()

