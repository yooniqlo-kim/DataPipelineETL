import findspark
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, unix_timestamp, to_date
from pyspark.sql.types import StructType, StructField, StringType

findspark.init()

# SparkSession 생성
spark = SparkSession.builder \
    .appName("AnimalShelterDataProcessing") \
    .getOrCreate()

# Spark 버전 확인
print("Spark Version:", spark.version)

# 1. 원천 데이터 수집
def fetch_api_data():
    url = "https://openapi.gg.go.kr/AbdmAnimalProtect"
    params = {
        "KEY": "{api_key}",
        "Type": "json",
        "pIndex": 1,
        "pSize": 1000
    }

    response = requests.get(url, params=params)
    
    data = response.json()
    rows = data.get('AbdmAnimalProtect', [{}])[1].get('row', [])
    return rows

# 데이터 수집
raw_data = fetch_api_data()
print(raw_data)

hdfs_raw_path = "hdfs://namenode:9000/data/raw_animal_data"

# Spark DataFrame 생성 
schema = StructType([
    StructField("SIGUN_CD", StringType(), True),
    StructField("SIGUN_NM", StringType(), True),
    StructField("ABDM_IDNTFY_NO", StringType(), True),
    StructField("THUMB_IMAGE_COURS", StringType(), True),
    StructField("RECEPT_DE", StringType(), True),
    StructField("DISCVRY_PLC_INFO", StringType(), True),
    StructField("SPECIES_NM", StringType(), True),
    StructField("COLOR_NM", StringType(), True),
    StructField("AGE_INFO", StringType(), True),
    StructField("BDWGH_INFO", StringType(), True),
    StructField("PBLANC_IDNTFY_NO", StringType(), True),
    StructField("PBLANC_BEGIN_DE", StringType(), True),
    StructField("PBLANC_END_DE", StringType(), True),
    StructField("IMAGE_COURS", StringType(), True),
    StructField("STATE_NM", StringType(), True),
    StructField("SEX_NM", StringType(), True),
    StructField("NEUT_YN", StringType(), True),
    StructField("SFETR_INFO", StringType(), True),
    StructField("SHTER_NM", StringType(), True),
    StructField("SHTER_TELNO", StringType(), True),
    StructField("PROTECT_PLC", StringType(), True),
    StructField("JURISD_INST_NM", StringType(), True),
    StructField("CHRGPSN_NM", StringType(), True),
    StructField("CHRGPSN_CONTCT_NO", StringType(), True),
    StructField("PARTCLR_MATR", StringType(), True),
    StructField("REFINE_LOTNO_ADDR", StringType(), True),
    StructField("REFINE_ROADNM_ADDR", StringType(), True),
    StructField("REFINE_ZIP_CD", StringType(), True),
    StructField("REFINE_WGS84_LOGT", StringType(), True),
    StructField("REFINE_WGS84_LAT", StringType(), True)
])

raw_df = spark.createDataFrame(raw_data, schema=schema)

# 2. 원천 데이터를 HDFS에 저장
raw_df.write.mode("overwrite").parquet(hdfs_raw_path)
print(f"{hdfs_raw_path}")

# 3. HDFS에서 원천 데이터를 로드
loaded_df = spark.read.parquet(hdfs_raw_path)

# 4. 데이터 변형 (보호 기간 계산 및 보호소별 통계 생성)
transformed_df = loaded_df.withColumn("BEGIN_DATE", to_date(col("PBLANC_BEGIN_DE"), "yyyyMMdd")) \
    .withColumn("END_DATE", to_date(col("PBLANC_END_DE"), "yyyyMMdd")) \
    .withColumn("DURATION",
                (unix_timestamp(col("END_DATE")) - unix_timestamp(col("BEGIN_DATE"))) / (60 * 60 * 24))

shelter_stats = transformed_df.groupBy("SHTER_NM") \
    .agg(
        count("*").alias("TOTAL_ANIMALS"),
        avg(col("DURATION")).alias("AVG_PROTECTION_DURATION")
    )

shelter_stats.show(truncate=False)

#5. 데이터 적재
hdfs_processed_path = "hdfs://namenode:9000/data/shelter_stats"

shelter_stats.write.mode("overwrite").parquet(hdfs_processed_path)
print(f"{hdfs_processed_path}")
