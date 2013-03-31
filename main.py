#! /usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter
import initdb
import price

import logging

current_frame = None

def FrameLoader(frame, root):
  def closure():
    global current_frame
    if current_frame:
      current_frame.pack_forget()

    current_frame = frame
    current_frame.pack()

  return closure

def main():
  root = Tkinter.Tk()
  #root.geometry('600x600+100+100')
  bar = Tkinter.Menu()

  initdb_frame = initdb.DBInitializer()
  price_frame = price.Pricer()

  command_dict = {'Initialize DBs':FrameLoader(initdb_frame, root),
                  'Price':FrameLoader(price_frame, root)}

  selection = Tkinter.Menu()
  for menu_name, handler in command_dict.items():
    selection.add_radiobutton(label=menu_name, command=handler)

  bar.add_cascade(label='Options', menu=selection)
  root.config(menu=bar)
  root.mainloop()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,)
  main()
