# Autogenerate Demo Page  

+ Update **data.xlsx** with video and paper information
  + Thumbnails should be in **../files/images/ directory** and with **resolution 500x360**
  + Video link should be the **YouTube embed ID**
  + Collapsed = 1 indicates the entry would not be highlighted among the top entries  
  + Entries appear in same order as provided in the datasheet
+ *Run compile_page.py to generate index.html in directory ../*
  + Requires [**openpyxl**](https://openpyxl.readthedocs.io/en/stable/)
  + Requires MS Excel (or equivalent)