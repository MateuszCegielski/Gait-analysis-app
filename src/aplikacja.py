import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

from PyQt5.QtWidgets import QFileDialog
from gaitpy.gait import *

"""
Projekt 2 - analiza chodu autorzy Kacper Kilianek i Mateusz Cegielski 
Używany algorytm do analizy chodu GAITPY wymaga określenia pionowej osi, na podstawie pochodzących z niej wyników dokonuje analizy chodu
GAITPY wymaga do uruchomienia:
pythona w wersji 3.6
pandas >= 0.20.3
scipy >= 1.2.0
numpy >= 1.13.3
PyWavelets >= 0.5.2
scikit-learn == 0.21.3
statsmodels >= 0.8.0
bokeh >= 0.12.10
dill >= 0.2.7.1
deepdish >= 0.3.4
Zalecamy instalację podanych konkretnych wersji, nie wyższych, gdyż nam nie działał gaitpy gdy mieliśmy wyższe wersje pakietów
POLECAMY PRZETESTOWAĆ PROGRAM NA NASZYCH PLIKACH - np. dlugi.csv, najdluzszy.csv - tam osią pionową jest oś z
DODATKOWE oznaczenia legendy:
PFP - początek fazy podporu (i analogicznie koniec fazy wykroku)
PFW - początek fazy wykroku (i analogicznie koniec fazy podporu)
"""


"""
Tworzenie głownego okna, tworzenie i umiejscowienie przycisków, nadanie im parametrów 
"""


