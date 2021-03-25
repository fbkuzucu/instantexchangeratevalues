from PyQt5 import QtWidgets
import sys
import requests
from bs4 import BeautifulSoup
import sqlite3

class Pencere(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()
        self.baglanti()


    def baglanti(self):

        self.baglanti = sqlite3.connect("doviz.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kurlar (birimler TEXT,degerler TEXT)")
        self.baglanti.commit()

    def init_ui(self):

        self.baslik = QtWidgets.QLabel("Döviz Hesaplama Programına Hoşgeldiniz!")
        self.kur1 = QtWidgets.QLineEdit()
        self.yazi_alani = QtWidgets.QLabel("Anlık kur değerini görmek isterseniz\nLütfen üstteki boşluğa ismini yazınız\nNot = Veritabanı Oluşturma İşlemi Bi Kereliğine Mahsustur\nÇıkış Yapmayı Unutmayınız Aksi Halde Veritabanı Düzgün Çalışmaz\nAlttaki Boşlukları Hesaplama İçin Kullanabilirsiniz")
        self.hesapla = QtWidgets.QPushButton("Değeri Öğren")
        self.veritabani = QtWidgets.QPushButton("Veritabanı Oluştur")
        self.cikis = QtWidgets.QPushButton("Çıkış Yap")



        x = QtWidgets.QHBoxLayout()
        x.addWidget(self.hesapla)
        x.addWidget(self.veritabani)
        x.addWidget(self.cikis)

        a = QtWidgets.QHBoxLayout()
        a.addStretch()
        a.addWidget(self.yazi_alani)
        a.addStretch()

        y = QtWidgets.QVBoxLayout()

        y.addWidget(self.baslik)
        y.addWidget(self.kur1)
        y.addLayout(a)
        y.addStretch()
        y.addLayout(x)

        self.cikis.clicked.connect(self.click)
        self.veritabani.clicked.connect(self.click)
        self.hesapla.clicked.connect(self.click)
        self.setLayout(y)
        self.setWindowTitle("Döviz Programı")
        self.show()

    def click(self):
        sender = self.sender()

        if (sender.text() == "Veritabanı Oluştur"):
            self.yazi_alani.setText("Veritabanı Oluştu!")
            self.doviz()

        elif (sender.text() == "Değeri Öğren"):
            self.value()

        elif (sender.text() == "Çıkış Yap"):
            self.cursor.execute("Delete From kurlar")
            self.baglanti.commit()
            QtWidgets.qApp.quit()



    def doviz(self):

        deger = list()
        kur = list()
        deg = list()
        url = "https://www.doviz.com/"
        response = requests.get(url)
        icerik = response.content
        soup = BeautifulSoup(icerik,"html.parser")

        kurlar = soup.find_all("span",{"class":"name"})
        degerler = soup.find_all("span",{"class":"value"})

        for a, b in zip(kurlar, degerler):
            a = a.text
            b = b.text

            a = a.strip()
            a = a.replace("\n", " ")

            b = b.strip()
            b = b.replace("\n", " ")
            b = b.replace(",",".")
            b = b.replace("$"," ")

            kur.append(a)
            deger.append(b)
        
        kur.remove(kur[5])
        deger.remove(deger[5])
        

        for a in deger:
            a = float(a)
            deg.append(a)


        for a, b in zip(kur,deger):
            self.cursor.execute("insert into kurlar values (?,?)",(a,b))
            self.baglanti.commit()




    def value(self):
        a = self.kur1.text()
        self.cursor.execute("select * from kurlar where birimler = ?", (a,))
        x = self.cursor.fetchall()
        if (len(x) == 0):
            self.yazi_alani.setText("Değerini öğrenmek istediğiniz kuru lütfen büyük harflerle girin ya da veritabanında aradığınız kur olmayabilir ama hangisi olduğunu söylemem")
        else:
            self.yazi_alani.setText("{} = {}".format(x[0][0],x[0][1]))














app = QtWidgets.QApplication(sys.argv)
pencere = Pencere()
sys.exit(app.exec_())

