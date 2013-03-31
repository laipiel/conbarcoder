#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, Tkinter
import database
import logging
from pysqlite2 import dbapi2 as sqlite

class Pricer(Tkinter.Frame):
  def __init__(self, master=None):
    Tkinter.Frame.__init__(self, master)
    self.CreateWidgets()

  def CalculateTax(self, dollar, cent, category):
    return dollar, cent

  def HandleLookup(self, new_value):
    if not database.AcceptOnlyInteger(new_value):
      return False

    if new_value == '':
      new_value = 0
    
    barcode = int(new_value)
    database.cursor_.execute(database.select_barcode_db_query, (barcode,))
    result = database.cursor_.fetchall()

    if len(result) == 0:
      self.lookup_info.set('Item not found')
      self.lookup_price.set('')
      self.deleteitem_button['state'] = Tkinter.DISABLED
    else:
      result = result[0]
      display_msg = 'Name: %s, Category: %d' % (result[1], result[4])
      self.lookup_info.set(display_msg)

      after_tax_dollar, after_tax_cent = self.CalculateTax(result[2], result[3], result[4])

      price_msg = '$%d.%02d ($%d.%02d)' % (result[2], result[3], after_tax_dollar, after_tax_cent)
      self.lookup_price.set(price_msg)
      self.deleteitem_button['state'] = Tkinter.NORMAL

    logging.info(result)
    return True

  def HandleDeleteButton(self):
    try:
      database.cursor_.execute(database.delete_item_barcode_db_query,
          (int(self.lookup_barcode_entry.get()), ))
      database.conn_.commit()
    except sqlite.OperationalError as e:
      logging.debug(e)
      error_msg = 'barcode=[%s] deletion failed.' % (self.lookup_barcode_entry.get())
      self.lookup_info.set(error_msg)
    else:
      msg = 'barcode=[%s] deletion successful.' % (self.lookup_barcode_entry.get())
      self.lookup_info.set(msg)
      self.deleteitem_button['state'] = Tkinter.DISABLED

    self.lookup_barcode_entry.set_focus()

  def CreateWidgets(self):
    self.lookup_frame = Tkinter.Frame(self)

    self.lookup_barcode_label = Tkinter.Label(self.lookup_frame, text="Barcode: ")
    self.lookup_barcode_label.pack(side=Tkinter.LEFT)

    self.lookup_barcode_entry = Tkinter.Entry(self.lookup_frame)
    self.lookup_barcode_entry['validate'] = 'key'
    self.lookup_barcode_entry['validatecommand'] = (
        self.lookup_barcode_entry.register(self.HandleLookup), '%P')
    self.lookup_barcode_entry.pack(side=Tkinter.LEFT)

    self.lookup_frame.pack()

    self.lookup_info = Tkinter.StringVar()
    self.lookup_info_label = Tkinter.Label(self,
        textvariable=self.lookup_info)
    self.lookup_info_label.pack()

    self.lookup_price = Tkinter.StringVar()
    self.lookup_price_label = Tkinter.Label(self,
        textvariable=self.lookup_price,
        font=('Helvetica', 50),
        fg='red')
    self.lookup_price_label.pack()

    self.deleteitem_button = Tkinter.Button(self)
    self.deleteitem_button["text"] = "Delete Item"
    self.deleteitem_button['state'] = Tkinter.DISABLED
    self.deleteitem_button['command'] = self.HandleDeleteButton

    self.deleteitem_button.pack()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,)
  root = Tkinter.Tk()
  app = Pricer(master=root)
  app.pack()
  app.mainloop()
