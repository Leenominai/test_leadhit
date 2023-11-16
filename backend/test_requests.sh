#!/bin/bash

# Тестовый запрос 1
curl -X POST -d "f_name1=value1&f_name2=value2" http://test_backend:5000/get_form

# Тестовый запрос 2
curl -X POST -d "f_name1=invalid_phone" http://test_backend:5000/get_form