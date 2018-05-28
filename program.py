import MySQLdb
import numpy
import math
import sys
numpy.set_printoptions(threshold=numpy.nan)
from scipy.stats.stats import pearsonr

   
# konek ke db
#db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="",db = "tugasakhir")
#cursor = db.cursor()

# cara insert data ke db
#cursor.execute("INSERT INTO kata (kata, sense) VALUES ('kadekA', 1)")
#db.commit()

# cara select data ke db
#cursor.execute("SELECT * FROM kata")
#results = cursor.fetchall()
#for row in results:
#    print(row)

# fungsi mencari nilai bobot
def cariKata(stringList, toMatch, windowSize):
    before = windowSize
    after = windowSize
    result = []
    
    sb = []
    for x in range(len(stringList)) :
        if (toMatch == stringList[x]) :
            index = x
            if (index == 0) :
                titik = index
                titikKanan = index + after
                while titik <= titikKanan :
                    sb.append(stringList[titik])
                    titik = titik + 1
                result = sb
                
            elif (index == len(stringList)-1) :
                titik = index
                titikKiri = index - before
                while titik >= titikKiri :
                    sb.append(stringList[titikKiri])
                    titikKiri = titikKiri + 1
                result = sb
                
            elif (index > 0) and (index < len(stringList)-1) :
                titik = index
                titikKiri = index - before
                titikKanan = index + before
                
                if(titikKiri >= 0):
                    while titikKiri <= titik:
                        sb.append(stringList[titikKiri])
                        titikKiri = titikKiri + 1
                    if(titikKanan <= len(stringList)-1):
                        titik = titik + 1
                        while titikKanan >= titik:
                            sb.append(stringList[titik])
                            titik = titik + 1
                    elif(titikKanan > len(stringList)-1):
                        titik = titik + 1
                        titikKanan = len(stringList)-1
                        while titikKanan >= titik:
                            sb.append(stringList[titik])
                            titik = titik + 1
                            
                if(titikKiri < 0):
                    titikKiri = 0
                    while titikKiri <= titik:
                        sb.append(stringList[titikKiri])
                        titikKiri = titikKiri + 1
                    if(titikKanan <= len(stringList)-1):
                        titik = titik + 1
                        while titikKanan >= titik:
                            sb.append(stringList[titik])
                            titik = titik + 1
                    elif(titikKanan > len(stringList)-1):
                        titik = titik + 1
                        titikKanan = len(stringList)-1
                        while titikKanan >= titik:
                            sb.append(stringList[titik])
                            titik = titik + 1
                
                result = sb
    return result

def termFreq(stringList,cari):
    result = 0
    for x in range(len(stringList)):
        if(stringList[x] == cari):
            result = result + 1
    return result

def hitungPMIMax(stringList, matrixAkhir, totalKataUnik, kata1, kata2):
    result = 0
    
    fdW1W2 = 0
    ek = 10
    yw1 = 0
    yw2 = 0
    p = 7.5
    q = 10
    n = len(stringList)
    fw1 = termFreq(stringList,kata1)
    fw2 = termFreq(stringList,kata2)
    
    #print("kata 1 : ",kata1)
    #print("kata 2 : ",kata2)
    
    for i in range(1,totalKataUnik+1):
        if(kata1 == matrixAkhir[i][0]):
            for j in range(1,totalKataUnik+1):
                if(kata2 == matrixAkhir[0][j]):
                    fdW1W2 = matrixAkhir[i][j]
                    #print("Coocurence : ",fdW1W2)
                    yw1 = (math.pow((math.log(fw1))+q,p))/(math.pow((math.log(700))+q,p))
                    yw2 = (math.pow((math.log(fw2))+q,p))/(math.pow((math.log(700))+q,p))
                    result2 = ((fdW1W2-((ek/n)*(fw1*fw2-(fw1/yw1)*(fw2/yw2))))*n)/((fw1/yw1)*(fw2/yw2))
                    if(result2<= 0):
                        result = 0;
                    else:
                        result = math.log(result2)
                    #print("yw1 : ",yw1)
                    #print("yw2 : ",yw2)
                    #print("Nilai PMIMax : ",result)
                    #print("n : ",n)
                    #print("fw1 : ",fw1)
                    #print("fw2 : ",fw2)
    return result

