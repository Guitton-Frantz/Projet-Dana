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

PRICES_AVAILABILITY = {
    "In Stock": "In Stock",
    "Yes": "In Stock",
    "yes": "In Stock",
    "TRUE": "In Stock",
    "available": "In Stock",
    "Out Of Stock": "Out Of Stock",
    "FALSE": "Out Of Stock",
    "No": "Out Of Stock",
    "sold": "Out Of Stock",
    "Retired": "Out of Stock",
    "More on the Way": "More on the Way",
    "Special Order": "Special Order",
    "undefined": ""
}

PRICES_CONDITION = {
    "New": "New",
    "new": "New",
    "Used": "Used",
    "refurbished": "Refurbished",
    "refurbished": "Refurbished",
    "pre-owned": "Pre-owned"
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
        self._dest.writerow(self._columns)
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
    
    def sort_prices_availability(self):
        for iCol in range(len(self._columns)):
            if self._columns[iCol].startswith("prices.availability"):
                for row in self._data:
                    data = row[iCol]
                    newData = ""
                    for keyPA, newPA in PRICES_AVAILABILITY.items():
                        if data.find(keyPA) != -1:
                            newData = newPA
                            break
                    row[iCol] = newData
                
    def sort_prices_condition(self):
        for iCol in range(len(self._columns)):
            if self._columns[iCol].startswith("prices.condition"):
                for row in self._data:
                    data = row[iCol]
                    newData = ""
                    for keyPC, newPC in PRICES_CONDITION.items():
                        if data.find(keyPC) != -1:
                            newData = newPC
                            break
                    row[iCol] = newData

    def add_to_freq(freq, data):
        if data in freq:
            freq[data] += 1
        else:
            freq[data] = 1

    def get_column_freq(self, column_name, column_list=False):
        freq = dict()
        for iCol in range(len(self._columns)):
            if self._columns[iCol].startswith(column_name):
                for row in self._data:
                    if column_list: # variante pour les colonnes comporant des listes
                        for data in row[iCol].split(','):
                            ModifyData.add_to_freq(freq, data)
                    else:
                        ModifyData.add_to_freq(freq, row[iCol])
        return freq
    
    def print_column_ordered(self, column_name, column_list=False):
        freq = self.get_column_freq(column_name, column_list)
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
    
    modifData.print_column_ordered("categories", True)
    modifData.sort_categories()
    modifData.print_column_ordered("categories", True)

    modifData.print_column_ordered("prices.availability")
    modifData.sort_prices_availability()
    modifData.print_column_ordered("prices.availability")

    modifData.print_column_ordered("prices.condition")
    modifData.sort_prices_condition()
    modifData.print_column_ordered("prices.condition")

    modifData.write_data_csv()

