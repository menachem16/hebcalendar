import requests
import json
from bs4 import BeautifulSoup

# הגדרת cookies ו-Headers
cookies = {
    '_ga': 'GA1.1.883357810.1733346859',
    '_gcl_au': '1.1.950480939.1733346859',
    '_ga_2MNHNZHPSS': 'GS1.1.1733346859.1.0.1733346859.0.0.0',
    '_hjSessionUser_397155': 'eyJpZCI6IjZmZmY2NTE1LTdhMDMtNWVjMC04YmI2LWI3YWMxNGMyOTYyZCIsImNyZWF0ZWQiOjE3MzMzNDY4NjE2MDcsImV4aXN0aW5nIjpmYWxzZX0=',
    '_hjSession_397155': 'eyJpZCI6IjZlNDlmN2M0LTk3YjItNGQ1YS1iNGRmLTJlZjlkZjIxYTRmYyIsImMiOjE3MzMzNDY4NjE2MDcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# יצירת session
session = requests.Session()

# פונקציה שמחלצת JSON מתוך תוכן JSON.parse
def extract_json_from_script(script_content):
    start_index = script_content.find("JSON.parse('") + len("JSON.parse('")
    end_index = script_content.rfind("');")
    json_data = script_content[start_index:end_index]
    
    # מעקב אחר הערך של json_data
    print("json_data לפני המרה ל-JSON:", json_data[:100])  # הדפסת 100 התווים הראשונים
    
    json_data = json_data.replace("\\'", "'").replace('\\"', '"')  # טיפול בתווים מיוחדים
    return json.loads(json_data)

# שליחת בקשה ל-URL
response = session.get('https://www.yeshiva.org.il/calendar', cookies=cookies, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # חיפוש סקריפטים המכילים JSON
    script_tags = soup.find_all("script")
    
    extracted_json = None
    for script in script_tags:
        if "JSON.parse(" in script.text:
            print("נמצא סקריפט מתאים!")
            try:
                extracted_json = extract_json_from_script(script.text)
                break
            except json.JSONDecodeError as e:
                print("שגיאה בהמרה ל-JSON:", e)
                print("תוכן ה-json_data שגרם לשגיאה:", script.text)
    
    if extracted_json:
        # שמירת התוצאה לקובץ JSON
        with open("calendar_data.json", "w", encoding="utf-8") as json_file:
            json.dump(extracted_json, json_file, ensure_ascii=False, indent=4)
        print("המידע נשמר בהצלחה בקובץ calendar_data.json!")
    else:
        print("לא נמצא מידע מתאים ל-JSON.parse.")
else:
    print(f"שגיאה בבקשה: סטטוס {response.status_code}")
