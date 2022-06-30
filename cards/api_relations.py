import requests
import json

def translate_word(fromlang, text):

	url = "https://cheap-translate.p.rapidapi.com/translate"
	payload = {
		"fromLang": fromlang,
		"text": text,
		"to": 'en'
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "47e8381166msh29eed1d31927cf6p1164d7jsnf7268929f90f",
		"X-RapidAPI-Host": "cheap-translate.p.rapidapi.com"
	}
	response = requests.request("POST", url, json=payload, headers=headers)
	return json.loads(response.text)['translatedText']


def random_word():
	url = "https://random-words-api.vercel.app/word"
	response = requests.request("GET", url)
	return json.loads(response.text)[0]['word']

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

	url = "https://microsoft-translator-text.p.rapidapi.com/translate"

	querystring = {"to[0]": lang, "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}

	payload = [{"Text": text}]
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "47e8381166msh29eed1d31927cf6p1164d7jsnf7268929f90f",
		"X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
	}

	response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

	trans_word = json.loads(response.text)
	return trans_word[0]['translations'][0]['text']
