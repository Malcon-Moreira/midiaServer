import sqlite3
import subprocess

from dotenv import load_dotenv
import os
import bcrypt

BANCO = os.getenv('BANCO')

def connect_banco():
    conn = sqlite3.connect(BANCO)
    return conn


def check_user_exists(username):
    conn = connect_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario FROM cadastro")
    rows = cursor.fetchall()
    for row in rows:
        if username == row[0]:
            return True
    conn.close()
    return False


def add_user(username, password):
    conn = connect_banco()
    cursor = conn.cursor()
    senha_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO cadastro (usuario, senha) VALUES (?, ?)", (username, senha_hashed))
    conn.commit()

def check_login(username, password):
    conn = connect_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM cadastro WHERE usuario = ?", (username,))
    senha_banco = cursor.fetchone()
    if not senha_banco:
        return False
    if bcrypt.checkpw(password.encode(), senha_banco[0]):
        return True
    else:
        return False

