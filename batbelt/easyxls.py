#!/usr/bin/python
# coding: utf-8

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
import numpy as np
from xlwt import Workbook
from typing import Optional, Tuple, Any, List, Union


class EasyXls:
    def __init__(self, workbook: str) -> None:

        # Opening of the workbook. No need to specify
        # the extension
        # TODO: handle errors
        self.name = workbook

        self.wb = xlrd.open_workbook(self.name)

        # Attribute containing the names of all the sheets
        # in the workbook
        self.names_sheets = self.wb.sheet_names()

        # By default, load first sheet
        self.sheet = self.wb.sheet_by_name(self.names_sheets[0])

        self.workbootout = Workbook()
        self.sheet_out = self.workbootout.add_sheet("OCB")

    def _parse(self, input_str: str) -> Tuple[int, int]:

        """
        Transforms "A1", "A", "1" or "AA1" into the corresponding indexes

        Arguments:
            input_str (str): a Excel column name (letter), row index, or cell coo

        Returns:
            Tuple[int, int]: the true coordinates of the selected cells
        """

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        input_str = str(input_str)

        # Find the number(s) of the cell(s)
        nbr = re.findall("\d+", input_str)

        index_nbr: Optional[int]

        if nbr:
            # Delete the numbers in the input_str to get only the letters
            letters = input_str.replace(nbr[0], "")

            # Get the index by substracting 1 to the number
            index_nbr = int(nbr[0]) - 1
        else:
            letters = input_str
            index_nbr = None

        index_letter = None

        for position, lettre in enumerate(letters):

            if index_letter is None:
                index_letter = 0

            # Calculate the good index:
            # AA differs from AAA
            if position != 0:
                index_letter += 26 ** position

            index_letter += alphabet.index(lettre)

        return (index_letter, index_nbr)

    def get_all_columns(self) -> List[List[Any]]:

        """
        Returns a list of lists of the values of all the columns of a sheet
        One list per column.

        Returns:
            List[List[Any]]: list of list of values. Type is unpredictable, could be
                             str, int, float or other
        """

        data_list = []

        for i in range(self.sheet.ncols):
            data_to_add = [v if v != "" else np.nan for v in self.sheet.col_values(i)]
            if data_to_add:
                data_list.append(data_to_add)

        return data_list

    def get_all_rows(self) -> List[List[Any]]:

        """
        Returns a list of lists of the values of all the rows of a sheet
        One list per row.

        Returns:
            List[List[Any]]: list of list of values. Type is unpredictable, could be
                             str, int, float or other
        """

        data_list = []

        for i in range(self.sheet.nrows):
            data_to_add = [v if v != "" else np.nan for v in self.sheet.row_values(i)]
            if data_to_add:
                data_list.append(data_to_add)

        return data_list

    def value(self, input_str: str) -> List[Any]:

        """
        Returns the value(s) of the specified cell(s)

        Arguments:
            input_str (str): selection of cells

        Returns:
            List[Any]: list of values for selected cells. If selection is a row, return
                       all the values in row. If selection is column, return values in
                       columun. If selection is a cell, return a list of len 1 with the
                       cell value
        """

        index_letter, index_nbr = self._parse(input_str)

        # Get one liste with the required values.
        if index_letter is None:
            liste = self.sheet.row_values(index_nbr)
        elif index_nbr is None:
            liste = self.sheet.col_values(index_letter)
        elif index_nbr is not None and index_letter is not None:
            liste = [self.sheet.cell_value(index_nbr, index_letter)]

        return liste

    def change_sheet(self, name: str) -> None:

        """
        Change current sheet of the workbook

        Arguments:
            name (str): name of the sheet to switch to

        Returns:
            None
        """

        self.sheet = self.wb.sheet_by_name(name)

    def write(
        self,
        coo: Union[str, Tuple[int, int]],
        content: Union[List[Any], Any],
        direction: str = "h",
        path: str = None,
    ) -> None:

        """
        Arguments:
            coo (Union[str, Tuple[int, int]]: cell, or row, or col coordinates
            content (Union[List[Any, Any]]): content to write.
                                             Sould be a lost or any value
            direction (str): how to write the content.
                             h for horizontally, v for vertically
            path (str): default None. Path for the output workbook.
                        If None, output path will be forged from input file + _out.xlsx

        Returns:
            None:
        """

        if type(coo) is str:
            index_letter, index_nbr = self._parse(coo)

            if index_letter is None:
                index_letter = 0
            if index_nbr is None:
                index_nbr = 0
        elif type(coo) is tuple:
            index_letter = coo[0]
            index_nbr = coo[1]
        else:
            raise TypeError("coo must be a string or a tuple")

        if type(content) is list:

            if direction is "h":
                for index, value in enumerate(content):
                    self.sheet_out.write(index_nbr, index_letter + index, value)
            elif direction is "v":
                for index, value in enumerate(content):
                    self.sheet_out.write(index_nbr + index, index_letter, value)
            else:
                raise ValueError("Sens must be either 'h' or 'v'")

        else:
            if index_nbr is not None and index_letter is not None:
                self.sheet_out.write(index_nbr, index_letter, content)
            else:
                raise ValueError("Cell's coo not provided and content not a list")

        # Write in the workbook
        if path is None:
            self.workbootout.save(self.name + "_out.xls")
        else:
            self.workbootout.save(path)


if __name__ == "__main__":
    import os

    data_path = os.path.join("sales_in", "MAXILASE__Jan-March__2016.xlsx")
    xls = EasyXls(data_path)
    # print(xls.value("B2"))
    # print(xls.value("A"))
