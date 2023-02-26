class Config:
    APPOINTED_USER = 'decan'
    APPOINTED_PASS = 'qwerty'
    APPOINTED_DB_NAME = 'studentdb'
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{APPOINTED_USER}:{APPOINTED_PASS}@/{APPOINTED_DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
