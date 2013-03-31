#! /usr/bin/python
# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite

create_barcode_db_query = 'create table BarcodeDB(barcode int NOT NULL, \
name varchar(255), dollar int DEFAULT 0, cent int DEFAULT 0, category NOT \
NULL, PRIMARY KEY (barcode), CHECK (barcode >= 0), CHECK (dollar >= 0), CHECK \
(cent >= 0), CHECK (cent < 100))'

drop_barcode_db_query = 'drop table BarcodeDB'

select_barcode_db_query = 'SELECT * FROM BarcodeDB WHERE barcode=?'

update_item_barcode_db_query = 'UPDATE BarcodeDB SET name=?, dollar=?, cent=?, category=? WHERE barcode=?'

add_item_barcode_db_query = 'INSERT INTO BarcodeDB VALUES (?, ?, ?, ?, ?)'

delete_item_barcode_db_query = 'DELETE FROM BarcodeDB WHERE barcode=?'

conn_ = sqlite.connect('conDB')
cursor_ = conn_.cursor()

def AcceptOnlyInteger(new_value):
  if new_value == '':
    return True
  try:
    int(new_value)
  except ValueError as e:
    return False

  return True
