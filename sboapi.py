import json
import requests
import time 
from datetime import datetime
import sqlite3
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError

DROP_BELOW = 0.2
DT = datetime.today().strftime("%b%d")

def get_live_matches():
  #print("Scanning for live matches......")
  #print("")
  url = "https://api.betting-api.com/sbobet/football/live/all"

  payload = {}
  headers = {
    'Authorization': 'Bearer ca22c699a88647b6ba514247c2db79752eda9852ddcd449397075572fc195088'
  }

  r = requests.request("GET", url, headers=headers, data = payload)
  matches = r.json()
  
  return matches

def fhh(i):
  #First half hdp
  
  try:
    fhh1_type1 = i['markets']['half']['1']['handicaps1'][0]['type']
    fhh1t1_odds = i['markets']['half']['1']['handicaps1'][0]['value']
  except:
    fhh1_type1 = 'NULL'
    fhh1t1_odds = 'NULL'
    #print("Value Error in FH HDP1 type1")

  try:
    fhh1_type2 = i['markets']['half']['1']['handicaps1'][1]['type']
    fhh1t2_odds = i['markets']['half']['1']['handicaps1'][1]['value']
  except:
    fhh1_type2 = 'NULL'
    fhh1t2_odds = 'NULL'
    #print("Value Error in FH HDP1 type2")

  try:
    fhh2_type1 = i['markets']['half']['1']['handicaps2'][0]['type']
    fhh2t1_odds = i['markets']['half']['1']['handicaps2'][0]['value']
  except:
    fhh2_type1 = 'NULL'
    fhh2t1_odds = 'NULL'
    #print("Value Error in FH HDP2 type1")
  
  try:
    fhh2_type2 = i['markets']['half']['1']['handicaps2'][1]['type']
    fhh2t2_odds = i['markets']['half']['1']['handicaps2'][1]['value']
  except:
    fhh2_type2 = 'NULL'
    fhh2t2_odds = 'NULL'
    #print("Value Error in FH HDP2 type2")
  
  return [fhh1_type1, fhh1t1_odds, fhh1_type2, fhh1t2_odds, fhh2_type1, fhh2t1_odds, fhh2_type2, fhh2t2_odds]

def fho(i):
  #First half over
  #fho = min(i['markets']['half']['1']['totals'], key=lambda lt: lt['type'])
  try:
    fho_type1 = i['markets']['half']['1']['totals'][0]['type']
    fhot1_odds = i['markets']['half']['1']['totals'][0]['over']
  except:
    fho_type1 = 'NULL'
    fhot1_odds = 'NULL'
    #print("Value Error in FH over type1")

  try:
    fho_type2 = i['markets']['half']['1']['totals'][1]['type']
    fhot2_odds = i['markets']['half']['1']['totals'][1]['over']
  except:
    fho_type2 = 'NULL'
    fhot2_odds = 'NULL'
    #print("Value Error in FH over type2")

  return [fho_type1, fhot1_odds, fho_type2, fhot2_odds]

def fth(i):
  try:
    fth1_type1 = i['markets']['handicaps1'][0]['type']
    fth1t1_odds = i['markets']['handicaps1'][0]['value']
  except:
    fth1_type1 = 'NULL'
    fth1t1_odds = 'NULL'
  
  try:
    fth1_type2 = i['markets']['handicaps1'][1]['type']
    fth1t2_odds = i['markets']['handicaps1'][1]['value']
  except:
    fth1_type2 = 'NULL'
    fth1t2_odds = 'NULL'
  
  try:
    fth2_type1 = i['markets']['handicaps2'][0]['type']
    fth2t1_odds = i['markets']['handicaps2'][0]['value']
  except:
    fth2_type1 = 'NULL'
    fth2t1_odds = 'NULL'
  
  try:
    fth2_type2 = i['markets']['handicaps2'][1]['type']
    fth2t2_odds = i['markets']['handicaps2'][1]['value']
  except:
    fth2_type2 = 'NULL'
    fth2t2_odds = 'NULL'
  

  return [fth1_type1, fth1t1_odds, fth1_type2, fth1t2_odds, fth2_type1, fth2t1_odds, fth2_type2, fth2t2_odds]

