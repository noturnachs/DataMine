import requests
from bs4 import BeautifulSoup
import csv
import os
import re


def create_csv_file(domain, data_list):
    csv_file = f"{domain}_MembersData.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Name", "Email"])

        for data in data_list:
            writer.writerow([data["Name"], data["Email"]])

    print(f"Data has been saved to '{csv_file}'.")


def getEmail(response2, name):
    try:
        soup2 = BeautifulSoup(response2, "html.parser")
        div_tags = soup2.find_all(
            "div",
            class_="field field--name-field-email field--type-email field--label-above field__items",
        )

        for div_tag in div_tags:
            email_div = div_tag.find("div", class_="field__item")
            if email_div:
                email_a_tag = email_div.find("a", href=True)
                if email_a_tag and email_a_tag["href"].startswith("mailto:"):
                    email_address = email_a_tag["href"][7:]
                    data_list.append({"Name": name, "Email": email_address})
    except:
        email_address = "No Email Found"

    return email_address


website_url = "https://www.priceedwards.com/professionals"
match = re.search(r"www\.(.*?)\.com", website_url)

if match:
    domain = match.group(1)
    print("Domain:", domain)
    print("\n")
else:
    print("Pattern not found in the URL.")

response = requests.get(website_url)

data_list = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    span_tags = soup.find_all("span", class_="field-content")
    counter = 0
    for span_tag in span_tags:
        a_tag = span_tag.find("a")
        if a_tag:
            name = a_tag.get_text()
            href = a_tag.get("href")

            emailParsing = "https://www.priceedwards.com" + href
            response2 = requests.get(emailParsing)

            if response2.status_code == 200:
                email_address = getEmail(response2.text, name)

            else:
                print(f"Failed to retrieve email for {name}")

            print("Name:", name)
            print("Email:", email_address)
            counter = counter + 1
            print("\n")

else:
    print("Failed to retrieve the web page.")

TotalNumberofAgents = counter
print("Number of Agents:", TotalNumberofAgents)

create_csv_file(domain, data_list)
