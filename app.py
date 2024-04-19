from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from flask import *
from flask import render_template

def get_news_from_indianexpress(page, category):
	bro= webdriver.Chrome()
	bro.get(f"https://indianexpress.com/section/{category}/page/{page}/")
	news_title=[]
	news_decription=[]
	sleep(2)
	elem = bro.find_elements(By.CLASS_NAME,value="title")
	elem2 = bro.find_elements(By.TAG_NAME, "p")
	for x in elem:
		news_title.append(x.get_attribute("textContent"))
	for y in elem2:
		news_decription.append(y.get_attribute("textContent"))
	news_decription = [i for i in news_decription if i != ""]
	news=[]
	for x in range(0, len(news_title)):
		news.append([news_title[x], news_decription[x]])
	return news

app = Flask(__name__, template_folder="temp", static_folder="static")

@app.route("/")
def home():
	news = get_news_from_indianexpress(1,"cities")
	return render_template("index.html", news=news,n=1, category="cities", title="News Headlines",pp="", np="2")

@app.route("/section/<sec>/page/<n>")
def page(sec,n):
	try:
		news = get_news_from_indianexpress(int(n),sec)
		return render_template("index.html", news=news,n=n, category=sec, title=sec, np =(int(n)+1), pp =(int(n)-1))
	except:
		news = get_news_from_indianexpress(1, "cities")
		return render_template("index.html",news=news,n=1, category=sec, title="News Headlines",pp="", np="2")

if __name__ == '__main__':
	app.run(debug=True)