import yaml
import pandas as pd
import pymysql
import streamlit as st

# import os
# import sqlite3

class DataBase:
    def __init__(self, f_config="env/db_userinfo.yml"):
        self.uInfo = self.db_load_config(f_config)
        self.dbinfo = self.uInfo['remote-nas']
        self.con = self.db_open(self.dbinfo)
        self.cursor = self.con.cursor()
    
    def db_load_config(self, f_config):
        with open(f_config, 'r') as fid:
            uInfo = yaml.load(fid, Loader=yaml.FullLoader)
        return uInfo
    
    def db_open(self, dbinfo):
        return pymysql.connect(
            host=dbinfo["host"],
            user=dbinfo["user"],
            port=dbinfo["port"],
            password=dbinfo["pwd"],
            database=dbinfo["dbname"][0]
        )

    def table_columns(self, table_name):
        query = f"DESCRIBE {table_name}"
        self.cursor.execute(query)
        column_names = [row[0] for row in self.cursor.fetchall()]
        return column_names
    
    def read_table(_self, tbl, site=None):
        """
        - `site`: integer, 站点编号
        - `tbl` : string, 数据库名
        """
        if site is None:
            sql = f"SELECT * FROM {tbl}"
        else:
            sql = f"SELECT * FROM {tbl} WHERE (`site` = {site})"
        
        _self.cursor.execute(sql)
        data = _self.cursor.fetchall()
        column_names = _self.table_columns(tbl)
        df = pd.DataFrame(data, columns=column_names)
        return df

    def close(self):
        self.cursor.close()
        self.con.close()


def hello():
    print("hello")
