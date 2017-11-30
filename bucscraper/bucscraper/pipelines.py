# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from sqlalchemy.orm import sessionmaker
from slugify import slugify

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page

from bucscraper.models import BucscraperDB, db_connect, create_table
from blog.models import BlogPage

def truncate_string(content, numberofwords=12, suffix='...'):
    if len(content) <= numberofwords:
            return content
    else:
        return ' '.join(content.split()[:numberofwords]) + suffix

class BucscraperPipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save articles in the database.

        This method is called for every item pipeline component.
        """        
        text_index = Page.objects.filter(title="Minitrue Index").first()
            
        slug_path = slugify(truncate_string(item["text"],5, ''))
        blogtitle = truncate_string(item["text"],8)
        blogpage = BlogPage()
        blogpage.body = [            
            # ('paragraph', blocks.RichTextBlock()),        
            # ('image', ImageChooserBlock()),
            ('articleIP', blocks.URLBlock(item["link"])),
        ]
        
        # blogbody = StreamField([
        #     ('heading', blogtitle),
        #     ('paragraph', blocks.RichTextBlock(item["text"])),                    
        #     ('articleIP', item["link"]),
        #])    
        print("LINK: " + item["link"])
        
        text_index.add_child(instance=BlogPage(title=blogtitle, 
                                    slug=slug_path, 
                                    intro = truncate_string(item["text"],25),
                                    body = blogpage.body
                                    # body = [            
                                    #     ('articleIP', item["link"]),
                                    # ]
        ))

        #blogpage.save()
        #session = self.Session()   
        # try:
        #     session.add(blogpage)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        # return item


    # def process_item(self, item, spider):
        # """Save deals in the database.

        # This method is called for every item pipeline component.
        # """
        # session = self.Session()
        # scraperdb = BucscraperDB()
        # scraperdb.text = item["text"]
        # scraperdb.link = item["link"]

        # try:
        #     session.add(scraperdb)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        # return item
