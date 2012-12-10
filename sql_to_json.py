#!/usr/bin/env python3
import re
import json


metaPattern = re.compile(r"INSERT INTO `metaWords` \(`id`,`navi`,`ipa`,`infixes`,`partOfSpeech`\) VALUES \('(\d+)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)',(?:'((?:[^'\\]|\\.)*)'|NULL),'((?:[^'\\]|\\.)*)'\);")
localizedPattern = re.compile(r"INSERT INTO `localizedWords` \(`id`,`languageCode`,`localized`,`partOfSpeech`\) VALUES \('(\d+)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'\);")
unescapePattern = re.compile(r"\\(.)")

sql = ""
with open("dict.sql", "r", encoding="utf8") as f:
	sql = f.read()

words = {}
for found in metaPattern.finditer(sql):
	groups = list(found.groups())
	for i in range(len(groups)):
		if groups[i]:
			groups[i] = unescapePattern.sub(r"\1", groups[i].strip())
	words[int(groups[0])] = {"id": int(groups[0]), "navi": groups[1], "ipa": groups[2], "infixes": groups[3], "partOfSpeech": groups[4], "localized": {}}

for found in localizedPattern.finditer(sql):
	groups = list(found.groups())
	for i in range(len(groups)):
		groups[i] = unescapePattern.sub(r"\1", groups[i].strip())
	words[int(groups[0])]["localized"][groups[1]] = {"languageCode": groups[1], "localized": groups[2], "partOfSpeech": groups[3]}

def sortFunc(elem):
	return elem["id"]

with open("dict.json", "w", encoding="utf8") as f:
	json.dump(sorted(words.values(), key=sortFunc), f, ensure_ascii=False, indent="\t", sort_keys=True)
