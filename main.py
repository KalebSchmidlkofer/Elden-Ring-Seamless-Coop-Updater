#!C:\Users\joshl\Downloads\Auto-Updater-Elden_ring\.venv\Scripts\python
import zipfile
import json
import requests
import yaml
import os
from time import sleep
with open('config.yaml') as f:
    config = yaml.safe_load(f)
inipassword = config['VARIABLES']['inipassword']
EldenRingPath = config['VARIABLES']['EldenRingPath']

clear = lambda: os.system('cls')
filename = f'eldenring-Seamless-coop.zip'
git_repo = 'https://api.github.com/repos/LukeYui/EldenRingSeamlessCoopRelease/releases/latest'
versionpath = f'{EldenRingPath}/SeamlessCoop/version.txt'

url = git_repo

def request_grab(download):
  '''Request the json data from github's api'''
  response=requests.get(git_repo)
  # print(response)
  clear()

  if response.status_code == 200:
    
    # data=json.loads(response.text)  
    data = response.json()
    # print(data)
    url = data['assets'][0]['browser_download_url']
    # print(url)
    global version
    version = data['name']
    # print(version)
    if download:
      print(f'Path: {EldenRingPath}')
      print(f'Password: {inipassword}')
      print(f'\nDownloading Zip file as {filename}')
      response = requests.get(url)
      with open(f'{EldenRingPath}/{filename}', 'wb') as f:
        f.write(response.content)
      extract(filename, EldenRingPath)
      cooppassword(inipassword, EldenRingPath)
      if not os.path.exists(versionpath):
        with open(versionpath, 'w') as f:
          f.write(version)
      else:
        with open(versionpath, 'w') as f:
          f.close()

        with open(versionpath, 'a') as f:
          f.write(version)
          
  else:
    raise Exception(f'Unable to find {git_repo}')

def extract(filename, path):
  '''Extract a zip file with zipfilename and path'''
  with zipfile.ZipFile(f'{path}/{filename}', 'r') as zip:
    print(f'Extracting zip file in {path}')
    zip.extractall(path)

def cooppassword(password, path):
  '''Opens seamlesscoopsettings.ini file and changes coop password'''
  with open(f'{path}/SeamlessCoop/seamlesscoopsettings.ini', 'r+') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('cooppassword'):
            lines[i] = f'cooppassword = {password}\n'
    print(f'Setting cooppassword = {password}')
    f.seek(0)
    f.writelines(lines)
    f.truncate()

def current_version(path):
  '''Current Version of seamless coop mod On Your Local System'''
  if os.path.exists(path):
    with open(path, 'r') as f:
      lines = f.readline()
    print(f'Current Version: {lines}')
  else:
    raise FileExistsError(f'{path} Does not exist, Creating')
def latest_version():
  '''Fetches latest version of Seamless coop mod from github's api'''
  print(f'Downloading Version: {version}')

request_grab(download=True)
current_version(versionpath)
latest_version()
sleep(4)
