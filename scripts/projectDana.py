#!/usr/bin/env python3
# -*- coding: utf-8 -

from sre_parse import CATEGORIES
from sys import argv
import csv

CATEGORIES = {
    "Computer": "Computers",
    "PC": "Computers",
    "Audio": "Audio",
    "Tablet": "Tablets",
    "Accessorie": "Accessories",
    "TV": "TV",
    "Television": "TV",
    "Video": "Video",
    "Speaker": "Speakers",
    "Camera": "Cameras",
    "Headphone": "Headphones",
    "Headset": "Headphones",
    "Photo": "Photo",
    "Car": "Car",
    "Mobile": "Mobile",
    "Cell Phone": "Mobile",
    "Laptop": "Laptops",
    "Storage": "Storage",
    "Drive": "Storage",
    "Keyboard": "Keyboards",
    "Network": "Network",
    "Home Theater": "Home Theater",
    "Bluetooth": "Bluetooth",
    "Wireless": "Bluetooth",
    "Monitor": "Screens",
    "Screen": "Screens",
    "Stereo": "Stereo",
    "Office": "Office",
    "Desktop": "Office",
    "Component": "Components",
    "Wi-Fi": "Wi-Fi",
    "Video Game": "Video Games",
    "Mice": "Mice",
    "Mouse": "Mice",
    "MP3 Player": "Media Player",
    "Media Player": "Media Player",
    "Batterie": "Batteries",
    "CD": "CD",
    "DVD": "DVD",
    "Blu-ray": "Blu-ray",
    "Microphone": "Microphones",
    "Router": "Router",
    "GPS": "GPS",
    "Adapter": "Adapters & Cables",
    "Cable": "Adapters & Cables",
    "Xbox": "Console",
    "PlayStation": "Console",
    "Nintendo": "Console"
}

class ModifyData:
    def __init__(self, source, dest) -> None:
        self._src = csv.reader(open(source))
        self._dest = csv.writer(open(dest, "w"), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self._columns = []
        self._data = []
        self.extract_data_csv()

    def extract_data_csv(self):
        i = 0
        for row in self._src:
            if i == 0:
                self._columns = row
            else:
                self._data.append(row)
            i+=1

    def write_data_csv(self):
        for row in self._data:
            self._dest.writerow(row)

    def sort_categories(self):
        for iCol in range(len(self._columns)):
            if self._columns[iCol].startswith("categories"):
                for row in self._data:
                    newCategRow = set()
                    for categ in row[iCol].split(','):
                        for keyCateg, newCateg in CATEGORIES.items():
                            if categ.find(keyCateg) != -1:
                                # print(f"categ {categ} .find(keyCateg) {keyCateg}")
                                newCategRow.add(newCateg)
                    newRow = ""
                    for newCateg in newCategRow:
                        newRow += newCateg + ","
                    row[iCol] = newRow[:-1] # suppression de la dernière virgule

    def get_column_freq(self, column_name):
        freq = dict()
        for iCol in range(len(self._columns)):
            if self._columns[iCol].startswith(column_name):
                for row in self._data:
                    for data in row[iCol].split(','):
                        if data in freq:
                            freq[data] += 1
                        else:
                            freq[data] = 1
        return freq
    
    def print_column_ordered(self, column_name):
        freq = self.get_column_freq(column_name)
        ordered = sorted(freq.items(), key=lambda x: x[1])
        for data in ordered:
            print(f'{data[1]}. {data[0]}')
        print(f"There are {len(ordered)} different values for the column {column_name}")

if __name__=='__main__':
    if len(argv)!=3:
        print(f"""utilisation : {argv[0]} <source> <destination>
        - <source> est le chemin vers le csv contenant les données source
        - <destination> est le chemin vers le csv contenant les données modifiées. Si le fichier existe déjà, cela l'écrase.""")
        exit(1)
    modifData = ModifyData(argv[1], argv[2])
    print(modifData._columns)
    modifData.print_column_ordered("categories")
    modifData.sort_categories()
    modifData.print_column_ordered("categories")
    modifData.write_data_csv()
