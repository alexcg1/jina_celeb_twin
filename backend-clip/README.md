## Download and extract data

1. `mkdir data`
2. Download [celeba dataset](https://drive.google.com/file/d/0B7EVK8r0v71pZjFTYXZWM3FlRnM/view?resourcekey=0-dYn9z10tMJOBAkviAcfdyQ)
3. Extract into `data`

## Index

```shell
python app.py -t index -n 1000 # "-n" specifies max docs to index
```

## Query

```shell
python app.py -t query_restful
```
