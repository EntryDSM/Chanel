from os import environ

SERVICE_NAME = environ.get("SERVICE_NAME", "Chanel")
RUN_ENV = environ.get("RUN_ENV")

VAULT_ADDRESS = environ.get("VAULT_ADDRESS")
VAULT_TOKEN = environ.get("VAULT_TOKEN")
GITHUB_TOKEN = environ.get("GITHUB_TOKEN")

LOGO = """
   ___  _                          _ 
  / __\| |__    __ _  _ __    ___ | |
 / /   | '_ \  / _` || '_ \  / _ \| |
/ /___ | | | || (_| || | | ||  __/| |
\____/ |_| |_| \__,_||_| |_| \___||_|
"""
