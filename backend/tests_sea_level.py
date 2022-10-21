import sea_level_pred

def test_pol():
    print(sea_level_pred.pol_pred(CO2 = 336.56, CH4 = 1626, GLA = -10,TEMP = -0.042, HEAT = 0.35))

def test_svm():
    print(sea_level_pred.svm_pred(CO2 = 336.56, CH4 = 1626, GLA = -10,TEMP = -0.042, HEAT = 0.35))