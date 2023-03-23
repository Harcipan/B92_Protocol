import tkinter as tk
from tkinter import *
import random #python random module

class CreateToolTip(object):
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
        self.root=tk.Tk()
        self.zajosBit=0
        self.photo = PhotoImage(file = "b92.ico")
        self.root.iconphoto(False, self.photo)

        self.root.title("B92 Ideális kulcs")
        self.root.geometry("1000x900")

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        
        self.label=tk.Label(self.root, text="Beállítások")
        self.label.grid(padx=20,pady=20, column=0,row=0,)
        
        self.keyLength = Scale(self.root, from_=500, to=10000,tickinterval=9500, length=200, orient=HORIZONTAL, label="Kulcshossz")
        self.keyLength.grid(column=0,row=1,sticky="we")
        self.keyLength.set(5000)
        self.eveSpying = Scale(self.root, from_=0, to=100,tickinterval=100, length=200, orient=HORIZONTAL , label="Eve támadásának frekvenciája")
        self.eveSpying.grid(column=0,row=2,sticky="we")
        self.eveSpying.set(10)
        self.sampleSize = Scale(self.root, from_=100, to=2000,tickinterval=1900, length=200, orient=HORIZONTAL, label="Ellenőrizendő bitek száma")
        self.sampleSize.grid(column=1,row=1,sticky="we")
        self.sampleSize.set(1000)
        self.zaj = Scale(self.root, from_=0, to=50,tickinterval=50, length=200, orient=HORIZONTAL , label="Zaj")
        self.zaj.grid(column=1,row=2,sticky="we")
        self.zaj.set(10)
        
        self.button=tk.Button(self.root, text="Start", command = self.szimulacio)
        self.button.grid(padx=100, pady=10,column=1,row=0)
        self.output=tk.Text(self.root, state='disabled', width=50)
        self.output.grid()

        """styling"""
        self.root.config(background="#303030")
        self.label.config(font=("Arial",16),fg="white", bg="#303030")
        self.button.config(font=('Arial',14),fg="white", bg="#303030", activebackground="#303030")
        self.keyLength.config(font=('Arial',14),fg="white", bg="#303030")
        self.eveSpying.config(font=('Arial',14),fg="white", bg="#303030")
        self.sampleSize.config(font=('Arial',14),fg="white", bg="#303030")
        self.zaj.config(font=('Arial',14),fg="white", bg="#303030")
        self.output.config(background ="#303030", relief=SUNKEN,font=('Arial',14),fg="white",)

        """Tooltips"""
        self.zajTooltip = CreateToolTip(self.zaj, \
       'A zaj a szimulációban a fotonok polarizációját újrasorsolja nem pedig megcseréli '
       'önmagának merőleges polarizációjúvá. Ezért 0-100%, helyett csak 0-50% között '
        'lehet változtatni a zajt, mivel 50-100% között ugyan az a változás történik '
        'mint 0-50% között csak fordítva.')

        self.root.mainloop()
    
    def szimulacio(self):
        #choice=input("Szeretné a programot egyéni beállításokkal futtatni? (y/n)")

        """Beállítások"""

        keyLength=int(self.keyLength.get())
        keyAlice=[] #Alice kulcsa
        keyBob=[] #Bob álltal megkapott bitek
        AliceNewKey=[] #Alice álltal megtartott bitek
        keyEve=[] #Eve mért bitei
        eveSpying=float(self.eveSpying.get()/100) #Eve mennyiszer halgat bele a kulcsba 0=soha, 1=mindig
        noise=float(self.zaj.get()/100) #mekkora valószinűséggel változik jelentősen a foton pol.
        sampleSize=int(self.sampleSize.get()) #ellenőrzött bitek hossza (akár lehet input is a felh.-tól)
        runAmm=1
        minErtek=1
        maxErtek=1
        lepes=1
        beall=1
        hibasBit=0
        osszHiba=0
        eveNincs=0

        """Szimuláció"""

        print("'kulcshossz', 'Eve támadásának frekvenciája', 'zaj', 'ellenőrzött bitek', 'talált hibák átlaga'")
        if(lepes<1):
            loopLepes=int((1/lepes)*lepes)
            maxErtek=int((1/lepes)*maxErtek)
        else:
            loopLepes=int(lepes)

        if(maxErtek<1):
            maxErtek=int((1/lepes)*maxErtek)
        if(minErtek<1):
            minErtek=int((1/lepes)*minErtek)

        for p in range(minErtek,maxErtek+loopLepes,loopLepes):
            for k in range(0,runAmm):

                
                """Alice kulcsának generálása"""


                for i in range(keyLength):
                    keyAlice.append(round(random.random()))
                if(runAmm==1):
                    print("Alice generált kulcsa:")
                    print(keyAlice)

                    
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
                    if(eveSpying<random.random()):
                        eveNincs+=1
                        onlyAB()
                    else:
                        eveMeasure=round(random.random())
                        if (eveMeasure==keyAlice[i])&(round(random.random())==1):#eve sikeres
                            keyEve.append(eveMeasure)#eve felírja a mért bitet
                            #jól mért -> olyan mintha Alice üzenne
                            onlyAB()
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
                if(runAmm==1):
                    self.output.config(state="normal")
                    self.output.insert(INSERT,"Alice megtartott bitjei:\n"+str(AliceNewKey)+"\n"f"Alice kulcsának hossza: {len(AliceNewKey)}\n")
                    self.output.insert(INSERT,"Bob mért bitjei:\n"+str(keyBob)+"\n"f"Bob kulcsának hossza: {len(keyBob)}\n")
                    self.output.insert(INSERT,"Eve mért bitjei:\n"+str(keyEve)+"\n"f"Eve kulcsának hossza: {len(keyEve)}\n")
                    self.output.grid()
                    self.output.config(state="disabled")
                    print("Alice megtartott bitjei:")
                    print(AliceNewKey)
                    print(f"Alice kulcsának hossza: {len(AliceNewKey)}")
                    print("Bob mért bitjei")
                    print(keyBob)
                    print(f"Bob kulcsának hossza: {len(keyBob)}")
                    print("Eve mért bitjei:")
                    print(keyEve)
                    print(f"Eve kulcsának hossza: {len(keyEve)}")


                #Ellenőrzés
                ABC=len(AliceNewKey) #Alice Before Controll
                #elég hosszú-e a kulcs
                if(len(keyBob)<=sampleSize):
                    print("Kulcs nem elég hosszú")
                    """(+) lehetőség, hogy még küldjön biteket"""

                #Alice és Bob ellenörzi a kulcs egy részét majd kidobják amiket publikusan ellenőriztek
                bitEllen=0
                for i in range(sampleSize):
                    if(len(AliceNewKey)>0):
                        bitEllen=random.randrange(0,len(AliceNewKey))
                    if (AliceNewKey[bitEllen]!=keyBob[bitEllen]):
                        hibasBit+=1
                        #print("Hiba Alice és Bob kulcsa nem egyezik")
                    AliceNewKey.pop(bitEllen)
                    keyBob.pop(bitEllen)
                if(runAmm==1):
                    self.output.config(state="normal")
                    self.output.insert(INSERT,"Alice végső Kulcsa:\n"+str(AliceNewKey)+"\n"f"Alice végső kulcsának hossza: {len(AliceNewKey)}\n")
                    self.output.insert(INSERT,"Bob végső Kulcsa:\n"+str(keyBob)+"\n"f"Bob kulcsának hossza: {len(keyBob)}\n")
                    self.output.insert(INSERT,f"Zaj álltal okozott összes hiba: {self.zajosBit} (várt összes:{keyLength*noise})\n")
                    self.output.insert(INSERT,f"Zaj álltal okozott összes várt hiba: {round(ABC*noise,2)}\n")
                    self.output.insert(INSERT,f"A várt hiba zaj miatt: {round(sampleSize*noise,2)}\n")
                    self.output.insert(INSERT,f"A várt hiba Eve miatt: {sampleSize*0.25*eveSpying}\n")
                    self.output.insert(INSERT,f"A várt hiba Eve miatt: {sampleSize*0.25*eveSpying}\n")
                    self.output.grid()
                    self.output.config(state="disabled")
                    print("Alice végső Kulcsa:")
                    print(AliceNewKey)
                    print("Bob végső Kulcsa:")
                    print(keyBob)
                    print('\n')
                    print(f"Zaj álltal okozott összes hiba: {self.zajosBit} (várt összes:{keyLength*noise})")
                    print(f"Zaj álltal okozott összes várt hiba: {round(ABC*noise,2)}")
                    print(f"A várt hiba zaj miatt: {round(sampleSize*noise,2)}")
                    print(f"A várt hiba Eve miatt: {sampleSize*0.25*eveSpying}")
                    print('\n')
                    if(hibasBit==0):
                        self.output.config(state="normal")
                        self.output.insert(INSERT,"Alice és Bob sikeresen birtokolják ugyan azt a kulcsot\n")
                        self.output.grid()
                        self.output.config(state="disabled")
                        print("Alice és Bob sikeresen birtokolják ugyan azt a kulcsot")
                    else:
                        self.output.config(state="normal")
                        self.output.insert(INSERT,f"Alice és Bob {hibasBit} db hibát talált\n")
                        self.output.insert(INSERT,f"Eve {eveNincs} bitbe nem hallgatott bele")
                        self.output.grid()
                        self.output.config(state="disabled")
                        print(f"Alice és Bob {hibasBit} db hibát talált")
                        print(f"Eve {eveNincs} bitbe nem hallgatott bele")
                osszHiba+=hibasBit
                hibasBit=0

            if(runAmm>1):
                if(kiIras=="f"):
                    f = open("B92_Adatok.txt", "a")
                    k=[keyLength, round(eveSpying,2), round(noise,2), sampleSize, round(osszHiba/runAmm,2)]
                    for i in range(len(k)):
                        f.write(str(k[i]))
                        if(i<len(k)-1):
                            f.write(" ")
                    f.write('\n')
                    f.close()
                    print("processing...")
                else:
                    print(keyLength, round(eveSpying,2), round(noise,2), sampleSize, round(osszHiba/runAmm,2))
                if(beall==1):
                    keyLength+=int(lepes)
                elif(beall==2):
                    eveSpying+=lepes
                elif(beall==3):
                    noise+=lepes
                elif(beall==4):
                    sampleSize+=int(lepes)

            """Tisztítás következő futtatás elött"""

            
            osszHiba=0
            keyAlice=[]
            keyBob=[]
            AliceNewKey=[]
            keyEve=[]


GUI()
