  # Dataflow
A broad picture of the dataflow of the `crypto_analytics` module.

### Key
```
flow direction  =  <-  ->  |  ^
                           v  |
                   -----
node            =  | x |
                   -----
                   *---*
runloop/script  =  | x |
                   *---*
                   -----     -----
multiple nodes  =  | x | ... | x |
                   -----     -----
```

### Table
- [Data Collection](#data-collection)
- [Preprocessing](#preprocessing)
- [Training](#training)
- [Live Inference](#live-inference)

### Data Collection
```
  ------------         ------------
  | endpoint |   ...   | endpoint |
  ------------         ------------
       |                    |
       v                    v
 --------------       --------------      *----------------------*
 | DataSource |  ...  | DataSource |  ->  | CollectionController |
 --------------       --------------      *----------------------*
       |                    |                         |
       v                    v                         v
----------------     ----------------           ------------
| raw_data.csv | ... | raw_data.csv |           | Notifier |
----------------     ----------------           ------------
```
- `endpoint` - the endpoint we are collecting data from
- `DataSource` - the class that fetches and writes our raw API data
- `CollectionController` - the class that periodically calls `fetch` and `write` for all `DataSource` classes
- `Notifier` - handles sending notifications to discord etc.
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
           ---------------      *-------------------------*
           | DataHandler |  ->  | PreprocessingController |
           ---------------      *-------------------------*
                  |                          |
                  v                          v
      -------------------------        ------------
      | preprocessed_data.csv |        | Notifier |
      -------------------------        ------------
```
- `raw_data.csv` - the file we are reading raw data from
- `DataSource` - the class that reads from our saved raw data
- `DataHandler` - the class that transforms data from multiple `DataSource` classes and combines them in to one table of data
- `PreprocessingController` - the class that calls `read` and `write` and validates the preprocessed data
- `Notifier` - handles sending notifications to discord etc.
- `preprocessed_data.csv` - the file we are writing preprocessed data to

### Training
```
-------------------------
| preprocessed_data.csv |
-------------------------
            |
            v
     ---------------
     | DataHandler |
     ---------------
            |
            v
        ---------      *--------------------*
        | Model |  ->  | TrainingController |
        ---------      *--------------------*
            |                    |
            v                    v
      --------------        ------------
      | checkpoint |        | Notifier |
      --------------        ------------
```
- `preprocessed_data.csv` - the file we are reading preprocessed data from
- `DataHandler` - the class that holds the preprocessed data read from `preprocessed_data.csv`
- `Model` - the model that gets trained
- `TrainingController` - the class that manages the training loop
- `Notifier` - handles sending notifications to discord etc.
- `checkpoint` - the file that stores our model's learned weights


### Live Inference
```
 ------------         ------------
 | endpoint |   ...   | endpoint |
 ------------         ------------
       |                    |
       v                    v
--------------       --------------
| DataSource |  ...  | DataSource |
--------------       --------------
       |                    |
       ----------------------
                 |
                 v
          ---------------
          | DataHandler |
          ---------------
                 |
                 v
             ---------      --------------
             | Model |  <-  | checkpoint |
             ---------      --------------
                 |
                 v
           *----------*      ------------
           | TradeBot |  ->  | TradeAPI |
           *----------*      ------------
                 |
                 v
           ------------
           | Notifier |
           ------------
```
- `endpoint` - the endpoint we are reading live data from
- `DataSource` - the class that fetches our endpoint data
- `DataHandler` - the class that transforms data from multiple `DataSource` classes and combines them in to one table of data
- `Model` - the trained model that makes predictions
- `checkpoint` - the file that stores our model's learned weights
- `TradeBot` - the bot that takes model predictions and makes trades
- `TradeAPI` - the class that allows us to make trades by calling trading
- `Notifier` - handles sending notifications to discord etc. APIs
