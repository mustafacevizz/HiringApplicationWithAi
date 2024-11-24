import pydotplus
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from six import StringIO
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier


def mapper(df, values, column_name):
    df[column_name] = df[column_name].map(values)   #Belirli değerleri kullanıcı tarafından değer atamak için kullandık


def visualize_tree(clf, features):                  #Karar ağacını görselleştirme fonksiyonu
    dot_data = StringIO()
    tree.export_graphviz(clf, out_file=dot_data,    #Bu fonksiyon karar ağacını dot formatına dönüştürür
                         feature_names=features)    # karar ağacını ve kullanılan özelliklerin ismini alır
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  #Grafiğe dönüştürür
    graph.write_png('result.png')                   #PNG formatında kaydeder



def predict_platform(features_array):   #Mapper dönüşümü ile değerler tanımlanır
    platform_list = {'Linkedin': 1, 'Kariyer.net': 2, 'Yenibiris.com': 3, 'Friend Advice': 4, 'Isbul.net': 5,
                     'Other': 6}    #Platform listemizi tanımladık
    df = pd.read_csv("dataset/HR-Employee-Attrition.csv", encoding="latin1", sep=';', header=0) #Veri setimizi okuduk
    numerical_values = {'Yes': 1, 'No': 0}  #Sayısal evet hayır değelerini tanımladık
    mapper(df, numerical_values, 'Hired')   #Hired değerini mapper dönüşümü ile 0-1 olacak şekilde belirledik
    mapper(df, numerical_values, 'OverTime')    #OverTime değerini mapper dönüşümü ile 0-1 olacak şekilde belirledik
    mapper(df, numerical_values, 'ForeignLanguageSkills')   #ForeignLanguageSkills değerini mapper dönüşümü ile 0-1 olacak şekilde belirledik
    mapper(df, numerical_values, 'ComputerSkills')  #ComputerSkills değerini mapper dönüşümü ile 0-1 olacak şekilde belirledik
    mapper(df, numerical_values, 'AdvancedMSExcelSkills')   #AdvancedMSExcelSkills değerini mapper dönüşümü ile 0-1 olacak şekilde belirledik
    mapper(df, numerical_values, 'WillingToRelocate')   #WillingToRelocate değerini mapper dönüşümü ile 0-1 olacak şekilde belirledik
    mapper(df, {'Travel_Rarely': 1, 'Travel_Frequently': 2, 'Non-Travel': 0}, 'BusinessTravel')
    mapper(df, {'Sales': 1, 'Research & Development': 2, 'Human Resources': 3}, 'Department')
    mapper(df, {'Life Sciences': 1, 'Other': 0, 'Medical': 2, 'Marketing': 3, 'Technical Degree': 4,
                'Human Resources': 5}, 'EducationField')
    mapper(df, {'Male': 0, 'Female': 1}, 'Gender')
    mapper(df, {'Sales Executive': 1, 'Research Scientist': 2, 'Laboratory Technician': 3,
                'Manufacturing Director': 4, 'Healthcare Representative': 5, 'Manager': 6,
                'Sales Representative': 7, 'Research Director': 8, 'Human Resources': 9}, 'JobRole')
    mapper(df, {'Single': 1, 'Married': 2, 'Divorced': 0}, 'MaritalStatus')
    mapper(df, {'Y': 1, 'N': 0}, 'Over18')
    mapper(df, platform_list,
           'HearUsFrom')
    independents = list(df.columns[-8:-1])  #Bağımsız değişkenleri belirler ve modelin tahmininde kullanır
    df.dropna(inplace=True)     #Veri setindeki boş değerleri kaldırır

    y = df["HearUsFrom"]        #Y bağımlı değişkeni HearUsFrom belirlendi
    X = df[independents]        #X bağımsız değişkeni independents belirlendi

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=20)  #Eğitim ve Test setlerine ayırdı

    model = RandomForestClassifier(n_estimators=100)    #Random Forest modeli oluşturur
    model.fit(X_train, y_train)                         #X_train ve y_train ile eğitir

    positions = []          # Boş bir liste oluşturuluyor bu liste özelliklerin pozisyonlarını tutacak
    features = []           # Boş bir liste oluşturuluyor, bu liste özellikleri tutacak.
    year_info_cursor = 0    # Yıl bilgisine ait pozisyonun indeksini tutacak
    for i in range(0, len(features_array)):
        if str(features_array[i]).count('year(s)') > 0: # Eğer özellik isminde 'year(s)' ifadesi bulunuyorsa
            positions.append(5)     # 'year(s)' ifadesi bulunursa, positions listesine 5 ekleniyor (pozisyonu temsil eder)
            year_info_cursor = i    # Yıl bilgisine ait pozisyonun indeksi year_info_cursor değişkenine atanıyor.
        else:   #Eğer özellik ismi boş değilse
            if len(features_array[i]) > 0:
                if len(features_array[i]) > 2:  # Eğer özellik ismi 2 karakterden uzunsa (sayısal bir değeri temsil ediyorsa)
                    positions.append(int(features_array[i][0])) # İlk karakteri alarak pozisyon listesine ekleniyor.
                else:
                    positions.append(int(features_array[i]))    # Özellik ismi 2 karakterden kısa ise direkt olarak ekleniyor.

    if positions and len(positions) > 0:    # Eğer positions listesi boş değilse ve uzunluğu 0'dan büyükse
        for x in range(0, len(independents)):
            if not x == 5 and x in positions:   # Eğer x pozisyon listesinde değilse ve x!=5 ise
                features.append(1)  # features listesine 1 ekleniyor
            elif not x == 5:
                features.append(0)  # features listesine 0 ekleniyor
            else:   # x=5 ise (yıl bilgisine ait pozisyon)
                features.insert(5, int(features_array[year_info_cursor][:-8]))  # Yıl bilgisini features listesine ekleniyor.
                # Sonuç olarak, positions ve features listeleri belirlenmiş oluyor.
    predicted_key = model.predict([features])   #Random forest modeli az önce oluşturulan features özelliklerini kullanarak tahmin yapılır
    #predicted_key modelin tahmin ettiği sayısal sınıftır
    predicted_value = ""
    prediction_score =  model.score(X_test, y_test) * 100

    for key, value in platform_list.items():    #En başta belirttiğimiz paltform_listteki elemanlarları key,value ile döner
        if value == predicted_key[0]:           #Tahmin ettiği predictedkey ile value eşleşiyorsa
            predicted_value = key               #predictedvalue ya key değerini atar yani eğer predictedkey 1 ise platform listesindeki 1. ile eşleşir
            break                               #döngüden çıkar

    clf = DecisionTreeClassifier()  # Decision tree Classifier oluşturulur
    clf = clf.fit(X, y)             # Karar ağacı X ve y ile eğitilir, modelin verileri öğrenmesi sağlanır
    visualize_tree(clf, independents)   #Yukardaki visualize_tree fonksiyonuna gidip oluşturduğu karar ağacını görselleştirir
    ReturnGraph(df, y_test, ['Linkedin', 'Kariyer.net', 'Yenibiris.com', 'Friend Advice', 'Isbul.net', 'Other'])

    return predicted_value, prediction_score    #Tahmin edilen platform ismini ve modelin doğruluk skoru değerlerini döndürür


