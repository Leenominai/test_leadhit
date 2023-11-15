#!/bin/bash

# Тестовый запрос 1
curl -X POST -d "f_name1=value1&f_name2=value2" http://localhost:5000/get_form

# Тестовый запрос 2
curl -X POST -d "f_name1=invalid_phone" http://localhost:5000/get_form