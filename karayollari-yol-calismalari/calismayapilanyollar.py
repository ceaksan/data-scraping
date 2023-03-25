import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def get_works(direction):
    url = f"https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/CalismaYapilanYollarYeni.aspx?Bolge={direction}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table", {"class": "table"})
    rows = soup.find_all('tr', class_='trCalismaYapilanYollarDatas')[1:]
    works = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 4:
            identifier = cols[0].text.strip()
            name = cols[1].text.strip()
            notification_date = cols[2].text.strip()
            update_date = cols[3].text.strip()
            issues = get_issue(name)
            works.append(
                {
                    "identifier": identifier,
                    "name": name,
                    "notification_date": notification_date,
                    "update_date": update_date,
                    "issues": issues,
                }
            )
    return works


def get_issue(work_name):
    stopwords = ["çalışması", "çalışmaları"]
    keywords_to_issue = {
        "üstgeçit": "Üstgeçit",
        "köprü yapım": "Köprü yapım",
        "tramvay": "Tramvay hattı yapım",
        "bağlantı yolu": "Bağlantı yolu",
        "yaya üst geçidi": "Yaya üst geçidi yapım",
        "demiryolu köprüsü": "Demiryolu köprüsü yapım",
        "heyelan": "Heyelan",
        "trafik kapalı": "Trafik kapatılarak çalışma yapılması",
        "katılım kolu bağlantı": "Katılım kolu bağlantı",
        "genleşme derzi onarım": "Genleşme derzi onarım",
        "derz yenileme": "Derz yenileme",
        "üstyapı yenileme": "Üstyapı yenileme",
        "üstyapı yenileme": "Üstyapı yenileme",
        "yol yapım": "Yol yapım ve onarım",
        "yol onarım": "Yol yapım ve onarım",
        # Add more keywords and issues as needed
    }
    for keyword, issue in keywords_to_issue.items():
        if keyword in work_name.lower():
            if isinstance(issue, list):
                return [i for i in issue if i not in stopwords]  # Return the list of issues
            else:
                return [issue] if issue not in stopwords else [] # Return the single issue as a list
    return ["Diğer"]  # Default issue if none of the keywords match


works = get_works(1)

# Convert works list to a pandas DataFrame
df = pd.DataFrame(works)

# Bar chart of issue types
issue_counts = df["issues"].value_counts()
issue_counts.plot(kind="bar", title="Issue Types")

# Pie chart of work notification dates
notification_dates = [work['notification_date'] for work in works]
unique_notification_dates = set(notification_dates)
notification_date_counts = [notification_dates.count(date) for date in unique_notification_dates]

plt.figure(figsize=(8, 6))
plt.pie(notification_date_counts, labels=unique_notification_dates, autopct='%1.1f%%')
plt.title("Yapım Çalışmalarının Bildirim Tarihleri")
plt.show()

# Bar chart of work update dates
update_dates = [datetime.strptime(work['update_date'], '%d.%m.%Y') for work in works if work['update_date']]
unique_update_dates = sorted(set(update_dates))
update_date_counts = [update_dates.count(date) for date in unique_update_dates]

plt.figure(figsize=(12, 6))
plt.bar(unique_update_dates, update_date_counts, color='green', width=1)
plt.title("Yapım Çalışmalarının Güncelleme Tarihleri")
plt.xlabel("Tarih")
plt.ylabel("Sayı")
plt.show()

# Bar chart of issue types
issues = [issue for work in works for issue in work['issues']]
unique_issues = list(set(issues))
issue_counts = [issues.count(issue) for issue in unique_issues]

plt.figure(figsize=(12, 6))
plt.bar(unique_issues, issue_counts, color='orange')
plt.title("Çalışma Türlerine Göre Çalışma Sayıları")
plt.xlabel("Çalışma Türleri")
plt.ylabel("Sayı")
plt.show()
