from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("H2H_Wins_Test").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Spark SQL Query computing sum(win)
df = spark.sql("""
SELECT 'Mumbai Indians' AS team, 1 AS win
UNION ALL SELECT 'Mumbai Indians', 1
UNION ALL SELECT 'Mumbai Indians', 1
UNION ALL SELECT 'Chennai Super Kings', 1
UNION ALL SELECT 'Chennai Super Kings', 1
""")

result = df.groupBy("team").sum("win").orderBy("sum(win)", ascending=False)
result.show()

spark.stop()
