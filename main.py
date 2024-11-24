import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QCheckBox, QHBoxLayout, QComboBox
from PyQt5 import QtCore, sip
from tkinter import *
import predictor_helper as helper


class DrawInputScreen(QWidget):
    singleton: 'DrawInputScreen' = None
    def __init__(self):
        super().__init__()
        self.PredictHiringPlatformWindow()  #Uygulama çalıştığında gözüken ekranı oluşturur(boş pencere).
        # Bunu oluşturmak için aşağıdaki PredictHiringPlatformWindow fonksiyonuna gider
        self.DrawFeatures()     #Draw Features Fonksiyonuna giderek nesneleri oluşturur.
        self.button.clicked.connect((self.RunPredictor))    #Run Predictor Fonksiyonuna gider
        self.rebutton.clicked.connect((self.restart))   #Aşağıdaki restart fonksiyonuna gider
        self.array = []     #Boş bir dizi oluşturur

    def restart(self):
        self.window().setVisible(False)     #Restarta basıldıktan sonra uygulamayı görünmez yapar
        window2 = DrawInputScreen()         #Ardından tekrar DrawInputScreen fonksiyonunu çalıştırır
        window2.show()                      #Tekrar uygulamayı gösterir

    def ClearThings(self, layouts):
        for layout in layouts:              #Tüm layoutları dolaşır
            if layout is not None:          #Eğer layout none değilse while döngüsüne girer
                while layout.count():       #Layout sayısını kontrol eder eğer 0 değilse döngü başlar
                    item = layout.takeAt(0) #Layouttaki nesnesinin ilk elemanını alır ve layouttan çıkarır
                    widget = item.widget()  #item içindeki widget alınır ve widget değerine atanır
                    if widget is not None:  #widget değeri none değilse aşağıdaki if komutuna geçer
                        if type(widget) == QPushButton: #widget eğer bir butonsa
                            if widget.isEnabled():
                                widget.setEnabled(False)    #Buton etkinse devre dışı bırakır
                            else:
                                widget.setEnabled(False)    #Buton etkinse yine devre dışı bırakır
                            break
                    else:
                        self.clearLayout(item.layout())     #Eğer widget değeri nonesa buraya gelir ve
                                                            # layouttaki diğer nesneleri temizler


    def SetResult(self, text, margin_top):
        self.label = QLabel(text, self)                     #Label nesnesi oluşturur ve ismini text parametresiyle alır
        self.label_layout.addWidget(self.label)             #Label'ı bir label_layout isimli layoutun içine ekler
        self.label.setGeometry(400, margin_top, 200, 75)    #Labelın konumu ve boyutunu belirler
        self.label.setText(text)                            #Labelın görünen ismi belirlenir
        self.label.show()                                   #Label arayüzde gösterilir

    def GetCheckedBoxes(self, object):
        if not type(object) == QComboBox and object.isCheckable():  #Obje ComboBox değilse ve İşaretlenebilirse bu bloğun içine girer
            if object.isChecked():                                  #Obje işaretliyse
                self.array.append(object.text())                    #En başta oluşturduğumuz Self Array'in içine nesne eklenir
            else:                                                   #Obje işaretli değilse
                if self.array.count(object.text()) > 0:             #Checkbox self arrayın içindeyse
                    self.array.remove(object.text())                #Self Arrayden nesne kaldırılır
        elif type(object) == QComboBox:                             #Obje eğer ComboBox ise
            for item in self.array:                                 #Self array listesinde
                if str(item).count('year(s)') > 0:                  #years içeren öğe varsa
                    self.array.remove(item)                         #Self arrayden silinir
            self.array.append(object.currentText())                 #ComboBox'ın metni tekrar eklenir (year(s))
        else:
            self.array.append(object.text())

    def PredictHiringPlatformWindow(self):
        self.resize(1000, 500)      #Pencerenin genişlik ve yüksekliği ayarlanır
        self.move(300, 150)         #Pencerenin başlatıldığı konumunu ayarlar
        self.setWindowTitle('Prediction of Social Hiring Platform App')     #Pencerenin metni ayarlanır

    def DrawFeatures(self):
        self.label_layout = QHBoxLayout()   #Yatay düzenli Layoutlar oluşturulur
        self.cbox_layout = QHBoxLayout()    #Yatay düzenli Layoutlar oluşturulur
        self.button_layout = QHBoxLayout()  #Yatay düzenli Layoutlar oluşturulur

        self.f1 = QCheckBox("0 - ForeignLanguageSkills")    #f1 Checkboxını oluşturduk
        self.f1.stateChanged.connect(lambda: self.GetCheckedBoxes(self.f1))     #CheckBoxun durumu değiştiğinde GetCheckedBoxes fonksiyonu çağırılır
        self.cbox_layout.addWidget(self.f1)                 #Oluşturulan CheckBox yukarda oluşturulan Layoutun içine eklenir
        self.f2 = QCheckBox("1 - ComputerSkills")           #f2 Checkboxını oluşturduk
        self.f2.stateChanged.connect(lambda: self.GetCheckedBoxes(self.f2))     #CheckBoxun durumu değiştiğinde GetCheckedBoxes fonksiyonu çağırılır
        self.cbox_layout.addWidget(self.f2)                 #Oluşturulan CheckBox yukarda oluşturulan Layoutun içine eklenir
        self.f3 = QCheckBox("2 - AdvancedMSExcelSkills")    #f3 Checkboxını oluşturduk
        self.f3.stateChanged.connect(lambda: self.GetCheckedBoxes(self.f3))     #CheckBoxun durumu değiştiğinde GetCheckedBoxes fonksiyonu çağırılır
        self.cbox_layout.addWidget(self.f3)                 #Oluşturulan CheckBox yukarda oluşturulan Layoutun içine eklenir
        self.f4 = QCheckBox("3 - WillingToRelocate")        #f4 Checkboxını oluşturduk
        self.f4.stateChanged.connect(lambda: self.GetCheckedBoxes(self.f4))     #CheckBoxun durumu değiştiğinde GetCheckedBoxes fonksiyonu çağırılır
        self.cbox_layout.addWidget(self.f4)                 #Oluşturulan CheckBox yukarda oluşturulan Layoutun içine eklenir
        self.f5 = QCheckBox("4 - OverTime")                 #f5 Checkboxını oluşturduk
        self.f5.stateChanged.connect(lambda: self.GetCheckedBoxes(self.f5))     #CheckBoxun durumu değiştiğinde GetCheckedBoxes fonksiyonu çağırılır
        self.cbox_layout.addWidget(self.f5)                 #Oluşturulan CheckBox yukarda oluşturulan Layoutun içine eklenir

        self.label = QLabel("5 - TotalWorkingYears", self)  #Bir Label oluşturulur
        self.cbox_layout.addWidget(self.label)              #Oluşturulan Label ComboBox Layoutuna eklenir
        self.cb = QComboBox()                               #ComboBox oluşturulur
        for i in range(0, 31):
            text = str(i) + " year(s)"
            self.cb.addItem(text)                           #0-30 arası sayılar ComboBox içine eklenir
        self.cb.currentIndexChanged.connect(lambda: self.GetCheckedBoxes(self.cb))      #ComboBoxın değişip değişmediğini kontrol eder ve günceller
        self.cbox_layout.addWidget(self.cb, stretch=1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft) #ComboBoxı Layouta ekler

        self.f7 = QCheckBox("6 - Hired")                    #f7 Checkboxını oluşturduk
        self.f7.stateChanged.connect(lambda: self.GetCheckedBoxes(self.f7))     #CheckBoxun durumu değiştiğinde GetCheckedBoxes fonksiyonu çağırılır
        self.cbox_layout.addWidget(self.f7)                 #Oluşturulan CheckBox yukarda oluşturulan Layoutun içine eklenir

        self.button = QPushButton("Run Predictor", self)    #Run Predictor butonunu oluşturur
        self.button.setGeometry(350, 350, 200, 75)          #Butonun (X,Y,Genişlik,Yükseklik) değerleri belirlenir

        self.rebutton = QPushButton("Clear", self)          #Clear butonunu oluşturur
        self.rebutton.setGeometry(550, 350, 200, 75)        #Butonun (X,Y,Genişlik,Yükseklik) değerleri belirlenir
        self.button_layout.addWidget(self.button)           #Butonlar Layoutların içine eklenir
        self.button_layout.addWidget(self.rebutton)         #Butonlar Layoutların içine eklenir
        self.setLayout(self.cbox_layout)                    #Pencerenin ana düzeni belirlenir

    def RunPredictor(self):
        if self.array.count(self.cb.currentText()) == 0:    #ComboBoxların kontrolü gerçekleşir
            self.array.append(self.cb.currentText())        #Eğer ComboBoxtan bir değer seçildiyse ve Self Arrayin içinde yoksa ekler
        if len(self.array) == 1:                            #Self Arrayde yalnızca 1 öğe varsa (ComboBox) CheckBoxlar kontrol edilir
            self.GetCheckedBoxes(self.f1)                   #Seçili CheckBoxlar belirlenir ve Self Arraye eklenir
            self.GetCheckedBoxes(self.f2)
            self.GetCheckedBoxes(self.f3)
            self.GetCheckedBoxes(self.f4)
            self.GetCheckedBoxes(self.f5)
            self.GetCheckedBoxes(self.f7)

        value, score = helper.predict_platform(self.array)  #predict_platformdan gelen sonuçlara göre değerler döndürür
        self.SetResult('Predicted Platform : ' + str(value), 100)   #Sonuçları Gösterir
        self.SetResult('Accuracy Score : %' + "%.2f" %(score), 150) #Sonuçları Gösterir
        self.ClearThings([self.label_layout, self.cbox_layout, self.button_layout]) #ClearThings fonksiyonuna gider ve Layoutları temizler

        self.array = [] #Self Arrayi sıfırlar


app = QApplication(sys.argv)
window = DrawInputScreen()
window.show()
sys.exit(app.exec_())


