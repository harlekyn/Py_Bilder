import os
import re
import shutil
import pyexiv2      # ExIf Daten auslesen
import tqdm         # https://github.com/tqdm/tqdm
import ConfigParser


#
## Ort auslesen

config = ConfigParser.ConfigParser()
config.read('settings.ini')

ort = config.get('Allgemein', 'Ort')
typ = config.get('Allgemein', 'Typ')

print '[*] Einstellung: ' + ort
print '[*] Einstellung: ' + typ

#
## Funktion: Umbenennen

def umbenennen(original):
    metadata = pyexiv2.ImageMetadata(original)
    metadata.read()
    tag = metadata['Exif.Image.DateTime']
    date_pic = tag.value
    neu = '20' + date_pic.strftime("%y-%m-%d-%H-%M-%S")
    
    try:
        os.rename(original, neu + '.jpg')
    except OSError as e:
        print ('[-] Error: %s' % e)
        try:
            os.rename(original, neu + '_Copy.jpg')
        except OSError as e:
            print ('[-] 2.Error: %s' % e)
            try:
                os.rename(original, neu + '_Copy2.jpg')
            except OSError as e:
                print ('[-] 3.Error: %s' % e)

#
## Ordner durchsuchen

for root, path, files in os.walk(ort):
    for filename in files:
        string1 = str(filename)    # Umwandeln in String
        string2 = re.sub(r'\'', '', string1) # Entfernen von '
        string3 = re.sub(r'\[', '', string2) # Entfernen von [
        string4 = re.sub(r'\]', '', string3) # Entfernen von ]

        if string4.endswith(typ):
            datei = os.path.join(root, string4)
            print '[*] Datei: ' + datei
            umbenennen(datei)
