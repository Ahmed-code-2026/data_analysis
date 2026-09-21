import pandas as pd

from app.utils.logger import get_logger


logger = get_logger("transformer")


def transform_data(df):
    logger.info("Starting data transformation for %d records", len(df))

    try:
        data = df.copy()

        # --------------------------------
        # 1. توحيد أسماء الأعمدة
        # --------------------------------
        data.columns = (
            data.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # --------------------------------
        # 2. تحويل أنواع البيانات
        # --------------------------------

        if "student_id" in data.columns:
            data["student_id"] = data["student_id"].astype("Int64")

        if "age" in data.columns:
            data["age"] = data["age"].astype("Int64")

        if "gpa" in data.columns:
            data["gpa"] = data["gpa"].astype(float)

        if "attendance" in data.columns:
            data["attendance"] = data["attendance"].astype(float)

        if "score" in data.columns:
            data["score"] = data["score"].astype(float)

        if "semester" in data.columns:
            data["semester"] = data["semester"].astype("Int64")

        # --------------------------------
        # 3. إنشاء performance_level
        # --------------------------------

        def get_performance_level(gpa):

            if gpa >= 3.5:
                return "Excellent"

            elif gpa >= 3.0:
                return "Very Good"

            elif gpa >= 2.5:
                return "Good"

            elif gpa >= 2.0:
                return "Acceptable"

            else:
                return "At Risk"

        data["performance_level"] = data["gpa"].apply(
            get_performance_level
        )

        # --------------------------------
        # 4. إنشاء attendance_status
        # --------------------------------

        data["attendance_status"] = data["attendance"].apply(
            lambda attendance:
            "Good" if attendance >= 75 else "Low"
        )

        logger.info("Data transformation completed for %d records", len(data))
        return data
    except Exception:
        logger.exception("Data transformation failed")
        raise