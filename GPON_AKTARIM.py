#######################################################################################################################
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
########################################################################################################################
from dosya_rc import *
import os
from datetime import datetime
#######################################################################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("untitled.ui", self)
        self.pushButton.clicked.connect(self.result)
        self.pushButton_3.clicked.connect(self.clear)
        self.pushButton_2.clicked.connect(self.pss587)
        self.pushButton_4.clicked.connect(self.clear1)
        self.pushButton_5.clicked.connect(self.result2)
        self.pushButton_6.clicked.connect(self.clear2)
        self.pushButton_7.clicked.connect(self.pss71)
        self.pushButton_8.clicked.connect(self.clear3)
        self.pushButton_9.clicked.connect(self.help)
        self.setFixedSize(610, 642)
        self.result1 = None
        self.pss = None
        self.result2 = None

    def result(self):
       file_path, _ = QFileDialog.getOpenFileName(self, "Open Result_callgroup file", os.path.expanduser("~"),"Result_callgroup files (*.txt)")
       self.lineEdit.setText(file_path)
       self.result1=file_path

    def pss587(self):
       file_path1, _ = QFileDialog.getOpenFileName(self, "Open 587_PSS_CALLGRP_PSI file", os.path.expanduser("~"),"587_PSS_CALLGRP_PSI files (*.txt)")
       self.lineEdit_2.setText(file_path1)

       with open(file_path1) as f1, open(self.result1) as f2:
           dict1 = {}
           set2 = set()

           # İlk dosyadaki verileri dictionary'e ekle
           for satir in f1:
               satir = satir.replace("x80", "")
               veriler = satir.split(",")
               tel = veriler[0].replace("tel:", "").replace("'", "")
               grpno = veriler[1].replace("'", "")
               dict1[tel] = grpno

           # İkinci dosyadaki verileri set2'ye ekle
           for satir in f2:
               satir = satir.replace("tel:", "")
               if not satir.startswith('+'):
                   satir = '+' + satir
               tel = satir.strip().replace("'", "")
               set2.add(tel)

           # setler arasındaki kesişimi bul
           kesisim = set(dict1.keys()).intersection(set2)

           f = open("callgrppsi_output.txt", "a")
           f.write('\n--------------------------------------------------\n')
           f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
           f.close()

           # Kesişimi ekrana yazdır
           print("\n")
           for tel in kesisim:
               grpno = dict1[tel]  # dictionary kullanarak ilgili tel değerine ait grpno değerini alın
               f = open("callgrppsi_output.txt", "a")
               f.write("\n"f'ADD CALLGRPPSI:PSI="tel:{tel}",GRPNO="{grpno}";')
               f.close()
           QMessageBox.information(self, "Successful", "The file was created (CALL_GROUP_PSI_OUTPUT)")

    def result2(self):
        file_path2, _ = QFileDialog.getOpenFileName(self, "Open Result_callgroup file", os.path.expanduser("~"),"Result_callgroup files (*.txt)")
        self.lineEdit_3.setText(file_path2)
        self.result2 = file_path2

    def pss71(self):
        file_path3, _ = QFileDialog.getOpenFileName(self, "Open 71_PSS_CALLGRP file", os.path.expanduser("~"),"71_PSS_CALLGRP files (*.txt)")
        self.lineEdit_4.setText(file_path3)
        ##################################################################################################################
        selmode_macros = {
            "1": "SEQS",
            "2": "TOPPRI",
            "3": "NEAPPRI",
            "4": "IDIE",
            "6": "TSS",
            "7": "TRS",
            "8": "TLS",
            "9": "TPS",
        }

        DISPILOT_macros = {
            "1": "YES",
            "0": "NO",
        }

        NONPILOT_macros = {
            "1": "YES",
            "0": "NO",
        }
        NONPILSELMOD_macros = {
            "0": "NORMAL",
            "1": "CNFIRST",
            "2": "PMFIRST",

        }

        CHARGPILOT_macros = {
            "1": "YES",
            "0": "NO",
        }

        TRIGSPECFORWARD_macros = {
            1: "YES",
            0: "NO",
        }
        ############################################################################################################

        with open(file_path3) as f1, open(self.result2) as f2:
            dict1 = {}
            set2 = set()
            for satir in f1:
                satir = satir.replace("x80", "")
                veriler = satir.split(",")
                grpno = veriler[0].replace("'", "")
                selmode = veriler[1].replace("'", "")
                Maxnum = veriler[2].replace("'", "")
                DISPLOT = veriler[3].replace("'", "")
                NAME = veriler[4].replace("tel:", "").replace("'", "")
                CALLIN = veriler[5].replace("'", "")
                CALLOUT = veriler[6].replace("'", "")
                NONPILOT = veriler[8].replace("'", "")
                NONPILSELMOD = veriler[9].replace("'", "")
                CHARGPILOT = veriler[10].replace("'", "")
                MAXRINGNUM = veriler[12].replace("'", "")
                CALLERQUEUE = veriler[13].replace("'", "")
                VIRNUMBER = veriler[14].replace("'", "")
                TRIGSPECFORWARD = veriler[15].replace("'", "")
                if not NAME.startswith('+'):
                    NAME = '+' + NAME
                dict1[NAME] = (grpno, selmode, Maxnum, DISPLOT, NONPILOT, MAXRINGNUM, NONPILSELMOD, CHARGPILOT, TRIGSPECFORWARD)


            for satir in f2:
                satir = satir.replace("tel:", "")
                if not satir.startswith('+'):
                    satir = '+' + satir
                NAME = satir.strip().replace("'", "")
                set2.add(NAME)

            kesisim = set(dict1.keys()).intersection(set2)
            f = open("callgroup_cmd_output.txt", "a")
            f.write('\n--------------------------------------------------------------------------------------------------\n')
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.close()
            # Kesişimi ekrana yazdır
            print("\n")
            for NAME in kesisim:
                grpno, selmode, Maxnum, DISPILOT, NONPILOT, MAXRINGNUM, NONPILSELMOD, CHARGPILOT, TRIGSPECFORWARD = \
                dict1[NAME]  # dictionary kullanarak ilgili tel değerine ait grpno değerini alın
                selmode_str = selmode_macros.get(selmode, "Unknown")
                DISPILOT_str = DISPILOT_macros.get(DISPILOT, "Unknown")
                NONPILOT_str = NONPILOT_macros.get(NONPILOT, "Unknown")
                NONPILSELMOD_str = NONPILSELMOD_macros.get(NONPILSELMOD, "Unknown")
                CHARGPILOT_str = CHARGPILOT_macros.get(CHARGPILOT, "Unknown")
                TRIGSPECFORWARD_int = TRIGSPECFORWARD_macros.get(int(TRIGSPECFORWARD), "Unknown")
                f = open("callgroup_cmd_output.txt", "a")
                f.write("\n"f'ADD CALLGROUP:GRPNO="{grpno}",NAME="{NAME}",SELMODE="{selmode_str}",MAXNUM="{Maxnum}",MAXRINGNUM={MAXRINGNUM},DISPILOT="{DISPILOT_str}",NONPILOT="{NONPILOT_str}",NONPILSELMOD="{NONPILSELMOD_str}",CHARGPILOT="{CHARGPILOT_str}",TRIGSPECFORWARD="{TRIGSPECFORWARD_int}";')
                f.close()
            QMessageBox.information(self, "Successful", "The file was created (CALL_GROUP_CMD_OUTPUT)")

    def help(self):
        QMessageBox.information(self, "Information", "After determining the output you want to create, start the process by selecting the Result_callgroup file. Don't forget to show the path of all files correctly!.")

    def clear(self):
       self.lineEdit.clear()

    def clear1(self):
       self.lineEdit_2.clear()

    def clear2(self):
       self.lineEdit_3.clear()

    def clear3(self):
       self.lineEdit_4.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow() 
    mainWindow.show()
    sys.exit(app.exec_())
