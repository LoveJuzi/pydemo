#!/bin/bash

psql -h localhost -p 5432 -U postgres -d postgres -f create_table.sql 
