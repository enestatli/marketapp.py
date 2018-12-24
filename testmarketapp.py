import sqlite3 as sql #sqlite3 database kutuphanesini python'da kullanmak icin cektim as sql sql olarak kisaltmak icin
from tkinter import * #tkinter isimli kutuphaneyi arayuzu tasarlamak ve buttonlar'a komut atamak icin 
import csv #txt, csv uzantili dosyalardan veri cekmek icin

class Ercan_db: #bu database olusturdugum sinifim

    def __init__(self):
        self.conn=sql.connect('market.db') #ercan.db isimli bir tane database dosyasi olusturur
        self.cur = self.conn.cursor() #cursor olusturdum. database'e veri ekleme,silme,update etme gibi islerde kullanirim

        self.cur.execute("CREATE TABLE IF NOT EXISTS ErcanBakkal (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                                                                    client TEXT NOT NULL,\
                                                                    product TEXT NOT NULL,\
                                                                    adet INTEGER NOT NULL,\
                                                                    price INTEGER NOT NULL,\
                                                                    total_price INTEGER NOT NULL)") # tablo olusturup tablodaki kolonlarin isimlerini verdim id, client, product gibi
        self.conn.commit() #olusturulan tabloyu gunceller


    def view(self):
        self.cur.execute("SELECT * FROM ErcanBakkal") #(*) ile tablomu(databasemi) seciyorum komple
        rows = self.cur.fetchall() #rows adli degiskene sectigim tablodaki verileri kaydediyorum. 
        return rows #rows degiskenine donderiyorum fonksiyonu, bu fonskiyonun sonucu her zaman rows olarak cikacak

    def insert(self,client,product,adet,price,total_price):
        self.cur.execute("INSERT INTO ErcanBakkal VALUES (NULL,?,?,?,?,?)",(client,product,adet,price,total_price)) #girilen verileri databasemin kolonlarina insert ediyorum
        self.conn.commit()
        self.view() #yukarda tanimladigim view fonksiyonunu bu fonksiyon icinde calistiriyorum

    """def update(self,ID,client,product,adet,price,total_price): #bura calismadi :D
                    self.cur.execute("UPDATE ErcanBakkal SET client=?,\
                                                            product=?,\
                                                            adet=?,\
                                                            price=?,\
                                                            total_price=?\
                                                            WHERE ID=?",(client,product,adet,price,total_price,ID))
        self.conn.commit()
        self.view()"""

    def delete(self,ID):
        self.cur.execute("DELETE FROM ErcanBakkal WHERE ID=?",(ID,)) #secilen id'yi siliyorum
        self.conn.commit()
        self.view()

    def search(self,client="",product="",adet=""):
        self.cur.execute("SELECT * FROM ErcanBakkal WHERE client=?\
                                                        OR product=?\
                                                        OR adet=?",(client,product,adet)) #girilen isme gore arama yapar
        rows = self.cur.fetchall() 
        return rows

    def calculate(self,client):
        self.cur.execute("SELECT * FROM ErcanBakkal") 
        rows = self.cur.fetchall() #rows adli degiskene sectigim tablodaki verileri kaydediyorum.
        result = 0 #result adinda bir degiskeni 0'a esitliyorum tablonun icinden cektigim veriyi buna kendini ekletiyorum
        for row in rows: #tablo icindeki verileri row ile tek tek gez;
            if (client==row[1]): #eger gezdigin veri benim isim olarak girdigim veriyle ayniysa;
                result += int(row[5]) #o isimde row[5] kolonundaki degerleri result degiskenine topla
        return result        

db = Ercan_db() #sinifimi burada db degiskenine atiyorum



def get_selected_row(event): #listeden mousela veri secmek icin
    global selected_tuple #global bir degisken tanimladim, sistemde her yerde gorunsun bu degisken
    index = list1.curselection() #listede mouse'la sectigim row'un index degiskenine kaydet diyorum
    if index: #sectigim index bos degilse
        selected_tuple=list1.get(index[0]) #global degiskenimi index[0] yani listede tiklanan ID'ye ata dedim
        entryClient.delete(0,END) #client entry'sini temizle
        entryClient.insert(END, selected_tuple[1]) #client entry'sine listede tikladigim id'nin client kolonuyla doldur
        entryProduct.delete(0,END)
        entryProduct.insert(END, selected_tuple[2])
        entryAdet.delete(0,END)
        entryAdet.insert(END, selected_tuple[3])


def view_command():
    list1.delete(0,END) #listeyi temizle
    for row in db.view(): #view fonskiyonundan gelen butun rowlari;
        list1.insert(END,row) #listemde goster

def search_command():
    list1.delete(0,END) #listeyi temizle
    for row in db.search(clientText.get(),productText.get(),adetText.get()): #entrylere girilen degerlere gore;
        list1.insert(END,row) #listemde goster ilgili client'i vs

def add_command():
    db.insert(clientText.get(),productText.get(),adetText.get(),get_price(),get_total_price()) #entrylere girilen degerleri ekle
    list1.delete(0,END) #listeyi temizle
    list1.insert(END,(clientText.get(),productText.get(),adetText.get(),get_price(),get_total_price())) #listede goster

def delete_command():
    db.delete(selected_tuple[0]) #listede secilen row'u sil

"""def update_command():
    db.update(selected_tuple,clientText.get(),productText.get(),adetText.get(),get_price(),get_total_price())"""

def get_price(): #test.csv isimli dosyadan urunlerin fiyatlarini cekmek icin olusturulan fonskiyon
    with open('test.csv') as file: #test.csv dosyasina gir
        reader = csv.DictReader(file) #reader degiskenine okunan verileri ata
        r = 0
        for row in reader: #okunan verilerde row ile gezin
            if (row['product'] == productText.get()): #csv dosyasi icindeki product ile entry olarak girilen ayniysa;
                r += int(row['price']) #fiyatini sayisal olarak cek
        return r 

def get_total_price():
    return get_price() * int(adetText.get())

def calculate_command():
    entryResult.delete(0,END)
    entryResult.insert(END,db.calculate(clientText.get()))

#---------------------------BURDAN SONRASI TKINTER ILE ARAYUZU OLUSTURMAK ICIN---------------------------#

window = Tk()

window.title("BEKKAL")

"""def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd

root.protocol("WM_DELETE_WINDOW", on_closing)"""

l1 = Label(window, text="Client")
l1.grid(row=0, column=0)

l2 = Label(window, text="Product")
l2.grid(row=0, column=2)

l3 = Label(window, text="Number")
l3.grid(row=1, column=0)

clientText = StringVar()
entryClient = Entry(window, textvariable=clientText)
entryClient.grid(row=0, column=1)

productText = StringVar()
entryProduct = Entry(window, textvariable=productText)
entryProduct.grid(row=0, column=3)

adetText = StringVar()
entryAdet = Entry(window, textvariable=adetText)
entryAdet.grid(row=1, column=1)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="View All", width=12, command=view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Search Client", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add Client", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update Selected", width=12)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete Selected", width=12, command=delete_command)
b5.grid(row=6, column=3)

"""b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)"""

b7 = Button(window, text="Calculate", width=12,command=calculate_command)
b7.grid(row=8, column=3)

l4 = Label(window, text="RESULT")
l4.grid(row=8, column=0)

entryResult = Entry(window)
entryResult.grid(row=8,column=1)

window.mainloop()