#!/bin/bash

ls notebooks | awk -F  '.' '{print $1}' | xargs -I {} jupyter nbconvert --to script --output ../scripts/{} notebooks/{}.ipynb
