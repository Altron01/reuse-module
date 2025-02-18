import pathlib
import re
import os
#pip install azure-keyvault-secrets azure-identity
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

destination_root = r"./factoryData"
pattern = "**/*.json"

def readFile(fileName):
  file = open(fileName, "r")
  txt = file.read()
  file.close()
  return txt
pass

VAULT_URL = os.environ["VAULT_URL"]
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

master_list = list(pathlib.Path(destination_root).glob(pattern))
for file in master_list:
  txt = readFile(str(file.absolute()))
  match_list = re.findall(r'@{([a-z|A-Z|\\(|\\)|\\.|_]*)}', txt)
  if len(match_list) == 0:
    continue

  for match in match_list:
    print("Replacing secret: " + match)
    txt = txt.replace("@{" + match + "}", client.get_secret(match.split(".")[1]).value)

  f = open(str(file.absolute()), "w")
  f.seek(0)
  f.truncate()
  f.write(txt)
  f.close()