def fto(i):
  try:
    fto_type1 = i['markets']['totals'][0]['type']
    fto1_odds = i['markets']['totals'][0]['over']
  except:
    fto_type1 = 'NULL'
    fto1_odds = 'NULL'

  try:
    fto_type2 = i['markets']['totals'][1]['type']
    fto2_odds = i['markets']['totals'][1]['over']
  except:
    fto_type2 = 'NULL'
    fto2_odds = 'NULL'


  return [fto_type1, fto1_odds, fto_type2, fto2_odds]


def check_sbo():
  matches = get_live_matches()
  
  lb(str(datetime.now().strftime("%H:%M:%S")) + " There are currently " + str(len(matches)) + " LIVE matches: ")
  
  
  for i in matches:
    now = datetime.now().strftime("%H:%M:%S")
    try:
      lb("SBO-{}, [{}]:   {} [{}:{}] {}".format(i['id'], i['tournament']['name'], i['team1'], i['score1'], i['score2'], i['team2']))
      lb(" ")
  
      if i['half_index'] == 0:
        lb("Date: {} Time: {} | First Half: {}mins | Half Index: {}".format(DT, str(now),str(i['minute']), i['half_index']))
      
        fhhdp = fhh(i)
        fhover = fho(i)
        
        #FT Hdp
        fthdp = fth(i)
        #FT Over
        ftover = fto(i)
        o = {'Time' : now, 'Team1' : i['team1'], 'Team2' : i['team2'], 'Mins' : str(i['minute']), 'Score' : "{}:{}".format(i['score1'], i['score2']), 'fhh1_type1' : fhhdp[0], 'fhh1t1_odds' : fhhdp[1], 'fhh1_type2' : fhhdp[2], 'fhh1t2_odds' : fhhdp[3], 'fhh2_type1' : fhhdp[4], 'fhh2t1_odds' : fhhdp[5], 'fhh2_type2' : fhhdp[6], 'fhh2t2_odds' : fhhdp[7], 'fho_type1' : fhover[0], 'fhot1_odds' : fhover[1], 'fho_type2' : fhover[2], 'fhot2_odds' : fhover[3], "fth1_type1" : fthdp[0], "fth1t1_odds" : fthdp[1], "fth1_type2" : fthdp[2], "fth1t2_odds" : fthdp[3], "fth2_type1" : fthdp[4], "fth2t1_odds" : fthdp[5], "fth2_type2" : fthdp[6], "fth2t2_odds" : fthdp[7], "fto_type1" : ftover[0], "fto1_odds" : ftover[1], "fto_type2" : ftover[2], "fto2_odds" : ftover[3] }
        
        try:
          getLastRow(o, "SBO" + str(i['id']), i['tournament']['name'])
        except:
          pass
        db(o, "SBO" + str(i['id']))
          
       

      #first half
      elif i['half_index'] == 1:
        
        lb("Date: {} Time: {} | First Half: {}mins | Half Index: {}".format(DT, str(now),str(i['minute']), i['half_index']))
        
        
        fhhdp = fhh(i)
        fhover = fho(i)
        
        #FT Hdp
        fthdp = fth(i)
        #FT Over
        ftover = fto(i)
        o = {'Time' : now, 'Team1' : i['team1'], 'Team2' : i['team2'], 'Mins' : str(i['minute']), 'Score' : "{}:{}".format(i['score1'], i['score2']), 'fhh1_type1' : fhhdp[0], 'fhh1t1_odds' : fhhdp[1], 'fhh1_type2' : fhhdp[2], 'fhh1t2_odds' : fhhdp[3], 'fhh2_type1' : fhhdp[4], 'fhh2t1_odds' : fhhdp[5], 'fhh2_type2' : fhhdp[6], 'fhh2t2_odds' : fhhdp[7], 'fho_type1' : fhover[0], 'fhot1_odds' : fhover[1], 'fho_type2' : fhover[2], 'fhot2_odds' : fhover[3], "fth1_type1" : fthdp[0], "fth1t1_odds" : fthdp[1], "fth1_type2" : fthdp[2], "fth1t2_odds" : fthdp[3], "fth2_type1" : fthdp[4], "fth2t1_odds" : fthdp[5], "fth2_type2" : fthdp[6], "fth2t2_odds" : fthdp[7], "fto_type1" : ftover[0], "fto1_odds" : ftover[1], "fto_type2" : ftover[2], "fto2_odds" : ftover[3] }
        

        try:
          getLastRow(o, "SBO" + str(i['id']), i['tournament']['name'])
        except:
          pass
        db(o, "SBO" + str(i['id']))
          
          
      #2nd half
      elif i['half_index'] == 2:
        lb("Date: {} Time: {} | 2nd Half: {}mins | Half Index: {}".format(DT, str(now),str(i['minute'] + 45), i['half_index']))
        fhhdp = fhh(i)
        fhover = fho(i)
        #FT Hdp
        fthdp = fth(i)
        #FT Over
        ftover = fto(i)
        o = {'Time' : now, 'Team1' : i['team1'], 'Team2' : i['team2'], 'Mins' : str(i['minute'] + 45), 'Score' : "{}:{}".format(i['score1'], i['score2']), 'fhh1_type1' : fhhdp[0], 'fhh1t1_odds' : fhhdp[1], 'fhh1_type2' : fhhdp[2], 'fhh1t2_odds' : fhhdp[3], 'fhh2_type1' : fhhdp[4], 'fhh2t1_odds' : fhhdp[5], 'fhh2_type2' : fhhdp[6], 'fhh2t2_odds' : fhhdp[7], 'fho_type1' : fhover[0], 'fhot1_odds' : fhover[1], 'fho_type2' : fhover[2], 'fhot2_odds' : fhover[3], "fth1_type1" : fthdp[0], "fth1t1_odds" : fthdp[1], "fth1_type2" : fthdp[2], "fth1t2_odds" : fthdp[3], "fth2_type1" : fthdp[4], "fth2t1_odds" : fthdp[5], "fth2_type2" : fthdp[6], "fth2t2_odds" : fthdp[7], "fto_type1" : ftover[0], "fto1_odds" : ftover[1], "fto_type2" : ftover[2], "fto2_odds" : ftover[3] }
        
        
        try:
          getLastRow(o, "SBO" + str(i['id']), i['tournament']['name'])
        except:
          pass
        db(o, "SBO" + str(i['id']))
        

      #half time
      elif i['half_index'] == 5:
        
        lb("Date: {} Time: {} | HT | Half Index: {}".format(DT, str(now), i['half_index']))
        fhhdp = fhh(i)
        fhover = fho(i)
        #FT Hdp
        fthdp = fth(i)
        #FT Over
        ftover = fto(i)
        o = {'Time' : now, 'Team1' : i['team1'], 'Team2' : i['team2'], 'Mins' : str(i['minute']), 'Score' : "{}:{}".format(i['score1'], i['score2']), 'fhh1_type1' : fhhdp[0], 'fhh1t1_odds' : fhhdp[1], 'fhh1_type2' : fhhdp[2], 'fhh1t2_odds' : fhhdp[3], 'fhh2_type1' : fhhdp[4], 'fhh2t1_odds' : fhhdp[5], 'fhh2_type2' : fhhdp[6], 'fhh2t2_odds' : fhhdp[7], 'fho_type1' : fhover[0], 'fhot1_odds' : fhover[1], 'fho_type2' : fhover[2], 'fhot2_odds' : fhover[3], "fth1_type1" : fthdp[0], "fth1t1_odds" : fthdp[1], "fth1_type2" : fthdp[2], "fth1t2_odds" : fthdp[3], "fth2_type1" : fthdp[4], "fth2t1_odds" : fthdp[5], "fth2_type2" : fthdp[6], "fth2t2_odds" : fthdp[7], "fto_type1" : ftover[0], "fto1_odds" : ftover[1], "fto_type2" : ftover[2], "fto2_odds" : ftover[3] }
      
        try:
          getLastRow(o, "SBO" + str(i['id']), i['tournament']['name'])
        except:
          pass
        db(o, "SBO" + str(i['id']))
          
       
      #other half index except 0,1,2,5
      else: 
        print("{}mins | {}".format(str(i['minute']), i['half_index']))
      
    except ValueError: 
      print("Value Error in general")
    except KeyError:
      print("Key Error in general or no half index")

    # except KeyError:
    #   print("Key Error in general")
    lb("---"*30)

