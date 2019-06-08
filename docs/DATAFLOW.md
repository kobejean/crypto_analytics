# Data Flow
A broad picture of the data flow of the `crypto_analytics` module.
### Table
- [Data Collection](#data-collection)
- [Preprocessing](#preprocessing)

### Data Collection
```
  ------------         ------------
  | endpoint |   ...   | endpoint |
  ------------         ------------
       |                    |
       v                    v
 --------------       --------------      ------------------------
 | DataSource |  ...  | DataSource |  --  | CollectionController |
 --------------       --------------      ------------------------
       |                    |
       v                    v
----------------     ----------------
| raw_data.csv | ... | raw_data.csv |
----------------     ----------------
```
- `endpoint` - the endpoint we are collecting data from
- `DataSource` - the class that fetches and writes our raw API data
- `CollectionController` - the class that periodically calls `fetch` and `write` for all `DataSource` classes
- `raw_data.csv` - the file we are writing raw data to

### Preprocessing
```
----------------     ----------------
| raw_data.csv | ... | raw_data.csv |
----------------     ----------------
       |                    |
       v                    v
 --------------       --------------
 | DataSource |  ...  | DataSource |
 --------------       --------------
       |                    |
       ----------------------
                  |
                  v
           ---------------      ---------------------------
           | DataHandler |  --  | PreprocessingController |
           ---------------      ---------------------------
                  |
                  v
      -------------------------
      | preprocessed_data.csv |
      -------------------------
```
- `raw_data.csv` - the file we are reading raw data from
- `DataSource` - the class that reads from our saved raw data
- `DataHandler` - the class that transforms data from multiple `DataSource` classes and combines them in to one table of data
- `preprocessed_data.csv` - the file we are writing preprocessed data to
