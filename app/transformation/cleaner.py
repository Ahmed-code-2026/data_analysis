import pandas as pd


def clean_data(df):

    data = df.copy()

    # --------------------------------
    # 1. إزالة المسافات الزائدة
    # --------------------------------
    text_columns = data.select_dtypes(
        include="object"
    ).columns

    for column in text_columns:
        data[column] = data[column].str.strip()

    # --------------------------------
    # 2. توحيد الكتابة للأعمدة النصية
    # --------------------------------
    if "city" in data.columns:
        data["city"] = data["city"].str.title()

    if "status" in data.columns:
        data["status"] = data["status"].str.title()

    if "major" in data.columns:
        data["major"] = data["major"].str.title()

    if "course" in data.columns:
        data["course"] = data["course"].str.title()

    # --------------------------------
    # 3. تحويل الأعمدة الرقمية
    # --------------------------------
    numeric_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance",
        "score",
        "semester"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    # --------------------------------
    # 4. معالجة القيم المفقودة
    # --------------------------------

    # الأعمدة الرقمية:
    # استخدام الوسيط Median
    numeric_columns = [
        "age",
        "gpa",
        "attendance",
        "score"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = data[column].fillna(
                data[column].median()
            )

    # الأعمدة النصية:
    # استخدام Unknown
    text_columns = data.select_dtypes(
        include="object"
    ).columns

    for column in text_columns:
        data[column] = data[column].fillna("Unknown")

    # --------------------------------
    # 5. إزالة السجلات المكررة بالكامل
    # --------------------------------
    data = data.drop_duplicates()

    return data