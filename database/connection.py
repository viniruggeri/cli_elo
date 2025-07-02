# backend/database/connection.py
import os
import json
from getpass import getpass
from cryptography.fernet import Fernet
import oracledb
from rich import print
from rich.console import Console

console = Console()

HOST = ""
PORT = ""
SERVICE_NAME = ""
DSN = oracledb.makedsn(HOST, PORT, service_name=SERVICE_NAME)

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "..", "db_config.json")
KEY_PATH = os.path.join(BASE_DIR, "..", "key.key")


def gerar_chave():
    chave = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(chave)


def carregar_chave():
    if not os.path.exists(KEY_PATH):
        gerar_chave()
    return open(KEY_PATH, "rb").read()


def criptografar(texto, chave):
    return Fernet(chave).encrypt(texto.encode()).decode()


def descriptografar(token, chave):
    return Fernet(chave).decrypt(token.encode()).decode()



def _salvar_login(user, password):
    chave = carregar_chave()
    config = {
        "user": criptografar(user, chave),
        "password": criptografar(password, chave),
        "dsn": criptografar(DSN, chave)
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def _carregar_login():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        chave = carregar_chave()
        return {
            "user": descriptografar(config["user"], chave),
            "password": descriptografar(config["password"], chave),
            "dsn": descriptografar(config["dsn"], chave)
        }
    return None



def cadastrar_login():
    console.print("\n[bold cyan]--- Cadastro de Login no Banco ELO ---[/bold cyan]")
    user = input("Usuário FIAP: ")
    password = getpass("Senha FIAP (não aparece ao digitar): ")

    _salvar_login(user, password)
    console.print("[bold green]✔ Login salvo com sucesso![/bold green]\n")


def get_connection():
    creds = _carregar_login()

    if not creds:
        cadastrar_login()
        creds = _carregar_login()

    try:
        conn = oracledb.connect(
            user=creds["user"],
            password=creds["password"],
            dsn=creds["dsn"]
        )
        conn.ping()
        console.print("[bold green]🟢 Conexão com Oracle realizada com sucesso![/bold green]\n")
        return conn

    except oracledb.DatabaseError as e:
        console.print(f"[bold red]❌ Falha na conexão: {e}[/bold red]")
        console.print("[yellow]Por favor, cadastre novamente suas credenciais.[/yellow]\n")
        cadastrar_login()
        creds = _carregar_login()
        conn = oracledb.connect(
            user=creds["user"],
            password=creds["password"],
            dsn=creds["dsn"]
        )
        return iter([conn])

print(get_connection())