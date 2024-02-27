# config.py
import mysql.connector
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password@123',
    'database': 'rewardmanagement',
    #'port': 23306,
}

from configuration.config import mysql_config
db = mysql.connector.connect(**mysql_config)
