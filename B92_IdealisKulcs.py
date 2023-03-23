import tkinter as tk
from tkinter import *
import random #python random module

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class GUI:
    
    def __init__(self):
        self.noise=0.1
        self.safety=10
        self.root=tk.Tk()
        self.zajosBit=0
        self.photo = PhotoImage(file = "b92.ico")
        self.root.iconphoto(False, self.photo)

        self.root.title("B92 Ideális kulcs")
        self.root.geometry("500x400")
        self.label=tk.Label(self.root, text="Beállítások")
        self.label.pack(padx=20,pady=20)
        self.zaj = Scale(self.root, from_=0, to=50,tickinterval=50, orient=HORIZONTAL, label="Zaj")
        self.zaj.pack()
        self.zaj.set(10)
        self.safety = Scale(self.root, from_=0, to=10,tickinterval=10, orient=HORIZONTAL , label="Kockázat")
        self.safety.pack()
        self.safety.set(10)
        self.button=tk.Button(self.root, text="Start", command = self.szimulacio)
        self.button.pack(padx=100, pady=10)
        self.output_text=tk.StringVar()
        self.output=tk.Label(self.root,textvariable=self.output_text)
        self.output.pack()

        """styling"""
        self.root.config(background="#303030")
        self.label.config(font=("Arial",16),fg="white", bg="#303030")
        self.button.config(font=('Arial',14),fg="white", bg="#303030", activebackground="#303030")
        self.zaj.config(font=('Arial',14),fg="white", bg="#303030")
        self.safety.config(font=('Arial',14),fg="white", bg="#303030")
        self.output.config(background ="#303030", relief=FLAT,font=('Arial',14),fg="white")

        self.zajTooltip = CreateToolTip(self.zaj, \
       'A zaj a szimulációban a fotonok polarizációját újrasorsolja nem pedig megcseréli '
       'önmagának merőleges polarizációjúvá. Ezért 0-100%, helyett csak 0-50% között '
        'lehet változtatni a zajt, mivel 50-100% között ugyan az a változás történik '
        'mint 0-50% között csak fordítva.')

        self.root.mainloop()
    
    def szimulacio(self):
        file=open("B92 Ideális Kulcs.txt","a")
        """Beállítások"""
        KulcsMin=1000 #küldött bitek mennyiségnek minimuma
        KulcsMax=10000 #küldött bitek mennyiségnek minimuma
        KulcsLepes=100 #biztonság fügvényében változik (nagyobb safety kisebb lépés
        #pontosabbb ideális kulcshossz érték
        EveMerMin=10 #Eva minimum mérési aránya
        EveMerMax=110
        EveMerLepes=10
        sampleSize=0.15 #szimulációs adatokból vett érték
        noise=float(self.zaj.get()/50)
        biztonsag=int(self.safety.get())
        smallKeys=[]
        smallestKey=[]

        for eveSpying in range(EveMerMin,EveMerMax,EveMerLepes):
            for keyLength in range(KulcsMin,KulcsMax,KulcsLepes):
                """Beállítások"""
                talaltHiba=0 #ennyi eltérést talált bob és anna
                keyAlice=[] #Alice kulcsa
                keyBob=[] #Bob álltal megkapott bitek
                AliceNewKey=[] #Alice álltal megtartott bitek
                vartHiba=keyLength*sampleSize*noise
                
                """Alice kulcsának generálása"""
                for i in range(keyLength):
                    keyAlice.append(round(random.random()))

                """Kommunikáció"""
                #hiba zaj miatt
                def noiseError():
                    self.zajosBit+=1
                    if(keyAlice[i]==0):
                        keyBob.append(1)
                    else:
                        keyBob.append(0)

                #csak Alice és Bob vesz részt a kommunikációban
                def onlyAB():
                        bobMeasure=round(random.random())
                        if (bobMeasure==keyAlice[i])&(round(random.random())==1):
                            if(random.random()>noise):#zaj
                                keyBob.append(bobMeasure)
                            else:
                                noiseError()
                            AliceNewKey.append(keyAlice[i])

                for i in range(keyLength):
                    #ha eve nem hallgatózik bob a várt értékeket méri
                    if(eveSpying<random.random()*100):
                        onlyAB()
                    else:
                        eveMeasure=round(random.random())
                        if (eveMeasure==keyAlice[i])&(round(random.random())==1):#eve sikeres
                            onlyAB()#jól mért -> olyan mintha Alice üzenne
                        else:#eve sikertelenül mér
                            if(random.random()>0.333333):#ha eve jó polarizációban küldi a bitet
                                onlyAB()
                                    #eve rossz pol. választ
                            elif((round(random.random())==1)&(round(random.random())==1)):#bob jól méri a rossz bitet
                                if(random.random()>noise):#zaj
                                    if(keyAlice[i]==0):#bob felírja a mért bitet és szól A-nek, hogy mért
                                        keyBob.append(1)#ami nem lehetett volna lehetséges így 2 különböző bitet írnak fel
                                        AliceNewKey.append(0)
                                    else:
                                        keyBob.append(0)
                                        AliceNewKey.append(1)
                                else:
                                    keyBob.append(keyAlice[i])
                                    AliceNewKey.append(keyAlice[i])

                """ellenőrzés"""
                #Alice és Bob ellenörzi a kulcs egy részét majd kidobják amiket publikusan ellenőriztek
                for i in range(int(sampleSize*keyLength)):
                    bitEllen=random.randrange(0,len(AliceNewKey))
                    if (AliceNewKey[bitEllen]!=keyBob[bitEllen]):
                        talaltHiba+=1
                    AliceNewKey.pop(bitEllen)
                    keyBob.pop(bitEllen)
                """Adatok kiírása"""
                #print(self.zajosBit, talaltHiba-vartHiba, talaltHiba, vartHiba, keyLength)
                file.write(str(talaltHiba-vartHiba))
                file.write('\n')
                if(talaltHiba-vartHiba>100):
                    #print(keyLength)
                    smallKeys.append(keyLength)
            if(smallKeys):
                smallestKey.append(min(smallKeys))
        nemIdealis=True
        while(nemIdealis):
            if(len(smallestKey)>biztonsag):
                self.output_text.set("Az ideális kulcshossz: "+str(smallestKey[biztonsag]))
                nemIdealis=False
            else:
                biztonsag-=1
                if biztonsag==0:
                    self.output_text.set("Az ideális kulcshossz: 10000+ \n Kérem csökkentse a zaj szintjét \n vagy vállaljon nagyobb kockázatot.")
                    nemIdealis=False
                #print(talaltHiba-vartHiba)#eltérés darabszámra
                #print(round((talaltHiba-vartHiba)/(keyLength*sampleSize)*100,3))#százalékos eltérés
                #kulcshossz növelése (ciklus 1)
                #eve mérési gyakoriságának növelése ciklus(2)


        #zaj=input("adj zajnak a szintjet") #mekkora a rendszerben a zaj (0-20)
        #safety=input("bizt") #mennyira akarja, hogy észrevegye, hogy lehalgassák

        #becsles szimul hosszárol
        #meghívom a szimulaciot
        #szimulacio(zaj,safety)

        #print idealis kulcshossz x safety
        #adatok kiírni
        file.close()

GUI()
