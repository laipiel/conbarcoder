#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, Tkinter
import database
import logging
from pysqlite2 import dbapi2 as sqlite

class DBInitializer(Tkinter.Frame):
  def __init__(self, master=None):
    Tkinter.Frame.__init__(self, master)
    self.CreateWidgets()

  def CreateInitDBButtonHandler(self, create_query, drop_query, message):
    def handle():
      try:
        database.cursor_.execute(drop_query)
      except sqlite.OperationalError:
        pass
      try:
        database.cursor_.execute(create_query)
      except:
        message.set('Initialization failed.')
      else:
        message.set('Initialization successful.')

    return handle

  def CheckIfBarcodeExists(self, barcode):
    try:
      database.cursor_.execute(database.select_barcode_db_query, (barcode,))
    except sqlite.OperationalError as e:
      logging.debug(e)
      self.message.set('Initialize the database first!')

    return len(database.cursor_.fetchall()) != 0

  def HandleAddItem(self):
    attr_dict = {"barcode":int(self.additem_barcode_entry.get()), "dollar":int(self.additem_dollar_entry.get()), "cent":int(self.additem_cent_entry.get()), "category":int(self.additem_category_entry.get())}
    logging.info(attr_dict)

    if attr_dict["cent"] >= 100:
      self.message.set("cent must be >= 0 and < 100")
      return

    if self.CheckIfBarcodeExists(attr_dict["barcode"]):
      query = database.update_item_barcode_db_query
      input_tuple = (self.additem_name_entry.get(), attr_dict["dollar"], attr_dict["cent"], attr_dict["category"], attr_dict["barcode"])
    else:
      query = database.add_item_barcode_db_query
      input_tuple = (attr_dict["barcode"], self.additem_name_entry.get(), attr_dict["dollar"], attr_dict["cent"], attr_dict["category"])

    try:
      database.cursor_.execute(query, input_tuple)
      database.conn_.commit()
    except sqlite.OperationalError as e:
      logging.debug(e)
      self.message.set("AddItem failed.")
    else:
      self.message.set("AddItem successful.")

  def CreateAddItemWidgets(self):
    self.add_entry_label = Tkinter.Label(self)
    self.add_entry_label["text"] = "\n\nAdd items"
    self.add_entry_label.pack(fill=Tkinter.BOTH)

    self.additem_frame = Tkinter.Frame(self)

    self.additem_barcode_label = Tkinter.Label(self.additem_frame, text="Barcode: ")
    self.additem_barcode_label.pack(side=Tkinter.LEFT)

    self.additem_barcode_entry = Tkinter.Entry(self.additem_frame)
    self.additem_barcode_entry["validate"] = "key"
    self.additem_barcode_entry["validatecommand"] = (
        self.additem_barcode_entry.register(database.AcceptOnlyInteger), '%P')
    self.additem_barcode_entry.pack(side=Tkinter.LEFT)

    self.additem_name_label = Tkinter.Label(self.additem_frame, text="   Product Name: ")
    self.additem_name_label.pack(side=Tkinter.LEFT)

    self.additem_name_entry = Tkinter.Entry(self.additem_frame)
    self.additem_name_entry.pack(side=Tkinter.LEFT)

    self.additem_dollar_label = Tkinter.Label(self.additem_frame, text="   Dollar: ")
    self.additem_dollar_label.pack(side=Tkinter.LEFT)

    self.additem_dollar_entry = Tkinter.Entry(self.additem_frame, width=5)
    self.additem_dollar_entry["validate"] = "key"
    self.additem_dollar_entry["validatecommand"] = (
        self.additem_dollar_entry.register(database.AcceptOnlyInteger), '%P')
    self.additem_dollar_entry.pack(side=Tkinter.LEFT)

    self.additem_cent_label = Tkinter.Label(self.additem_frame, text="   Cent: ")
    self.additem_cent_label.pack(side=Tkinter.LEFT)

    self.additem_cent_entry = Tkinter.Entry(self.additem_frame, width=3)
    self.additem_cent_entry["validate"] = "key"
    self.additem_cent_entry["validatecommand"] = (
        self.additem_cent_entry.register(database.AcceptOnlyInteger), '%P')
    self.additem_cent_entry.pack(side=Tkinter.LEFT)

    self.additem_category_label = Tkinter.Label(self.additem_frame,
        text="   Category (in number): ")
    self.additem_category_label.pack(side=Tkinter.LEFT)

    self.additem_category_entry = Tkinter.Entry(self.additem_frame, width=3)
    self.additem_category_entry["validate"] = "key"
    self.additem_category_entry["validatecommand"] = (
        self.additem_category_entry.register(database.AcceptOnlyInteger), '%P')
    self.additem_category_entry.pack(side=Tkinter.LEFT)

    self.additem_frame.pack()

    self.additem_button = Tkinter.Button(self)
    self.additem_button["text"] = "Add Item"
    self.additem_button["command"] = self.HandleAddItem

    self.additem_button.pack()

  def CreateWidgets(self):
    self.message = Tkinter.StringVar()
    self.status_label = Tkinter.Label(self)
    self.status_label["textvariable"] = self.message

    self.status_label.pack()

    self.barcode_db_button = Tkinter.Button(self)
    self.barcode_db_button["text"] = "Clear Barcode DB"
    self.barcode_db_button["command"] = self.CreateInitDBButtonHandler(
        database.create_barcode_db_query, database.drop_barcode_db_query,
        self.message)

    self.barcode_db_button.pack()

    self.CreateAddItemWidgets()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,)
  root = Tkinter.Tk()
  app = DBInitializer(master=root)
  app.pack()
  app.mainloop()