class Ui_MainWindow(object):
    def __init__(self):
        self.filepath = None
        self.dir = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1000)
        MainWindow.setFixedSize(1500, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1200, 900, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 171, 20))
        self.label.setObjectName("label")
        self.html = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.html.setGeometry(QtCore.QRect(10, 40, 1400, 800))
        self.html.setObjectName("html")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 21))
        self.menubar.setObjectName("menubar")
        self.menuPlik = QtWidgets.QMenu(self.menubar)
        self.menuPlik.setObjectName("menuPlik")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOtw_rz_plik = QtWidgets.QAction(MainWindow)
        self.actionOtw_rz_plik.setObjectName("actionOtw_rz_plik")
        self.actionWyjd = QtWidgets.QAction(MainWindow)
        self.actionWyjd.setObjectName("actionWyjd")
        self.menuPlik.addAction(self.actionOtw_rz_plik)
        self.menuPlik.addAction(self.actionWyjd)
        self.menubar.addAction(self.menuPlik.menuAction())
        # NOWE
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(30, 900, 121, 16))
        self.label3.setObjectName("label3")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(160, 900, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("x")
        self.comboBox.addItem("y")
        self.comboBox.addItem("z")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 900, 331, 16))
        self.label_2.setObjectName("label_2")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(580, 900, 91, 19))
        self.toolButton.setObjectName("toolButton")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aplikacja analizy chodu"))
        self.pushButton.setText(_translate("MainWindow", "Analizuj plik"))
        self.label.setText(_translate("MainWindow",
                                      "APLIKACJA ANALIZY CHODU - Wybierz plik .csv zawierający dane akcelerometryczne chodu do analizy oraz oś pionową, gdyż tego wymaga algorytm"))
        self.label.adjustSize()
        self.menuPlik.setTitle(_translate("MainWindow", "MENU"))
        self.actionOtw_rz_plik.setText(_translate("MainWindow", "Otwórz plik..."))
        self.actionWyjd.setText(_translate("MainWindow", "Wyjdź"))
        self.actionOtw_rz_plik.triggered.connect(lambda: self.openfile())
        self.actionWyjd.triggered.connect(lambda: sys.exit())
        self.pushButton.clicked.connect(lambda: self.analiza())
        # NOWE
        self.label3.setText(_translate("MainWindow", "Wybierz analizowaną oś:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "x"))
        self.comboBox.setItemText(1, _translate("MainWindow", "y"))
        self.comboBox.setItemText(2, _translate("MainWindow", "z"))
        self.label_2.setText(_translate("MainWindow", "Wybierz ścieżkę do której ma być zapisany wyjściowy plik HTML:"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.toolButton.clicked.connect(lambda: self.choosedir())

        """
        W tym miejscu, wybierana jest scieżka do danych .csv z danymi, które będą przetwarzane w kolejnej części 
        """

    def openfile(self):
        self.filepath = QFileDialog.getOpenFileName(directory=r'../logi', filter="*.csv")
        self.filepath = str(self.filepath)
        self.filepath = self.filepath[2:self.filepath.rfind("v") - 8]
        print(self.filepath)
        self.label.setText("Wybrałeś plik: " + self.filepath[self.filepath.rfind("/") + 1:self.filepath.rfind(
            "v") + 1] + " Wciśnij guzik Analizuj plik, by rozpocząć analizę.")
        self.label.adjustSize()

    """
    W tym miejscu w kodzie dochodzi do analizy 
    wczytanych danych i do wykreslenia charakterystyki chodu wraz z zaznaczeniem początka i końca poszczególnych faz chodu 
    
    """

    def analiza(self):
        if self.filepath is not None:
            raw_data = pd.read_csv(self.filepath, skiprows=1, names=['timestamps', 'x', 'y', 'z'], usecols=[0, 1, 2, 3])
            sample_rate = 50
            subject_height = 185
            # początek użycia gaitpy - analiza chodu
            gaitpy = Gaitpy(raw_data,
                            # Raw data consisting of vertical acceleration from lumbar location and unix timestamps
                            sample_rate,  # Sample rate of raw data (in Hertz)
                            v_acc_col_name=self.comboBox.currentText(),  # Vertical acceleration column name
                            ts_col_name='timestamps',  # Timestamp column name
                            v_acc_units='m/s^2',  # Units of vertical acceleration
                            ts_units='s',  # Units of timestamps
                            flip=True)  # If baseline data is at +1g or +9.8m/s^2, set flip=True

            #### Classify bouts of gait - Optional (use if your data consists of gait and non-gait periods)####
            gait_bouts = gaitpy.classify_bouts(
                result_file=r'..\logi\classified_gait.h5')  # File to save results to (None by default)
            """
            Scieżke powyżej i poniżej nalezy skonfigurowac samodzielnie w zalezności gdzie chcemy zapisac wyniki 
            """
            #### Extract gait characteristics ####
            gait_features = gaitpy.extract_features(subject_height,  # Subject height
                                                    subject_height_units='centimeter',  # Units of subject height
                                                    result_file=r'..\logi'
                                                                r'\gait_features.csv',
                                                    # File to save results to (None by default)
                                                    classified_gait=gait_bouts)  # Pandas Dataframe or .h5 file results of classify_bouts function (None by default)

            #### Plot results of gait feature extraction ####
            if self.dir is not None:
                gaitpy.plot_contacts(gait_features,
                                     # Pandas Dataframe or .csv file results of extract_features function
                                     result_file=self.dir + r'\plot_contacts.html',
                                     # File to save results to (None by default)
                                     show_plot=False)  # Specify whether to display plot upon completion (True by default)
                with open(self.dir + r'\plot_contacts.html', 'r') as f:
                    file = f.read()
                self.html.setHtml(file)
                self.label.setText("Oto twoja analiza chodu z wybranego pliku: " + self.filepath[self.filepath.rfind(
                    "/") + 1:self.filepath.rfind("v") + 1])
                self.label.adjustSize()
            else:
                gaitpy.plot_contacts(gait_features,
                                     # Pandas Dataframe or .csv file results of extract_features function
                                     result_file=r'..\logi\plot_contacts.html',
                                     # File to save results to (None by default)
                                     show_plot=False)  # Specify whether to display plot upon completion (True by default)
                with open(r'../logi/plot_contacts.html', 'r') as f:
                    file = f.read()
                self.html.setHtml(file)
                self.label.setText("Oto twoja analiza chodu z wybranego pliku: " + self.filepath[self.filepath.rfind(
                    "/") + 1:self.filepath.rfind("v") + 1])
                self.label.adjustSize()

        else:
            self.label.setText("Nie wybrano żadnego pliku, analiza niemożliwa")
            self.label.adjustSize()

    """
           W tym miejscu, wybierana jest scieżka folderu, gdzie będzie zapisany wyjściowy plik HTML
    """
    def choosedir(self):
        self.dir = QFileDialog.getExistingDirectory()
        self.dir = str(self.dir)
        print(self.dir)
        self.label.setText("Wybrałeś folder: " + self.dir)
        self.label.adjustSize()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
