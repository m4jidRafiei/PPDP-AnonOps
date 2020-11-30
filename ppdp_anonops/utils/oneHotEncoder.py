from sklearn.preprocessing import OneHotEncoder


class OneHotClusterer:

    @staticmethod
    def Encode(valueList):
        enc = OneHotEncoder(handle_unknown='ignore')
        enc.fit(valueList)
