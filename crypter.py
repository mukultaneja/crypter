import os
import json
import click
import logging
from crypter_main import CrypterMain
from crypter_lazy_load import CrypterCommandGroup

logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[logging.StreamHandler()])


@click.group()
def add():
    '''
    Add a new username/password tagged with the given key.
    '''
    pass

@add.command()
@click.option("--keyname", required=True)
@click.option("--username", required=True)
@click.option("--userpassword", hide_input=True, default='112')
@click.option("--autogenerate", required=False, default=True, show_default=True)
def key(keyname, username, userpassword, autogenerate):
    '''
    Provide a keyname to tag your username/password.
    '''
    response = CrypterMain.add_key(keyname, username, userpassword)
    click.echo("A record with the following information has been added succesfully")
    click.echo(response)


@click.group()
def get():
    '''
    Fetch the username/password tagged with the given key if any.
    '''
    pass

@get.command()
@click.option("--keyname", required=True)
def key(keyname):
    '''
    Provide a keyname to get your stored username/password if any.
    '''
    response = CrypterMain.get_key(keyname)
    click.echo(response)


@click.group()
def delete():
    '''
    Delete the username/password tagged with the given key if any.
    '''
    pass

@delete.command()
@click.option("--keyname", required=True)
def key(keyname):
    '''
    Provide a keyname to delete your stored username/password if any.
    '''
    click.echo(f"No key with name {keyname} is found")


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
    if os.path.exists("data.json"):
        with open("data.json") as data:
            try:
                res = json.load(data)
                click.echo(res)
            except json.JSONDecodeError:
                click.echo(f"No keys found")
            finally:
                return
    click.echo(f"No keys found")


@click.command()
def init():
    '''
    Perform the inital setup required to save your secrets.
    '''
    try:
        CrypterMain.init()
        click.echo("Setup is done")
    except Exception as ex:
        print(ex)


@click.group(
    cls=CrypterCommandGroup,
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
