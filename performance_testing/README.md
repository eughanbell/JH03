# Performace Testing / Cache Warming

The performance of the API requests can be tested with either provided or arbitrary data
This can also be used to prewarm the cache with many protein ids.

### Arbitrary Data (Cache Warming)

If you have a file with a uniprot id on each line saved beside the script 
(such as `example_ids.txt` in this folder), then by running

```
python performance_testing.py uniprot example_ids.txt
```

Then the script will run through each id and request it from `pss`. 
This means future calls to those ids will be faster, as they will be resident in the cache.


### Provided Data

Navigate to `performance_testing` and run
```
python performance_testing.py {choice of API Request} {file}
```
Refer to manuals.json keys for a list of currently available testing methods. An example file is provided to demonstrate the required data arrangement.


### Other Options

Multiple sequential and random Uniprot IDs can be tested in succession, the choice of exclusively testing alphafold is available. Execute as such:
```
python performance_testing.py {API Request 1} {Api Request 2} ... {Api Request N}
```
Refer to increments.json & randoms.json keys for a list of currently available testing methods.
