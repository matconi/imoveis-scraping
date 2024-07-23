# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from mysql import connector
from imovelscraper import settings

class MySQLPipeline(object):
    def __init__(self):
        print(settings.DB_SETUP)
        self.create_connection()
        self.cursor = self.conn.cursor
        self.create_table()

    def create_connection(self):
        setup = settings.DB_SETUP
        self.conn = connector.connect(
            host=setup.get('host'),
            database=setup.get('database'),
            user=setup.get('user'),
            password=setup.get('password'))

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS imoveis(
            id int NOT NULL auto_increment, 
            nome VARCHAR(255),
            preco VARCHAR(255),
            codigo VARCHAR(255),
            area VARCHAR(255),
            quartos VARCHAR(255),
            url VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.store_db(item)
        #we need to return the item below as scrapy expects us to!
        return item

    def store_in_db(self, item):
        self.curr.execute(""" insert into imoveis (nome, preco, codigo, area, quartos, url) values (%s,%s,%s,%s,%s,%s)""", (
            item["nome"],
            item["preco"],
            item["codigo"],
            item["area"],
            item["quartos"],
            item["url"],
        ))
        self.conn.commit()
