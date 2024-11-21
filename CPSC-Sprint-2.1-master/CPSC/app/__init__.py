# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


# Import core packages
import os
import pymysql
# Import Flask 
from flask import Flask

# Inject Flask magic
app = Flask(__name__)
app.secret_key = "12345678"

# Import routing to render the pages

dbConn = pymysql.connect(
    host='mysql-cpsc.cxqi48o8ig0e.us-east-1.rds.amazonaws.com',
    port=3306,
    user='vinson', 
    password='vinsoncpsc',
    database='CPSCProject',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = dbConn.cursor()



from app import views