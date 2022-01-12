

from PyQt5.QtSql import QSqlRecord


class Urun():
    #Id = int()
    #UrunAdi = str()
    def __init__(self, record : QSqlRecord):
        self.Id = record.value("UrunId")
        self.UrunAdi =record.value("UrunAdi")
        