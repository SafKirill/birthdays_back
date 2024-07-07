from envparse import Env
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

env = Env()

REAL_DATABASE_URL = env.str("REAL_DATABASE_URL", default=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

SECRET_KEY: str = env.str("SECRET_KEY", default="birthdays")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: str = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30000)

Email: str = env.str("Email", default="")
EmailPassword: str = env.str("EmailPassword", default="")