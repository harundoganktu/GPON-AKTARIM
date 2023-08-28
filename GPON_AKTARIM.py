#######################################################################################################################
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
########################################################################################################################
from dosya_rc import *
import os
from datetime import datetime
import re
#######################################################################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gpon.ui", self)
        self.setFixedSize(610, 642)
        self.pushButton_2.clicked.connect(self.pss587)
        self.pushButton_4.clicked.connect(self.clear1)
        self.comboBox.activated[str].connect(self.combo)
        self.pushButton_7.clicked.connect(self.pss71)
        self.pushButton_8.clicked.connect(self.clear3)
        self.pushButton_9.clicked.connect(self.create)
        self.pushButton.clicked.connect(self.difference)
        self.value = None
        self.pss = None
        self.pss71f = None
        self.grpno = None

    def combo(self, text):
        match = re.search(r'\((.*?)\)', text)
        if match:
            self.value = match.group(1)
            print(self.value)

    def pss587(self):
        file_path1, _ = QFileDialog.getOpenFileName(self, "Open 587_PSS_CALLGRP_PSI file", os.path.expanduser("~"),"587_PSS_CALLGRP_PSI files (*.txt)")
        self.lineEdit_2.setText(file_path1)
        self.pss = file_path1

    def pss71(self):
        file_path3, _ = QFileDialog.getOpenFileName(self, "Open 71_PSS_CALLGRP file", os.path.expanduser("~"), "71_PSS_CALLGRP files (*.txt)")
        self.lineEdit_4.setText(file_path3)
        self.pss71 = file_path3

    def create(self):
        with open(self.pss) as f1:
            dict1 = {}
            f = open("call_grp_psi_output.txt", "a")
            f.write('\n--------------------------------------------------\n')
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.close()
            for satir in f1:
                satir = satir.replace("x80", "")
                veriler = satir.split(",")
                tel = veriler[0].replace("tel:", "").replace("'", "")
                self.grpno = veriler[1].replace("'", "")
                print(f'"tel:{tel}",Grpno={self.grpno}";')
                if not tel.startswith('+'):
                    tel = '+' + tel
                digitler1 = tel[3:6]
                if self.value == digitler1:
                    with open("587.csv", "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([{tel}])
                    dict1[tel] = self.grpno
                    #telekom = tel.replace("+90", "")
                    #print(telekom)
                    f = open("call_grp_psi_output.txt", "a")
                    f.write("\n"f'ADD CALLGRPPSI:PSI="tel:{tel}",GRPNO="{self.grpno}";')
                    f.close()
            print()
            print("71_PSS_CALLGRP")
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

        with open(self.pss71) as f2:
            dict2 = {}
            f = open("call_group_cmd_output.txt", "a")
            f.write('\n--------------------------------------------------------------------------------------------------\n')
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.close()
            for satir in f2:
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
                NAME = NAME.replace("Tel:", "")
                NAME = NAME.replace("tel", "")
                NAME = NAME.replace("sip:", "")
                NAME = NAME.replace("el:", "")
                if not NAME.startswith('+'):
                    NAME = '+' + NAME
                digitler2 = NAME[3:6]
                if self.value == digitler2:
                    with open("71.csv", "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([{NAME}])
                    dict2[NAME] = (grpno, selmode, Maxnum, DISPLOT, NONPILOT, MAXRINGNUM, NONPILSELMOD, CHARGPILOT, TRIGSPECFORWARD)
                    grpno, selmode, Maxnum, DISPILOT, NONPILOT, MAXRINGNUM, NONPILSELMOD, CHARGPILOT, TRIGSPECFORWARD = dict2[NAME]
                    selmode_str = selmode_macros.get(selmode, "Unknown")
                    DISPILOT_str = DISPILOT_macros.get(DISPILOT, "Unknown")
                    NONPILOT_str = NONPILOT_macros.get(NONPILOT, "Unknown")
                    NONPILSELMOD_str = NONPILSELMOD_macros.get(NONPILSELMOD, "Unknown")
                    CHARGPILOT_str = CHARGPILOT_macros.get(CHARGPILOT, "Unknown")
                    TRIGSPECFORWARD_int = TRIGSPECFORWARD_macros.get(int(TRIGSPECFORWARD), "Unknown")
                    #telekom1 = NAME.replace("+90", "")
                    # print(telekom1)
                    f = open("call_group_cmd_output.txt", "a")
                    f.write("\n"f'ADD CALLGROUP:GRPNO="{grpno}",NAME="{NAME}",SELMODE="{selmode_str}",MAXNUM="{Maxnum}",MAXRINGNUM={MAXRINGNUM},DISPILOT="{DISPILOT_str}",NONPILOT="{NONPILOT_str}",NONPILSELMOD="{NONPILSELMOD_str}",CHARGPILOT="{CHARGPILOT_str}",TRIGSPECFORWARD="{TRIGSPECFORWARD_int}";')
                    f.close()
        QMessageBox.information(self, "Successful", "The outputs were created in the application directory")

    def difference(self):
        print()
        def compare_csv(file1, file2):
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                reader1 = csv.reader(f1)
                reader2 = csv.reader(f2)

                rows1 = list(reader1)
                rows2 = list(reader2)

                # A -> B karşılaştırması
                print("587 -> 71 farklılıkları:")
                for i, row in enumerate(rows1):
                    if row and row not in rows2:
                        print(f"Satır {i + 1}: {row}")

                # B -> A karşılaştırması
                print("71 -> 587 farklılıkları:")
                for i, row in enumerate(rows2):
                    if row and row not in rows1:
                        print(f"Satır {i + 1}: {row}")

        # Dosya isimlerini ve yolunu ayarlayın
        file_a = "587.csv"
        file_b = "71.csv"
        compare_csv(file_a, file_b)
    def clear1(self):
       self.lineEdit_2.clear()

    def clear3(self):
       self.lineEdit_4.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()  # veya mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.show()
    sys.exit(app.exec_())

