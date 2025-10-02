# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib, os

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("outputs/dataset.csv")
X = df[["load","A"]].abs()  # features
y = df["max_stress"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(Xtr, ytr)
pred = model.predict(Xte)
print("MAE:", mean_absolute_error(yte, pred))
print("R2:", r2_score(yte, pred))
joblib.dump(model, "outputs/model.joblib")
print("model saved to outputs/model.joblib")




















# # train_model.py (skeleton)
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_absolute_error, r2_score
# import joblib

# df = pd.read_csv('outputs/dataset.csv')
# X = df[['load', 'A_mean', 'geom_param1']]  # مثال
# y = df['max_stress']
# Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=0.2, random_state=42)
# model = RandomForestRegressor(n_estimators=200, random_state=42)
# model.fit(Xtr, ytr)
# pred = model.predict(Xte)
# print("MAE:", mean_absolute_error(yte, pred), "R2:", r2_score(yte, pred))
# joblib.dump(model, 'outputs/model.joblib')
