# 0. Introduction

rpy2_wrapper is a module to use several R statistical functions from Python programs. rpy2_wrapper has been implemented as a wrapper for the Rpy2 package.

Rpy2: https://rpy2.bitbucket.io  
Rpy2 documentation: http://rpy2.readthedocs.io/en/version_2.8.x/

### Topics

1. Purpose
2. What is contained in rpy2_wrapper?
3. Building the development environment
4. Test

# 1. Purpose

rpy2_wrapper makes six statistical functions of R available from Python programs. For statistical analysis, scipy.stats is generally used in the Python field. rpy2_wrapper was implemented to supplement statistical functions not available in scipy.stats.

# 2. What is contained in rpy2_wrapper?

The statistical functions in rpy2_wrapper are listed below.

Function (R code)

- ANOVA (`aov` function and `anova` function)
- Tukey-Kramer test (`TukeyHSD` function)
- Welch's ANOVA (`oneway.test` function with `var.equal=False`)
- Dunnett's test (`glht` function from `multcomp`)
- Steel-Dwass test (`pSDCFlig` function with `method="Monte Carlo"` from `NSM3`)
- Fisher's Exact Test (`fisher.test` function)

`multicomp`: https://cran.r-project.org/web/packages/multcomp/index.html  
`NSM3`: https://cran.r-project.org/web/packages/NSM3/index.html

To understand how to use each function, see the contents of `examples.ipynb` on Jupyter notebook. There is also a method to save the output result as a text file without displaying it on the screen (see the contents of `save_test.ipynb`).

# 3. Building the development environment

### Our Development Environment

- MacOSX Sierra (maybe other versions of MacOSX are OK)
- Xcode9.1
- Python 3.6.6
- R version 3.5.1

### Python packages

- pandas==0.23.3
- rpy2==2.9.4

### R packages

- multcomp
- NSM3

### a. Install R with homebrew

First of all, install the package manager for MacOS `homebrew` according to the following URL.

`homebrew`: https://brew.sh

Then, install R by the `brew` command on Terminal (not the standalone version of R).

```
$ brew install R
```
```
...

Error: The `brew link` step did not complete successfully
The formula built, but is not symlinked into /usr/local
Could not symlink bin/Rscript
Target /usr/local/bin/Rscript
already exists. You may want to remove it:
  rm '/usr/local/bin/Rscript'

To force the link and overwrite all conflicting files:
  brew link --overwrite r

To list all files that would be deleted:
  brew link --overwrite --dry-run r

Possible conflicting files are:
/usr/local/bin/Rscript -> /Library/Frameworks/R.framework/Resources/bin/Rscript
==> Summary
🍺  /usr/local/Cellar/r/3.5.1: 2,116 files, 55.6MB
==> Caveats
==> readline
This formula is keg-only, which means it was not symlinked into /usr/local,
because macOS provides the BSD libedit library, which shadows libreadline.
In order to prevent conflicts when programs look for libreadline we are
defaulting this GNU Readline installation to keg-only.

For compilers to find this software you may need to set:
    LDFLAGS:  -L/usr/local/opt/readline/lib
    CPPFLAGS: -I/usr/local/opt/readline/include
```

Run `brew link` to deal with the error.

```
$ brew link --overwrite r
```

### b. Install R packages

Start R on Terminal.

```
$ r
```
```r
R version 3.5.1 (2018-07-02) -- "Feather Spray"
Copyright (C) 2018 The R Foundation for Statistical Computing
Platform: x86_64-apple-darwin16.7.0 (64-bit)

...
```
When R opens, install two R packages, i.e. `multcomp` and` NSM3`.

```r
> install.packages("multcomp")
> install.packages("NSM3")
```

### c. Install Python packages

Install Rpy2 and Pandas with the `pip` command.

```
$ pip install rpy2
$ pip install pandas
```

### d. Install rpy2_wrapper

Move to the appropriate directory with `cd` command and run `git clone`.

```
$ git clone https://github.com/MTNakata/rpy2_wrapper/
```

Then the `rpy2_wrapper` directory starts to be downloaded. You can find a source code of the main program (`rpy2_wrapper.py`) and several sample programs/files (`examples.py`, `examples.ipynb`, `sample_data.csv` etc.) in the directory.

# 4. Test

For the test, enter the `rpy2_wrapper` directory and run `examples.py` on Terminal.

```
$ python examples.py
```