def db(o, match_id):
    
    con = sqlite3.connect(DT + 'odds.db')
    cur = con.cursor() 
    
    sql_cmd = "CREATE TABLE IF NOT EXISTS " + match_id + " (Time, Team1, Team2, Mins, Score, fhh1_type1, fhh1t1_odds, fhh1_type2, fhh1t2_odds, fhh2_type1, fhh2t1_odds, fhh2_type2, fhh2t2_odds, fho_type1, fhot1_odds, fho_type2, fhot2_odds, fth1_type1, fth1t1_odds, fth1_type2, fth1t2_odds, fth2_type1, fth2t1_odds, fth2_type2, fth2t2_odds, fto_type1, fto1_odds, fto_type2, fto2_odds);"
    cur.execute(sql_cmd)
    query = "Insert into " + match_id + " (Time, Team1, Team2, Mins, Score, fhh1_type1, fhh1t1_odds, fhh1_type2, fhh1t2_odds, fhh2_type1, fhh2t1_odds, fhh2_type2, fhh2t2_odds, fho_type1, fhot1_odds, fho_type2, fhot2_odds, fth1_type1, fth1t1_odds, fth1_type2, fth1t2_odds, fth2_type1, fth2t1_odds, fth2_type2, fth2t2_odds, fto_type1, fto1_odds, fto_type2, fto2_odds) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    

    try: 
        # Cursor object 
        cur = con.cursor() 
        # Execute query 
        cur.execute(query, (o['Time'], o['Team1'], o['Team2'], o['Mins'], o['Score'], o['fhh1_type1'], o['fhh1t1_odds'], o['fhh1_type2'], o['fhh1t2_odds'], o['fhh2_type1'], o['fhh2t1_odds'], o['fhh2_type2'], o['fhh2t2_odds'], o['fho_type1'], o['fhot1_odds'], o['fho_type2'], o['fhot2_odds'], o['fth1_type1'], o['fth1t1_odds'], o['fth1_type2'], o['fth1t2_odds'], o['fth2_type1'], o['fth2t1_odds'], o['fth2_type2'], o['fth2t2_odds'], o['fto_type1'], o['fto1_odds'], o['fto_type2'], o['fto2_odds'])) 
        # Commit changes
        con.commit() 
        # Print successful message 
        #print("Match record inserted successfully")
    except: 
        print("Error occurred...") 
        # Roll back if in case of issue
        con.rollback() 

    con.close()

