#!/usr/bin/env python3

import re
import base64

import click
import sh
from sh import git
from dotenv import dotenv_values

def get_dokku():
  remote = git.remote("get-url", "dokku").strip()
  m = re.match(r"(?P<user>.*)@(?P<host>.*):(?P<app>.*)", remote)
  return m.groups()

@click.command()
@click.argument("envfile", type=click.Path(file_okay=True, dir_okay=False, exists=True))
def main(envfile):
  user, host, app = get_dokku()

  dokku = sh.Command("ssh").bake("-tt", f"{user}@{host}")

  with open(envfile, "r") as fh:
    env = dotenv_values(envfile)
  
  for key, value in env.items():
    print(key)
    value_b64 = base64.b64encode(value.encode("utf8")).decode("utf8")
    # print(value_b64)

    dokku("config:set", "--encoded", "--no-restart", app, f"{key}={value_b64}")
  

if "__main__" == __name__:
  main()
