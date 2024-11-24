import csv
import json
import sqlite3
from emailer import Emailer
import requests

FILE_PATH = "order_emails.txt"

class Util:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("mtn.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.session = requests.Session()

    def make_email_list(self):
        with open(FILE_PATH, "r") as file:
            for line in file:
                temp = dict()
                line_tesxt = line.strip()
                values = line_tesxt.split(":")
                email = values[0].strip()
                app_password = values[5].strip()
                
                temp["email"] = email
                temp["app_password"] = app_password

                emailer = Emailer(email, app_password)
                resp = emailer.get_verification_code()
                if resp == "Getting verification code error":
                    print(f"Cant access Email : {email} ")
                    nonduplicated = self.check_duplicate_mail(email)
                    if nonduplicated == True:
                        self.insert_value(email, app_password, status = "false")
                    

                else:
                    with open("email_list.csv", mode="a", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=temp.keys())
                        file.seek(0, 2)
                        if file.tell() == 0:
                            writer.writeheader()
                        
                        writer.writerow(temp)

                    nonduplicated = self.check_duplicate_mail(email)
                    if nonduplicated == True:
                        self.insert_value(email, app_password, status = "true")

    def check_duplicate_mail(self, mail):
        self.cursor.execute("SELECT * FROM tb_emails WHERE email_address = ?", (mail,))
        row = self.cursor.fetchone()
        if row is not None:
            return False
        else:
            return True
        
    def insert_value(self, email, password, status):
        temp = dict()
        temp["email_address"] = email
        temp["app_password"] = password
        temp["status"] = status

        columns = ', '.join(temp.keys())
        placeholders = ', '.join(['?' for _ in temp])
        query = f"INSERT INTO tb_emails ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(temp.values()))
        self.conn.commit()

    def get_response(self, url, params = {}):
        if params is {}:
            resp = self.session.get(url)
            return resp
        else:
            resp = self.session.get(url, params=params)
            return resp
        
if __name__ == "__main__":
    util = Util()
    util.make_email_list()