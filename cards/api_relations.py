import requests
import json

def translate(fromlang, text, to):
	url = "https://cheap-translate.p.rapidapi.com/translate"
	payload = {
		"fromLang": fromlang,
		"text": text,
		"to": to
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "47e8381166msh29eed1d31927cf6p1164d7jsnf7268929f90f",
		"X-RapidAPI-Host": "cheap-translate.p.rapidapi.com"
	}
	response = requests.request("POST", url, json=payload, headers=headers)
	return json.loads(response.text)['translatedText']


def random_word():
	url = "https://random-word-api.herokuapp.com/word"
	response = requests.request("GET", url)
	return json.loads(response.text)[0]

def definition(word):
	url = "https://dictionary-by-api-ninjas.p.rapidapi.com/v1/dictionary"
	querystring = {"word": word}
	headers = {
		"X-RapidAPI-Key": "47e8381166msh29eed1d31927cf6p1164d7jsnf7268929f90f",
		"X-RapidAPI-Host": "dictionary-by-api-ninjas.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	definition = json.loads(response.text)
	return definition['definition']

def words_of_a_day(lang, text):

	url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
	payload = "q={}&target={}&source=en".format(text, lang)
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"Accept-Encoding": "application/gzip",
		"X-RapidAPI-Key": "47e8381166msh29eed1d31927cf6p1164d7jsnf7268929f90f",
		"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	trans_word = json.loads(response.text)
	return trans_word['data']['translations'][0]['translatedText']

