#!/usr/bin/python
# -*-coding:Utf-8 -*


"""
Layer for the xlrd module, which reads an xls file (Excel file,
format of 2003).
This module is written with the purpose to facilitate the reading
of an Excel file. It provides a very simple EasyXls object.

It mainly implements a parser function, which transforms "A1", "A", "1"
or "AA1" into the corresponding indexes, such if you do something like:

    xls.value("A")

You will get all the values of the column.
    
    xls.value("1")

will return the values of row 1.

   xls.value("A1")

will return the value of cell A1.
"""


import re
import xlrd
from xlwt import Workbook


class EasyXls():

    def __init__(self, workbook):


        #Opening of the workbook. No need to specify
        #the extension
        #TODO: handle errors
        self.name = workbook
        self.wb = xlrd.open_workbook(self.name + ".xls")

        #Attribute containing the names of all the sheets
        #in the workbook
        self.names_sheets = self.wb.sheet_names()

        #By default, the first sheet is loaded, but the method
        #change_sheet(name_of_the_sheet) can change that
        self.feuille = self.wb.sheet_by_name(self.names_sheets[0])


        self.workbootout = Workbook()
        self.sheet_out = self.workbootout.add_sheet("OCB")


    def parse(self, string):

        """transforms "A1", "A", "1" or "AA1" into the corresponding
        indexes. Should be private, use ONLY in this class"""

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        string = str(string)

        #Find the number(s) of the cell(s)
        nbr = re.findall('\d+', string)

        if nbr:
            lettres = string.replace(nbr[0], '')
            index_nbr = int(nbr[0]) - 1
        else:
            lettres = string
            index_nbr = None

        index_lettre = None

        for position, lettre in enumerate(lettres):

            if index_lettre is None:
                index_lettre = 0

            #Calculate the good index:
            #AA differs from AAA
            if position != 0:
                index_lettre += 26**position

            index_lettre += alphabet.index(lettre)

        return (index_lettre, index_nbr)


    def value(self, string):

        """Returns the value(s) of the specified cell(s)"""

        index_lettre, index_nbr = self.parse(string)

        #Get one liste with the required values.
        if index_lettre is None:
            liste =  self.feuille.row_values(index_nbr)
        elif index_nbr is None:
            liste = self.feuille.col_values(index_lettre)
        elif index_nbr is not None and index_lettre is not None:
            liste = self.feuille.cell_value(index_lettre, index_nbr)

        new_liste = []

        #Returns only the non empty values.
        #Try to convert the values to float.
        for value in liste:
            if not value:
                continue
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass

            new_liste.append(value)

        return new_liste 


    def change_sheet(self, name):

        """Change the current sheet of the workbook"""

        self.feuille = self.wb.sheet_by_name(name)


    def write(self, coo, content, sens="h"):

        """Writes the values in a file called NameOfTheWorkbook + _out,
        to not earase the current notebook""" 

        index_lettre, index_nbr = self.parse(coo)

        if index_lettre is None:
            index_lettre = 0
        if index_nbr is None:
            index_nbr = 0

        if type(content) is list:

            if sens is "h":
                for index, value in enumerate(content):
                    print(index_nbr, index_lettre)
                    self.sheet_out.write(index_nbr, index_lettre + index, value)

            elif sens is "v":
                for index, value in enumerate(content):
                    self.sheet_out.write(index_nbr + index, index_nbr, value)

        else:
            if index_nbr is not None and index_lettre is not None:
                return self.feuille.cell_value(index_lettre, index_nbr)
            else:
                print("Problème coo, et le content n'est pas une liste")

        #Writing the workbook
        self.workbootout.save(self.name + "_out.xls")



if __name__ == "__main__":

    xls = EasyXls("5nM")
    #print(xls.value("B2"))
    print(xls.value("A"))

