# Java와 Spark의 경로 설정
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SPARK_HOME=/opt/spark
export HADOOP_HOME=/opt/hadoop-3.4.0
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

# Spark Master의 호스트 설정
export SPARK_MASTER_HOST=namenode

# Hadoop 환경과의 연동
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop

# 네이티브 라이브러리 설정
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH

# Spark 작업 로그 설정
export SPARK_LOG_DIR=$SPARK_HOME/logs

# Spark History Server 설정
export SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs://namenode:9000/spark-logs -Dspark.history.ui.port=18080"
