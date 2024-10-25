import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = str(os.getenv('DATABASE_HOST'))
DATABASE_NAME = str(os.getenv('DATABASE_NAME'))
DATABASE_USER = str(os.getenv('DATABASE_USER'))
DATABASE_PASSWORD = str(os.getenv('DATABASE_PASSWORD'))
APP_SECRET_KEY = str(os.getenv('APP_SECRET_KEY'))


PSQLURL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
print(PSQLURL)


# class Config:
#     DEBUG = False
#     Testing = False
#     SECRET_KEY = str(os.getenv('APP_SECRET_KEY'))
#     SQLALCHEMY_DATABASE_URI = DATABASE_URI
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     BCRYPT_LOG_ROUNDS = 13
#     WTF_CSRF_ENABLED = True
#     DEBUG_TB_ENABLED = False
#     DEBUG_TB_INTERCEPT_REDIRECTS = False