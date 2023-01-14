import discord
import os
import requests
import json
import string
import random
from discord import app_commands

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=int("BURAYA SUNUCU IDSİNİ GİR")))
    print("Giriş Başarılı.")

headers = {
    "accept-encoding": "gzip",
    "content-length": "",
    "content-type": "application/json; charset=utf-8",
    "host": "eokulapp.meb.gov.tr",
    "user-agent": "Dart/2.17 (dart:io)"
    }

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def cihazkayit(uid: str):
  url0 = "https://eokulapp.meb.gov.tr/CihazKayit"
  
  json0 = {
      "sifre": "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w",
      "uid": f"{uid}",
      "p": "2.0.12",
      "pid": ""
      }
  
  sonuc = requests.post(url=url0, headers=headers, json=json0)
  
  json_data = json.loads(sonuc.text)
  gid = ""
  for i in json_data['GID']:
    gid += i
  return gid

async def eokulmetod(interaction: discord.Integration, tcno:str, uid:str, gid:str):
    url1 = "https://eokulapp.meb.gov.tr/OgrenciGiris"

    json1 = {
    "sifre": "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w",
    "uid": f"{uid}",
    "gid": f"{gid}",
    "tckn": f"{tcno}",
    "mobile_platform": ""
    }

    sonuc = requests.post(url=url1, headers=headers, json=json1)
    json_data = json.loads(sonuc.text)
    token = ""
    for i in json_data['OgrenciToken']:
      token += i

    url2 = "https://eokulapp.meb.gov.tr/NotBilgileri"

    headers2 = {
    "accept-encoding": "gzip",
    "authorization": "Bareer"+f" {token}",
    "content-length": "",
    "content-type": "application/json; charset=utf-8",
    "host": "eokulapp.meb.gov.tr",
    "user-agent": "Dart/2.17 (dart:io)"
    }

    json2 = {
    "sifre": "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w",
    "uid": f"{uid}",
    "gid": f"{gid}",
    }

    sonuc = requests.post(url=url2, headers=headers2, json=json2)
    json_data = json.loads(sonuc.text)
    
    try:
      i = 0
      global liste
      global toplampuan
      global derssaati
      toplampuan = 0
      liste = []
      derssaati = 0

      while True:
       jsonveri = json_data["notListesi"][i]
       liste.append(f"{jsonveri['Ders']}\n")

       a = 1
       x = 1
       while a < 7:
        asd = f"Y{str(a)}"
        if jsonveri[asd] != "":
         liste.append(f"Sınav {a}: {jsonveri[asd]}\n")
         x = x + 1
        a = a + 1

       a = 1
       x = 1
       while a < 7:
        asd = f"SZL{str(a)}"
        if jsonveri[asd] != "":
         liste.append(f"Sözlü {x}: {jsonveri[asd]}\n")
         x = x + 1
        a = a + 1

       liste.append(f"Ders Puanı: {jsonveri['PUANI']}\n\n")
       d=int(jsonveri['DersSaati'])
       p=float(jsonveri['PUANI'])
       derssaati+=d
       toplampuan+=(d*p)
       i = i + 1

    except:
     liste.append(f"DÖNEM ORTALAMASI: {toplampuan/derssaati}")
     open(str(os.path.dirname(os.path.abspath(__file__)))+r"\notlar.txt", 'w', encoding="utf-8").writelines(liste)
     await interaction.followup.send(file=discord.File(str(os.path.dirname(os.path.abspath(__file__)))+r"\notlar.txt"), content="Notların")

@tree.command(guild=discord.Object(id=int("BURAYA SUNUCU IDSİNİ GİR")), name='eokulnoteskikimlik', description='TC, Okul No, Aile Sıra No ve Cilt No girerek e-okul notlarına bak')
async def eokulnot(interaction: discord.Interaction, tcno: str, okulno:str, ailesirano: str, ciltno: str):
    await interaction.response.defer(ephemeral=True)
    uid = get_random_string(15)
    gid = cihazkayit(uid)
    url = "https://eokulapp.meb.gov.tr/OgrenciEkle"

    json2 = {
    "sifre": "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w",
    "uid": f"{uid}",
    "gid": f"{gid}",
    "tckn": f"{tcno}",
    "okulNo": f"{okulno}",
    "aileSiraNo": f"{ailesirano}",
    "ciltNo": f"{ciltno}",
    "seriNo": "",
    "kimlikTipi": "",
    "ip": "",
    "push_id": ""
    }

    if requests.post(url=url, headers=headers, json=json2).ok==True:
        await eokulmetod(interaction, tcno, uid, gid)
    else:
      await interaction.followup.send("Geçersiz değerler girildi.")    

@tree.command(guild=discord.Object(id=int("BURAYA SUNUCU IDSİNİ GİR")), name='eokulnotyenikimlik', description='TC, Okul No ve Kimlik Seri No girerek e-okul notlarına bak')
async def eokulnot(interaction: discord.Interaction, tcno: str, okulno:str, kimlikserino:str):
    await interaction.response.defer(ephemeral=True)
    uid = get_random_string(15)
    gid = cihazkayit(uid)
    url = "https://eokulapp.meb.gov.tr/OgrenciEkle"

    json2 = {
    "sifre": "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w",
    "uid": f"{uid}",
    "gid": f"{gid}",
    "tckn": f"{tcno}",
    "okulNo": f"{okulno}",
    "aileSiraNo": "",
    "ciltNo": "",
    "seriNo": f"{kimlikserino}",
    "kimlikTipi": "1",
    "ip": "",
    "push_id": ""
    }

    if requests.post(url=url, headers=headers, json=json2).ok==True:
        await eokulmetod(interaction, tcno, uid, gid)
    else:
      await interaction.followup.send("Geçersiz değerler girildi.") 

client.run("TOKEN")