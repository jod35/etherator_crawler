from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Integer, create_engine, Text, Boolean
from datetime import datetime
import os
from sqlalchemy import Integer, String, MetaData
from sqlalchemy import MetaData


from dotenv import load_dotenv
load_dotenv()
Base = declarative_base()

engine = create_engine(os.getenv('DB_CON_STRING'))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# TODO: webpages class to expand beyond hostnames


class HostnameClass(Base):

    __tablename__ = 'hostname_table'
    name = Column(String(), nullable=True)
    hostname = Column(String(), primary_key=True, nullable=False, unique=True)
    scheme = Column(String(), nullable=True)
    human_text = Column(String(), nullable=True)
    tokenized_words = Column(String(), nullable=True)
    tokenized_sentences = Column(String(), nullable=True)
    h1 = Column(String(), nullable=True)
    title = Column(String(), nullable=True)
    description = Column(Text(), unique=False, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    phone = Column(Text(), nullable=True)
    email = Column(String(), nullable=True)
    city_name = Column(String(), index=True, unique=False)
    state = Column(Text(), nullable=True)
    country = Column(Text(), nullable=True)
    streetAddress1 = Column(Text(), nullable=True)
    streetAddress2 = Column(Text(), nullable=True)
    pincode = Column(Text(), nullable=True)
    verified = Column(Boolean(), nullable=True, default=False)
    foundingDate = Column(Integer, nullable=True)
    pages_on_website = Column(Integer, nullable=True)
    target_account = Column(Boolean(), nullable=True, default=False)
    offer = Column(Text(), nullable=True)
    trade = Column(Text(), nullable=True)
    industry = Column(Text(), nullable=True)
    website_by = Column(Text(), nullable=True)
    urls = Column(String(), nullable=True)

    def __repr__(self):
        return f"LocalBusiness ('{self.hostname}')"

    def __str__(self) -> str:
        return super().__str__()

    def ourDictFunc(self):
        return {
            'name': self.name,
            'hostname': self.hostname,
            'scheme': self.scheme,

            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'phone': self.phone,
            'email': self.email,
            'city_name': self.city_name,
            'state': self.state,
            'country': self.country,
            'streetAddress1': self.streetAddress1,
            'streetAddress2': self.streetAddress2,
            'pincode': self.pincode,
            'verified': self.verified,
            'foundingDate': self.foundingDate,
            'pages_on_website': self.pages_on_website,
            'target_account': self.target_account,
            'offer': self.offer,
            'trade': self.trade,
            'industry': self.industry,
            'website_by': self.website_by
        }


print("commencted to database")
