import os
import yaml

env = os.environ.get("P2CI_ENV")

if env == None:
    env = ""
else:
    env = "." + env
f = open("./config" + env + ".yml")
data = yaml.load(f)
f.close()


def GetConfig():
    return data
