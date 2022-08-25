# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
#from etherator.models import db_connect, create_table
from urllib.parse import urlparse
#from flaskwebsite.models import HostnameClass
from sqlalchemy import update
from datetime import datetime as dt
from datetime import timedelta as td


import os
from urllib.parse import urlparse
import etherator.models as models


class EtheratorPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        try:
            engine = models.engine

            self.Session = sessionmaker(bind=engine)
            print("database initialized")
        except:
            raise Exception

    def process_item(self, item, spider):
        # print(f"processing")
        session = self.Session()
        today = dt.now()
        n_days_ago = today - td(days=2)
        # # for the page
        hostname_to_add = item['hostname']

        try:
            # print("in try")
            exists = session.query(models.HostnameClass).filter(
                models.HostnameClass.hostname == hostname_to_add).first()
            # print("exiting try")
            if exists:
                session.query(models.HostnameClass).filter_by(hostname=hostname_to_add).update(
                    {models.HostnameClass.hostname: item['hostname'],
                        models.HostnameClass.human_text: item['human_text'],
                        models.HostnameClass.h1: item['h1'],
                        models.HostnameClass.title: item['title'],
                        models.HostnameClass.scheme: item['scheme']})
                session.commit()
                session.close()
                # print(f"updated in exists")
            # elif exists and exists.human_text:

            #     DropItem(item)
            #     print(f"Old {hostname_to_add} break")

            elif not exists:
                # print("in not exists")
                hostname_object = models.HostnameClass()
                hostname_object.hostname = hostname_to_add
                #hostname_object.human_text = item['human_text']

                hostname_object.title = item['title']
                # hostname_object.h1 = item['h1']
                # hostname_object.urls = item['urls']
                # hostname_object.scheme = item['scheme']
                # session.add(hostname_object)
                # print(f"New - {item['hostname']}")
                session.commit()
                session.close()
                print(f"added {hostname_to_add}")
        except:
            print(f"exception {hostname_to_add}")
            raise Exception
        return item
