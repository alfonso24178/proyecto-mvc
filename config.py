import os

class Config:
    SECRET_KEY = 'tu_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/ticket_turno'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_SITE_KEY = '6LexyQcrAAAAAAZWBRaNvWMZj6FEtvoXnVIh5T66'
    RECAPTCHA_SECRET_KEY = '6LexyQcrAAAAAG0BIH20-v0rUXe1ulqTNJXaIp5I'