def ReturnGraph(df, y_test, platform_list):
    # ------Actual&Predicted----------
    _df = pd.DataFrame({'Actual': df['HearUsFrom'][:len(y_test)].values.flatten()
                          , 'Predicted': y_test.values[:, ]})

    df1 = _df.head(50)
    df1.plot(kind='bar', figsize=(20, 8)).set_yticklabels(platform_list)
    plt.title("Predicted and Actual Hiring Platforms In 50 Data")
    plt.grid(which='minor', linestyle=':', linewidth='2', color='black')
    plt.show()
    # --------------------------------

    # -------Female & Male Hiring&Fail Counts------
    mapper(df, {0: 'Male', 1: 'Female'}, 'Gender')
    #
    females = df["Gender"].isin(["Female"])
    hired_females = df["Hired"].isin([1])
    not_hired_females = df["Hired"].isin([0])
    #
    males = df["Gender"].isin(["Male"])
    hired_males = df["Hired"].isin([1])
    not_hired_males = df["Hired"].isin([0])
    #
    females_positive = len(df[females & hired_females])
    females_negative = len(df[females & not_hired_females])
    #
    males_positive = len(df[males & hired_males])
    males_negative = len(df[males & not_hired_males])
    #
    _df = pd.DataFrame({'Hired Females': females_positive
                            , 'Hired Males': males_positive}, index=['']
                        )
    _df.plot(kind='bar', figsize=(10, 8), grid=True)
    plt.title("'Hired Female & Male' Counts")
    plt.show()#for hiring
    #
    _df2 = pd.DataFrame({'Failed Females': females_negative
                           , 'Failed Males': males_negative}, index=['']
                       )
    _df2.plot(kind='bar', figsize=(10, 8), grid=True)
    plt.title("'Failures of Female & Male Hiring' Counts")
    plt.show() #for failures
    # -----------------------------------------------

    # ------- Hiring Counts By Platform------

    lengths = []
    for i in range(1, len(platform_list) + 1):
        p = df["HearUsFrom"].isin([i])
        h = df["Hired"].isin([1])
        lengths.append(len(df[p & h]))
    df = pd.DataFrame(
        lengths, index=platform_list, columns=["Hiring Counts By Platforms"]
    )

    df.plot.pie(subplots=True, figsize=(10, 10), fontsize=11, autopct="%1.1f%%", rotatelabels=True,
                explode=(0, 0.1, 0, 0, 0, 0))
    plt.show()
    # -----------------------------------------------