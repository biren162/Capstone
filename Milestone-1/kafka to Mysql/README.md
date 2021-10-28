# Commands:
open cmd
docker-compose up 

wait for above process to complete

## connect to db:
docker exec -it mysql bash -c 'mysql -u root -p$MYSQL_ROOT_PASSWORD'

use demo;

GRANT  CREATE, ALTER, DROP, SELECT, INSERT, UPDATE, DELETE ON demo.* TO connect_user;

## Create records in kafka (temporary testing)

docker exec -it ksqldb ksql http://ksqldb:8088

CREATE STREAM NEWS (title VARCHAR, summary VARCHAR, category VARCHAR, source VARCHAR, date VARCHAR)
  WITH (KAFKA_TOPIC='news', PARTITIONS=1, VALUE_FORMAT='AVRO');

INSERT INTO NEWS (title, summary ,category , source , date ) VALUES ('test title','jaldi se khatm karo ye program','sports','myownsource','10-09-2021');

open another cmd tab and run below command
docker-compose up myconnector -d


## check auto synced records in a tab where mysql is running
select * from news;

  
