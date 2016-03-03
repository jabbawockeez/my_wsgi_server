#coding:utf8
import os

#site settings
site_options = dict(
    site_name="Justfly's Blog",
    subtitle="a web developer, loves pyton and go",
    author="Justfly He",
    description="我的个人技术博客，关注python和go语言！",
    keywords=["python", "go"],
    password="pengfei1018",
    index_page_size=5,
    archive_page_size=20,
    navs=[
        dict(name="Home", link="/"),
        dict(name="Archive", link="/archive"),
        dict(name="About", link="/about"),
    ],
    copyright="Justfly He",
    duoshuo_shortname="justflyBlog",
    theme="modernist"
)

#system settings
COOKIE_SECRET = "justfly"

#bae settings
BAE_DB_NAME = "erxpumIHVvVVQalnlJuD"

#database settings
if "SERVER_SOFTWARE" in os.environ:
    try:
        import sae.const as const
        db_name = const.MYSQL_DB
    except:
        from bae.core import const
        db_name = BAE_DB_NAME
    DATABASE_URI = "mysql://%s:%s@%s:%s/%s?charset=utf8" % (
        const.MYSQL_USER,
        const.MYSQL_PASS,
        const.MYSQL_HOST,
        const.MYSQL_PORT,
        db_name
    )
    DATABASE_ECHO = False
    DEBUG = False
else:
    DATABASE_URI = "sqlite:///db/data.db"
    DATABASE_ECHO = True
    DEBUG = True
