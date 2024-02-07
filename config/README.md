# Example Config Folder

If this folder is present beside the compose.yaml file for running this project, it will be avaliable from within the running docker container for using user specified protein database weights (ie you would need a folder called `config/` in the same place as compose.yaml).

In this folder we have two example yaml config files for scoring the afdb and pdbe databases.
You do not need to include all of the parameters, the rest will be filled in with default values.

If you are not familiary with the format, `.yaml` files are lines of keys with values.
Keys can have sub-keys with their own values, where indentation matters (2 spaces for each level).

```
my_weight: 10

my_method_weights:
  default: 1
  x-ray: 0.7
  my_method: 0.8
```
Which would set `my_weight` to `10`, and `my_method_weights` to `{ 'default': 1, 'x-ray': 0.7, ... }`.
Note that we put in 2 spaces for each layer of depth. 
For more info on the yaml format check out: [yaml.org](https://yaml.org/)

## Afdb Config options

- `final_score_multiplier` The score is given by this value


## PDBe Config options

Pdbe looks for a file called `pdbe-weights.yaml` in `config/`. It can handle the following options.

- `final_score_multiplier` : The final score is multiplied by this value

### Chain Length Score

The score is the fraction of the total protein chain length that the file covers.

- `chain_length_multiplier` : The chain length score is multiplied by this value

- `default_chain_length_score` : The score given when the chain length cannot be calculated

### Method of Protein Scanning Score

This is a score for how the protein was measured (ie microscope, x-ray, etc.)

- `method_score_multiplier` : The method score is multiplied by this value

- `method_multipler` : 

This is a list of scores for each method. By default it only contains a `default` score (This is given when the method named does not have a score associated with it). 

If you wanted to add a method score (say you wanted `my_new_method` to have a score of 0.4) you would add it below `method_multiplier`

```
method_multiplier:
  x-ray: 0.2
  my_new_method: 0.4
```


### Resolution of Scanned Protein

This is a score given for the resolution of the protein. 

- `resolution_multiplier` : The resolution score is multiplied by this value

- The settings for calulating the resolution score
```
resolution:
  weight_at_0: value    # The score for a resolution of 0 Angstroms
  weight_at_1: value    # The score for a resolution of 1 Angstroms
  # How we interpolate scores between 0 and 1,
  # this can be either `linear` or `exponential`
  interpolation: value
  default: value        # The score to assign if we cannot find a resolution
```
