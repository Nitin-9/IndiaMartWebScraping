from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import csv
import time

app = Flask(__name__)
@app.route('/', methods = ['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")
@app.route('/review', methods = ['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://dir.indiamart.com/search.mp?ss=" + searchString
            options = ChromeOptions()
            options.headless =True
            jsp_scraper = Chrome(executable_path= r'C:\Users\Griffin Industries\PycharmProjects\IndiaMart-Scraper\chromedriver-win64\chromedriver.exe', options=options)
            jsp_scraper.get(flipkart_url)
            time.sleep(5)
            html = jsp_scraper.page_source
            soup = BeautifulSoup(html, "html.parser")
            #company = soup.findAll("div",{"class":"prd-bottom imgc fww flx100 ase rdhvr compnamegdv"})
            #company = soup.findAll("div", {"class": "flx1 df fww lst-cell mw-clc308 commnclas gdV mw500"})
            company = soup.findAll("section", {"class": "lst_cl prd-card fww brs5 pr bg1 prd-card-mtpl"})


            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Adderess, Phone_Indiamart \n"
            fw.write(headers)

            reviews = []
            for cname in company:
                try:
                    companyName = (cname.find("div", {"class": "prd-bottom imgc fww flx100 ase rdhvr compnamegdv"})).h4.a.span.text
                except:
                    companyName = 'No Name'

                try:
                    adderess = cname.find("p",{"class":"tac wpw"}).text
                except:
                    adderess = 'No Address'

                try:
                    phone_imart = cname.find("span",{"class":"pns_h duet fwb"}).text
                except:
                    phone_imart = 'No Number'

                mydict = {"Product": searchString, "Name": companyName, "Adderess":adderess,
                          "Phone_Indiamart":phone_imart}
                reviews.append(mydict)

            keys = reviews[0].keys()
            with open(filename, 'w', encoding='utf-8') as output_file:

                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(reviews)
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        finally:
            jsp_scraper.quit()

    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=8001, debug=True)
    # app.run(debug=True)


