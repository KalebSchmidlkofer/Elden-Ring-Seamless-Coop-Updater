import zipfile
import json
import requests

inipassword = ''
EldenRingPath = '/home/kaleb/coding/python/autoupdate/eldenRing/game'
filename = f'eldenring.zip'
git_repo = 'https://api.github.com/repos/LukeYui/EldenRingSeamlessCoopRelease/releases/latest'
url = git_repo

def extract(filename, path):
  '''Extract a zip file with zipfilename and path'''
  with zipfile.ZipFile(f'{path}/{filename}', 'r') as zip:
    zip.extractall(path)

def cooppassword(password, path):
  '''Opens seamlesscoopsettings.ini file and changes coop password'''
  with open(f'{path}/SeamlessCoop/seamlesscoopsettings.ini', 'r+') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('cooppassword'):
            lines[i] = f'cooppassword = {password}\n'
    f.seek(0)
    f.writelines(lines)
    f.truncate()


response=requests.get(git_repo)
print(response)
if response.status_code == 200:
  # data=json.loads(response.text)  
  data = response.json()
  # print(data)
  url = data['assets'][0]['browser_download_url']
  print(url)
  response = requests.get(url)
  with open(f'{EldenRingPath}/{filename}', 'wb') as f:
    f.write(response.content)
else:
  print(git_repo)

extract(filename, EldenRingPath)
cooppassword(inipassword, EldenRingPath)
