import pandas as pd

from app.utils.logger import get_logger


logger = get_logger("quality")


def validate_data(df):
    logger.info("Starting data validation for %d records", len(df))

    data = df.copy()

    # الأعمدة التي يجب أن تكون موجودة
    required_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance",
        "score"
    ]

    # التحقق من وجود الأعمدة
    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # تحويل الأعمدة الرقمية إلى أرقام
    numeric_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance",
        "score"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # إنشاء عمود لأسباب الأخطاء
    data["error_reason"] = ""

    # student_id مفقود
    data.loc[
        data["student_id"].isna(),
        "error_reason"
    ] += "Missing or invalid student_id; "

    # student_id مكرر
    duplicate_student_ids = (
        data["student_id"].notna()
        & data["student_id"].duplicated(keep=False)
    )
    data.loc[
        duplicate_student_ids,
        "error_reason"
    ] += "Duplicate student_id; "

    # العمر خارج النطاق
    data.loc[
        data["age"].isna()
        | (data["age"] < 16)
        | (data["age"] > 80),
        "error_reason"
    ] += "Invalid age; "

    # GPA خارج النطاق
    data.loc[
        data["gpa"].isna()
        | (data["gpa"] < 0)
        | (data["gpa"] > 4),
        "error_reason"
    ] += "Invalid GPA; "

    # الحضور خارج النطاق
    data.loc[
        data["attendance"].isna()
        | (data["attendance"] < 0)
        | (data["attendance"] > 100),
        "error_reason"
    ] += "Invalid attendance; "

    # الدرجة خارج النطاق
    data.loc[
        data["score"].isna()
        | (data["score"] < 0)
        | (data["score"] > 100),
        "error_reason"
    ] += "Invalid score; "

    # فصل البيانات الصحيحة والخاطئة
    invalid_data = data[
        data["error_reason"] != ""
    ].copy()

    valid_data = data[
        data["error_reason"] == ""
    ].copy()

    # إزالة عمود الأخطاء من البيانات الصحيحة
    valid_data = valid_data.drop(
        columns=["error_reason"]
    )

    logger.info(
        "Data validation completed: %d valid, %d invalid",
        len(valid_data),
        len(invalid_data),
    )
    return valid_data, invalid_data