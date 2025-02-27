# 유기동물 데이터 ETL
## 📌 프로젝트 개요

경기 공공 데이터로부터 수집한 유기동물 현황 데이터를 추출, 변환, 적재하는 ETL 파이프라인을 구성하였습니다. Docker를 사용하여 Hadoop 클러스터를 구성하고, Spark 클러스터를 활용하여 데이터를 처리합니다. 데이터는 HDFS에 저장됩니다.

## 📌 환경 설정

- **OS**: Ubuntu
- **Python**: 3.12
- **Spark**: 3.4.4
- **Hadoop**: 3.4.0
- **Jupyter Notebook**

## 📌 기술 스택

- ETL : PySpark
- 저장소 : HDFS
- 클러스터 관리 : YARN
- 데이터 처리 : Spark on YARN
- 컨테이너 관리 : Docker, Docker Compose

## 📌 주요 기능

### 1. 데이터 수집

- 경기 공공 데이터 API로부터 유기동물 현황 데이터를 수집합니다.

### 2. 데이터 변환

- 수집한 데이터를 Spark를 사용하여 처리합니다.
    - 보호 기간 계산 : 유기동물 보호된 기간(시작일자~종료일자)를 일 단위로 계산
    - 보호소별 통계 생성
        - 보호소별 총 유기동물 수
        - 보호소별 평균 보호 기간
    - 결과
        

### 3. 데이터 적재

- 변환된 데이터를 HDFS에 저장합니다.
    - 원천데이터 : hdfs://data/raw_animal_data
    - 처리된 데이터 : hdfs://data/shelter_stats
  
## 📌 과정

1. Docker Image 빌드
    - hadoop_base image 빌드
    - Docker compose 를 활용하여 클러스터 배포
        - `namenode` : 1개
        - `datanode` : 2개
2. 데이터 수집
    - 경기 공공 데이터 API로부터 유기동물 현황 데이터를 수집
    - Spark DataFrame으로 변환하여 HDFS에 저장
3. 데이터 처리
    - PySpark 를 사용하여 보호소별 유기동물 수 및 평균 보호기간 계산
4. 데이터 적재
    - 변환된 데이터를 HDFS에 저장

##  📌 트러블슈팅
### 문제 배경

- Pyspark 실행 중 작업이 실패했으며, `free -h` 를 통해 여유 메모리 부족 인식

### 해결 방법
- (1) Docker 컨테이너의 메모리 할당량 증가
- (2) swap 메모리 조정
- (3) Spark 작업의 메모리 조정
    - Spark executor memory와 driver memory를 낮춰 Spark의 메모리 요청 감소
- (4) Yarn의 maximum-allocation-mb 증가

### 개선점
- Spark의 메모리 최적화를 통해 작업 실패율 감소 및 실행 성능 향상
- Yarn의 최대 메모리 할당을 증가시켜 클러스터 자원 활용도 개선
