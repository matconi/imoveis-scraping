import scrapy
from imovelscraper.items import ImovelItem
import json
import urllib

class DeltaimoveisSpider(scrapy.Spider):
    # scrapy crawl deltaimoveisspider -O mydata.csv
    name = "deltaimoveisspider"
    allowed_domains = ["deltaimoveis.com.br"]
    start_urls = [f"https://{self.allowed_domains[0]}/retornar-imoveis-disponiveis"]
    total_pages = 1
    current_page = 1
    handle_httpstatus_list = [404]
    headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": f"https://www.{self.allowed_domains[0]}/venda/apartamento/uberlandia/?&pagina={str(current_page)}"
        }
    form_data = {
        "finalidade": "venda",
        "codigounidade": "",
        "codigocondominio": "0",
        "codigoproprietario": "0",
        "codigocaptador": "0",
        "codigosimovei": "0",
        "tipos": [
            {
                "codigo": "2",
                "nome": "Apartamento",
                "url_amigavel": "apartamento"
            }
        ],
        "codigocidade": "2",
        "codigoregiao": "0",
        "endereco": "",
        "edificio": "",
        "numeroquartos": "0",
        "numerovagas": "0",
        "numerobanhos": "0",
        "numerosuite": "0",
        "numerovaranda": "0",
        "numeroelevador": "0",
        "valorde": "0",
        "valorate": "0",
        "areade": "0",
        "areaate": "0",
        "areaexternade": "0",
        "areaexternaate": "0",
        "extras": "",
        "destaque": "0",
        "opcaoimovel": "0",
        "numeropagina": str(current_page),
        "numeroregistros": "20",
        "ordenacao": "valordesc",
        "cidades": {
            "codigo": "2",
            "nome": "Uberlândia",
            "estado": "MG",
            "nomeUrl": "uberlandia",
            "estadoUrl": "mg"
        },
        "condominio": {
            "codigo": "0",
            "nome": "",
            "nomeUrl": "todos-os-condominios"
        }
    }
        
    def start_requests(self):
        self.fetch_data()

    def parse(self, response):
        json_data = json.loads(response.text)
        imoveis = json_data.get('lista')
        self.total_pages = int(json_data.get('quantidade')) / int(self.form_data["numeroregistros"])

        for imovel in imoveis:
            item = ImovelItem()
            item['nome'] = imovel.get('titulo')
            item['preco'] = imovel.get('valor')
            item['codigo'] = imovel.get('codigo')
            item['area'] = imovel.get('arealote')
            item['quartos'] = imovel.get('numeroquartos')
            item['url'] = f"https://www.{self.allowed_domains[0]}/imovel/{imovel.get('url_amigavel')}/{imovel.get('codigo')}"
            item['images'] = [image.get('urlp') for image in imovel.get('fotos')]
            yield item

        if self.current_page < self.total_pages and self.current_page <= 2: # reduzir para apenas 2 paginas
            self.current_page += 1
            self.headers["Referer"] = f"https://www.{self.allowed_domains[0]}/venda/apartamento/uberlandia/?&pagina={str(self.current_page)}"
            self.form_data["numeropagina"] = str(self.current_page)
            self.fetch_data()

    def fetch_data(self):
        encoded = urllib.parse.urlencode(self.form_data)
        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            body=encoded,
            headers=self.headers,
            callback=self.parse,
        )