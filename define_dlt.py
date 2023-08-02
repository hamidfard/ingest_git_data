# Databricks notebook source
# MAGIC %md
# MAGIC you create a Delta Live Tables pipeline to convert the raw GitHub data into tables that can be analyzed by Databricks SQL queries. 

# COMMAND ----------

import dlt
from pyspark.sql.functions import *

def parse(df):
   return (df
     .withColumn("author_date", to_timestamp(col("commit.author.date")))
     .withColumn("author_email", col("commit.author.email"))
     .withColumn("author_name", col("commit.author.name"))
     .withColumn("comment_count", col("commit.comment_count"))
     .withColumn("committer_date", to_timestamp(col("commit.committer.date")))
     .withColumn("committer_email", col("commit.committer.email"))
     .withColumn("committer_name", col("commit.committer.name"))
     .withColumn("message", col("commit.message"))
     .withColumn("sha", col("commit.tree.sha"))
     .withColumn("tree_url", col("commit.tree.url"))
     .withColumn("url", col("commit.url"))
     .withColumn("verification_payload", col("commit.verification.payload"))
     .withColumn("verification_reason", col("commit.verification.reason"))
     .withColumn("verification_signature", col("commit.verification.signature"))
     .withColumn("verification_verified", col("commit.verification.signature").cast("string"))
     .drop("commit")
   )

@dlt.table(
   comment="Raw GitHub commits"
)
def github_commits_raw():
  df = spark.read.json(spark.conf.get("commits-path"))
  return parse(df.select("commit"))

@dlt.table(
  comment="Info on the author of a commit"
)
def commits_by_author():
  return (
    dlt.read("github_commits_raw")
      .withColumnRenamed("author_date", "date")
      .withColumnRenamed("author_email", "email")
      .withColumnRenamed("author_name", "name")
      .select("sha", "date", "email", "name")
  )

@dlt.table(
  comment="GitHub repository contributors"
)
def github_contributors_raw():
  return(
    spark.readStream.format("cloudFiles")
      .option("cloudFiles.format", "json")
      .load(spark.conf.get("contribs-path"))
  )