def getLastRow(o, match_id, league):
  #print(o)
  con = sqlite3.connect(DT + 'odds.db')
  cur = con.cursor() 
  sql_cmd = "SELECT * FROM " + match_id + " ORDER BY Time DESC LIMIT 1;"
  cur.execute(sql_cmd)
  result = cur.fetchone()
  #print(result)
  con.close()
  #print(result[4])
  if o['Score'] == result[4]:
    #FH Hdp1 type1 drop
    if o['fhh1_type1'] == result[5] and o['fhh1_type1'] <= 0:
      if o['fhh1t1_odds'] < result[6] and ((result[6] - o['fhh1t1_odds'])/result[6]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - FH Home ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fhh1_type1'], result[6], o['fhh1t1_odds'], o['Mins'])
        tg(msg)

    #FH Hdp1 type2 drop
    if o['fhh1_type2'] == result[7] and o['fhh1_type2'] <= 0:
      if o['fhh1t2_odds'] < result[8] and ((result[8] - o['fhh1t2_odds'])/result[8]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - FH Home ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fhh1_type2'], result[8], o['fhh1t2_odds'], o['Mins'])
        tg(msg)

    #FH Hdp2 type1 drop
    if o['fhh2_type1'] == result[9] and o['fhh2_type1'] <= 0:
      if o['fhh2t1_odds'] < result[10] and ((result[10] - o['fhh2t1_odds'])/result[10]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - FH Away ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fhh2_type1'], result[10], o['fhh2t1_odds'], o['Mins'])
        tg(msg)

    #FH Hdp2 type2 drop
    if o['fhh2_type2'] == result[11] and o['fhh2_type2'] <= 0:
      if o['fhh2t2_odds'] < result[12] and ((result[12] - o['fhh2t2_odds'])/result[12]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - FH Away ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fhh2_type2'], result[12], o['fhh2t2_odds'], o['Mins'])
        tg(msg)

    #FH Total type1 drop
    if o['fho_type1'] == result[13]:
      if o['fhot1_odds'] < result[14] and ((result[14] - o['fhot1_odds'])/result[14]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - FH Total over ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fho_type1'], result[14], o['fhot1_odds'], o['Mins'])
        tg(msg)

    #FH Total type2 drop
    if o['fho_type2'] == result[15]:
      if o['fhot2_odds'] < result[16] and ((result[16] - o['fhot2_odds'])/result[16]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - FH Total over ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fho_type2'], result[16], o['fhot2_odds'], o['Mins'])
        tg(msg)


    #Fulltime Hdp1 type1 drop
    if o['fth1_type1'] == result[17] and o['fth1_type1'] <= 0:
      if o['fth1t1_odds'] < result[18] and ((result[18] - o['fth1t1_odds'])/result[18]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - Fulltime Home ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fth1_type1'], result[18], o['fth1t1_odds'], o['Mins'])
        tg(msg)

    #Fulltime Hdp1 type2 drop
    if o['fth1_type2'] == result[19] and o['fth1_type2'] <= 0:
      if o['fth1t2_odds'] < result[20] and ((result[20] - o['fth1t2_odds'])/result[20]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - Fulltime Home ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fth1_type2'], result[20], o['fth1t2_odds'], o['Mins'])
        tg(msg)

    #Fulltime Hdp2 type1 drop
    if o['fth2_type1'] == result[21] and o['fth2_type1'] <= 0:
      if o['fth2t1_odds'] < result[22] and ((result[22] - o['fth2t1_odds'])/result[22]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - Fulltime Away ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fth2_type1'], result[22], o['fth2t1_odds'], o['Mins'])
        tg(msg)

    #Fulltime Hdp2 type2 drop
    if o['fth2_type2'] == result[23] and o['fth2_type2'] <= 0:
      if o['fth2t2_odds'] < result[24] and ((result[24] - o['fth2t2_odds'])/result[24]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - Fulltime Away ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fth2_type2'], result[24], o['fth2t2_odds'], o['Mins'])
        tg(msg)

    #Fulltime Total type1 drop
    if o['fto_type1'] == result[25]:
      if o['ftot1_odds'] < result[26] and ((result[26] - o['ftot1_odds'])/result[26]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - Fulltime Total over ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fto_type1'], result[26], o['ftot1_odds'], o['Mins'])
        tg(msg)

    #FT Total type2 drop
    if o['fto_type2'] == result[27]:
      
      if o['ftot2_odds'] < result[28] and ((result[28] - o['ftot2_odds'])/result[28]) > DROP_BELOW:
        msg = "SBO - {} - {} [{}] {} - Fulltime Total over ({}) drop from ({} to {}) at {} mins".format(league, o['Team1'], o['Score'], o['Team2'], o['fto_type2'], result[28], o['ftot2_odds'], o['Mins'])
        tg(msg)

  

def tg(msg):
  token = '1132386597:AAFoZ8xPw5rHtZzjX06LlelNzyvT7cUgG7U'
  url = 'https://api.telegram.org/bot' + token + '/sendMessage'
  data = {'chat_id': '-1001293678720', 'text': msg + " from Azure"}
  requests.post(url, data).json()

def lb(msg):
  token = '1132386597:AAFoZ8xPw5rHtZzjX06LlelNzyvT7cUgG7U'
  url = 'https://api.telegram.org/bot' + token + '/sendMessage'
  data = {'chat_id': '1206315369', 'text': msg}
  requests.post(url, data).json()

while True:
    #lb(str(datetime.now().strftime("%H:%M:%S")))
    DT = datetime.today().strftime("%b%d")
    try:
      check_sbo()
    except (OSError, ConnectionError, RemoteDisconnected, ProtocolError) as e:
      m = str(datetime.now().strftime("%H:%M:%S")) + ": " + str(e) + " Error occured -"
      tg(str(m))
      
    time.sleep(30)      
    
