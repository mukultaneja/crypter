# BSD 3-Clause License
# Copyright (c) 2024, mac
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

import os
import json
import click
import logging
from crypter_main import CrypterMain
from crypter_command_loader import CrypterCommandLoader

logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[logging.StreamHandler()])


def prompt_user_password(ctx, param, generate_password):
    '''
    Callback to prompt for username/password based on the generate_password flag value
    '''
    keyName = click.prompt("Please provide KeyName")
    userName = click.prompt("Please provide userName")
    userPassword = None
    if not generate_password:
        userPassword = click.prompt('Please provide UserPassword')
    return (keyName, userName, userPassword)


@click.group()
def add():
    '''
    Add a new username/password tagged with the given key.
    '''
    pass

@add.command()
@click.option("--generate-password", required=False, default=True, show_default=True, callback=prompt_user_password)
@click.option("--keyName", required=False, help="A keyname to tag username/password record")
@click.option("--username", required=False, help="user name")
@click.option("--userPassword", hide_input=True, help="user password")
def key(keyname, username, userpassword, generate_password):
    '''
    Provide a keyname to tag your username/password.
    '''
    try:
        keyname, username, userpassword = generate_password
        response = CrypterMain.add_key(keyname, username, userpassword)
        click.echo("A new record has been added with the following details,")
        click.echo(json.dumps(response, indent=4))
    except Exception as ex:
        click.echo(ex)


@click.group()
def get():
    '''
    Fetch the username/password tagged with the given key if any.
    '''
    pass

@get.command()
@click.option("--keyname", required=True, prompt=True)
def key(keyname):
    '''
    Provide a keyname to get your stored username/password if any.
    '''
    try:
        keyNames = [keyName.strip() for keyName in keyname.split(",")]
        response = CrypterMain.get_key(keyNames=keyNames)
        click.echo("Following record(s) have been found with the given key(s),")
        click.echo(json.dumps(response, indent=4))
    except Exception as ex:
        click.echo(ex)


@click.group()
def delete():
    '''
    Delete the username/password tagged with the given key if any.
    '''
    pass

@delete.command()
@click.option("--keyname", required=True, prompt=True)
def key(keyname):
    '''
    Provide a keyname to delete your stored username/password if any.
    '''
    try:
        keyNames = [keyName.strip() for keyName in keyname.split(",")]
        response = CrypterMain.delete_key(keyNames=keyNames)
        click.echo("Following record(s) have been deleted with the given key(s),")
        click.echo(json.dumps(response, indent=4))
    except Exception as ex:
        click.echo(ex)


@click.group()
def cloud():
    '''
    Option to configure cloud account to backup your secrets.
    '''
    pass

@cloud.command()
def configure():
    '''
    '''
    click.echo("Configure Cloud")

@cloud.command()
def sync():
    '''
    '''
    click.echo("Sync Cloud")


@click.command()
def list():
    '''
    List all the stored username/passwords.
    '''
    try:
        response = CrypterMain.get_key()
        click.echo("Following are the available record(s) in the system")
        click.echo(json.dumps(response, indent=2))
    except Exception as ex:
        raise ex

@click.command()
def init():
    '''
    Perform the inital setup required to save your secrets.
    '''
    try:
        response = CrypterMain.init()
        click.echo("Setup is done")
    except Exception as ex:
        click.echo(ex)


@click.group(
    cls=CrypterCommandLoader,
    lazy_subcommands={
        "add": "crypter.add",
        "get": "crypter.get",
        "delete": "crypter.delete",
        "list": "crypter.list",
        "cloud": "crypter.cloud",
        "init": "crypter.init"
    },
    help='''
    Crypter - A command line utility to generate random passwords
    for the given username & key. It generates random passwords on
    the fly using pre-defined encryption algorithm and store locally
    to access them later. It saves you from not storing your
    username/passwords on the third party storage and being hacked
    at the end. It allows to be your own master where your secrets are
    completely secret to you.
    '''
)
def cli():
    pass


cli()