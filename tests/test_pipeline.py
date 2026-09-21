import pandas as pd

from app.validation.quality import validate_data
from app.transformation.cleaner import clean_data
from app.transformation.transformer import transform_data


# --------------------------------
# 1. قراءة ملف CSV
# --------------------------------

data = pd.read_csv("C:\\Users\\Ahmed\\Desktop\\quality\\data\\raw\\raw_dataset.csv")

print("\n========== ORIGINAL DATA ==========")
print(data)


# --------------------------------
# 2. Validation
# --------------------------------

valid_data, invalid_data = validate_data(data)

print("\n========== VALID DATA ==========")
print(valid_data)


print("\n========== INVALID DATA ==========")
print(invalid_data)


# --------------------------------
# 3. Cleaning
# --------------------------------

cleaned_data = clean_data(valid_data)

print("\n========== CLEANED DATA ==========")
print(cleaned_data)


# --------------------------------
# 4. Transformation
# --------------------------------

transformed_data = transform_data(cleaned_data)

print("\n========== FINAL DATA ==========")
print(transformed_data)


# --------------------------------
# 5. معلومات عن البيانات النهائية
# --------------------------------

# print("\n========== COLUMNS ==========")
# print(transformed_data.columns.tolist())


# print("\n========== DATA TYPES ==========")
# print(transformed_data.dtypes)


# print("\n========== SHAPE ==========")
# print(transformed_data.shape)