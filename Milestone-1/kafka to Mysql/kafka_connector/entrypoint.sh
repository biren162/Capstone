#!/bin/bash

curl -X PUT http://kafka-connect:8083/connectors/sink-jdbc-mysql-01/config \
     -H "Content-Type: application/json" -d '{
    "connector.class"                    : "io.confluent.connect.jdbc.JdbcSinkConnector",
    "connection.url"                     : "jdbc:mysql://mysql:3306/demo",
    "topics"                             : "news",
    "key.converter"                      : "org.apache.kafka.connect.storage.StringConverter",
    "value.converter"                    : "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",
    "connection.user"                    : "connect_user",
    "connection.password"                : "asgard",
    "auto.create"                        : true,
    "auto.evolve"                        : true,
    "insert.mode"                        : "insert"
}'

curl -X PUT http://kafka-connect:8083/connectors/sink-jdbc-mysql-01/config \
     -H "Content-Type: application/json" -d '{
    "connector.class"                    : "io.confluent.connect.jdbc.JdbcSinkConnector",
    "connection.url"                     : "jdbc:mysql://mysql:3306/demo",
    "topics"                             : "news",
    "key.converter"                      : "org.apache.kafka.connect.storage.StringConverter",
    "value.converter"                    : "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",
    "connection.user"                    : "connect_user",
    "connection.password"                : "asgard",
    "auto.create"                        : true,
    "auto.evolve"                        : true,
    "insert.mode"                        : "insert"
}'
