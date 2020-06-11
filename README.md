# trregions
Django based rest API for Cities & districts of Turkey.


## Data
- Please download latest dataset from [http://postakodu.ptt.gov.tr/Dosyalar/pk_list.zip](http://postakodu.ptt.gov.tr/Dosyalar/pk_list.zip).
- Extract Excel file, place it project root and rename it to `data.xlsx`.
- Then run following:
```bash
$ python manage.py importdata
```