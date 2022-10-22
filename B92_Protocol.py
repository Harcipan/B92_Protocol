import random #python random module

choice=input("Szeretné a programot egyéni beállításokkal futtatni? (y/n)")

"""Beállítások"""

keyLength=10000
keyAlice=[] #Alice kulcsa
keyBob=[] #Bob álltal megkapott bitek
AliceNewKey=[] #Alice álltal megtartott bitek
keyEve=[] #Eve mért bitei
eveSpying=0.5 #Eve mennyiszer halgat bele a kulcsba 0=soha, 1=mindig
noise=0 #mekkora valószinűséggel változik jelentősen a foton pol.
sampleSize=1000 #ellenőrzött bitek hossza (akár lehet input is a felh.-tól)
zajosBit=0
runAmm=1
minErtek=1
maxErtek=1
lepes=1
beall=1
hibasBit=0
osszHiba=0
eveNincs=0

if(choice=="y"):
    kiIras=input("A terminálba vagy txt file-ba írjam ki az adatokat? (t,f):")
    runAmm=int(input("Egy beállítás hányszor fusson:"))
    if runAmm==1:
        keyLength=int(input("Kulcs hossza:"))
        eveSpying=float(input("Eve hányszor hallgat bele az üzenetbe százalékosan(0-1):"))
        noise=float(input("Zaj mértéke (0-1):"))
        sampleSize=int(input("Ellenőrizendő bitek száma (ajánlott:<kulcs hossza/10):"))
    else:
        if(kiIras=="f"):
            f = open("B92_Adatok.txt", "w")
        print("(1:kulcshossz, 2:Eve támadásának frekvenciája, 3: zaj mértéke, 4: ellenőrizendő bitek száma)")
        beall=int(input("Minek a függvényében szeretné futtatni a szimulációt? (1,2,3,4):"))
        if(beall==1):
            minErtek=int(input("Kezdő kulcshossz:"))
            maxErtek=int(input("Végső kulcshossz:"))
            eveSpying=float(input("Eve hányszor hallgat bele az üzenetbe százalékosan(0-1):"))
            noise=float(input("Zaj mértéke (0-1):"))
            sampleSize=int(input("Ellenőrizendő bitek száma (ajánlott:<kulcs hossza/10):"))
            keyLength=minErtek
        if(beall==2):
            minErtek=float(input("Kezdő Eve frekvencia:"))
            maxErtek=float(input("Végső Eve frekvencia:"))
            keyLength=int(input("Kulcs hossza:"))
            noise=float(input("Zaj mértéke (0-1):"))
            sampleSize=int(input("Ellenőrizendő bitek száma (ajánlott:<kulcs hossza/10):"))
            eveSpying=minErtek
        if(beall==3):
            minErtek=float(input("Kezdő zaj:"))
            maxErtek=float(input("Végső zaj:"))
            keyLength=int(input("Kulcs hossza:"))
            eveSpying=float(input("Eve hányszor hallgat bele az üzenetbe százalékosan(0-1):"))
            sampleSize=int(input("Ellenőrizendő bitek száma (ajánlott:<kulcs hossza/10):"))
            noise=minErtek
        if(beall==4):
            minErtek=int(input("Kezdő ellenőrzés:"))
            maxErtek=int(input("Végső ellenőrzés:"))
            keyLength=int(input("Kulcs hossza:"))
            eveSpying=float(input("Eve hányszor hallgat bele az üzenetbe százalékosan(0-1):"))
            noise=float(input("Zaj mértéke (0-1):"))
            sampleSize=minErtek
        lepes=float(input("Mekkora lépésekkel növekedjen az érték:"))

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
            global zajosBit
            zajosBit+=1
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
            bitEllen=random.randrange(0,len(AliceNewKey))
            if (AliceNewKey[bitEllen]!=keyBob[bitEllen]):
                hibasBit+=1
                #print("Hiba Alice és Bob kulcsa nem egyezik")
            AliceNewKey.pop(bitEllen)
            keyBob.pop(bitEllen)
        if(runAmm==1):
            print("Alice végső Kulcsa:")
            print(AliceNewKey)
            print("Bob végső Kulcsa:")
            print(keyBob)
            print('\n')
            print(f"Zaj álltal okozott összes hiba: {zajosBit} (várt összes:{keyLength*noise})")
            print(f"Zaj álltal okozott összes várt hiba: {round(ABC*noise,2)}")
            print(f"A várt hiba zaj miatt: {round(sampleSize*noise,2)}")
            print(f"A várt hiba Eve miatt: {sampleSize*0.25*eveSpying}")
            print('\n')
            if(hibasBit==0):
                print("Alice és Bob sikeresen birtokolják ugyan azt a kulcsot")
            else:
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
