# mftr

Not ready for prime time needs more testing !!

 Multiple File Token Replace 

python 3.6 script that allows you  to find a regex token and replace that match with some value in multiple files.  There are options to create a backup file and log all changes.  Other options allow you to overwrite the existing file , but the size of the token-match must equal the size or the replacement string. 


## Getting Started

switches :
* --token <t>  regex expression to match on
* --replace <r> string that will be replacing any matched tokens
* --directory <d>  directory to start the find and replace from 
* --rewrite    rewrite the file that has changes with out the restriction of  token-match-size == replace-string-size
* --backup     create a backup file (keep original with .bak extension)
* --log <l>    create a log file of all lines changed 

### Prerequisites

Minimally tested under python 3.6 only

```
Give examples
```

### Installing

chmod gu+x multiFileTokenReplace.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* 
* 
* 

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Readme template by Billie Thompson ** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **Jay Rubenstein** *Initial work*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GPL3 

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
