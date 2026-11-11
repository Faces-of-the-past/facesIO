From the point of view of data management, this project has two challenges ahead:

1. A classic data acquisition problem: digesting data from different sources (RKD's collection, Prado's collection, ...)
2. A new research-specific problem: turning the data from 1. into pairs containing `sitter_id` and `sitter_image`. These are the elementary particles we are going to feed to our ML algorithm

Problem 1 has known solutions. One of them is using an adapter pattern, a concept from Object Oriented Programming.

Problem 2 forces us to think of data structures. My suggestion is to use `Artwork`, for individual records, possibly with multiple sitters on them, and `Sitter` for each of those sitters.

Eventually, a list (or iterable) of `Sitter` objects will be fed to the ML algorithm. One (or multiple) `Interface`s orchestrate this.

See diagram below:

![](docs/classes.png)

The idea is that the **same** `Collection` interface can handle all sources of data. The specific implementations for handling different input sources are delegated to the sub-classes. See example [here](docs/rkd_imports.ipynb).

## Alternative approaches
After discussing this idea with the engineers at the Social Sciences and Humanities section:
### Reduce complexity
If `PradoCollection` and `RKDCollection` just contain a data parser, they are just a function in disguise. Consider just using `read_prado(path)` and `read_rkd(path)`.
### Consider using `pydantic`
`pydantic` adds model validation on top of the class hierarchy.\
### Consider using `attrs`
`attrs` seems to be a lightweight alternative to `pydantic`
### Consider using `polars`
A more modern, schema + dataframe approach.