# main program
def main():
    
    # baca file corpus hasil preprocessing
    print("1. Baca Corpus Hasil Preprocessing")
    fileCorpus = open("hasilPreprocessing5.txt", "r") 
    stringList = fileCorpus.read().strip().split(" ")
    stringList = list(filter(("").__ne__, stringList))
    
    # membuat list kata untuk matrix bobot dari file corpus hasil preprocessing
    print("2. Membuat List Kata Marix dari Corpus")
    stringListMatrix = list(set(stringList))
    stringListMatrix.sort()
    totalKataUnik = len(stringListMatrix)
    s = (totalKataUnik + 2, totalKataUnik + 2)
    
    # membuat inisialisasi matrix
    print("3. Inisialisasi Pembentukan Matrix")
    matrixAkhir = numpy.zeros(s, dtype = object)
    for x in range(totalKataUnik) :
        matrixAkhir[0][x+1] = stringListMatrix[x]
        matrixAkhir[x+1][0] = stringListMatrix[x]
    numpy.savetxt('matrixAkhir.csv', matrixAkhir, delimiter=',', fmt='%s')
    
    # hitung bobot
    print("4. Proses Penghitungan Bobot")
    windowSize = 5
    for x in range(totalKataUnik):
        context1 = cariKata(stringList,stringListMatrix[x],windowSize)
        for y in range(totalKataUnik):
            bobot = 0
            for k in range(len(context1)):
                if(stringListMatrix[y] == context1[k]):
                    bobot = bobot + 1
                    matrixAkhir[x+1][y+1] = bobot
    
    # simpan nilai bobot ke file matrixAjkhir
    print("5. Simpan Hasil Penghitungan Bobot")
    numpy.savetxt('matrixAkhir.csv', matrixAkhir, delimiter=',', fmt='%s')
    
    fileHasilKorelasi = open("hasilKorelasi.txt", "w")
    
    for x in range(3):
        x = x + 1
        print("+. Baca Gold Standar ",x)
        goldstandartext = "goldstandar",str(x),".txt"
        fileGoldStandar1 = open(''.join(goldstandartext), "r") 
        listGoldStandar1 = fileGoldStandar1.read().strip().split("\n")
        
        print("+. Cari dan Simpan Nilai PMI Max dari Corpus yang ada di Gold Standar ",x)
        arrayNilaiGoldStandar = []
        arrayNilaiPMIMax = []
        goldstandartext = "hasilPMIGoldStandar",str(x),".csv"
        hasilPMIGoldStandar1 = open(''.join(goldstandartext), "w")
        for i in range(len(listGoldStandar1)):
            listKataGoldStandar = listGoldStandar1[i].split(",")
            nilaiPMIMax = hitungPMIMax(stringList, matrixAkhir, totalKataUnik, listKataGoldStandar[0], listKataGoldStandar[1])
            arrayNilaiGoldStandar.append(float(listKataGoldStandar[2]))
            arrayNilaiPMIMax.append(nilaiPMIMax)
            kataDanPMI = listKataGoldStandar[0],",",listKataGoldStandar[1],",",str(nilaiPMIMax),"\n"
            hasilPMIGoldStandar1.write(''.join(kataDanPMI))
        hasilPMIGoldStandar1.close()
        
        print("+. Hitung dan Simpan Nilai Korelasi Dari Gold Standar ",x)
        nilaiKorelasi = pearsonr(arrayNilaiGoldStandar,arrayNilaiPMIMax)[0] 
        kataDanKorelasi = "nilai korelasi korpus dengan gold standar ",str(x)," : ",str(nilaiKorelasi),"\n"
        fileHasilKorelasi.write(''.join(kataDanKorelasi))
    
    fileHasilKorelasi.close()
    
    return

# jalankan main program
main()