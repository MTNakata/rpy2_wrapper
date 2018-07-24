# rpy2_wrapper
Rpy2 wrapper for statistical analysis by R

#Introduction

rpy2_wrapper is a tool for calling R statistical functions from Python.

I've implemented this as a wrapper for the Rpy2 package (), so we named `rpy2_wrapper`. Basically I made it for myself. But anyone can use it if you build the enviroment.


#Topics

1. Motivation for development
2. What does `rpy2_wrapper` enable us to do?
3. Procedure for environment building

#1. Motivation for development

When statistically analyzing with Python, I usually use `scipy.stats`. Although this is convenient and useful, it lacks some statistical functions (mainly multiple comparisons).

`rpy2_wrapper` has made some of R's statistical functions available in Python. Many of the functions of the R package have proven results and there is a sense of security. Basically, `rpy2_wrapper` is just a` Rpy2` wrapper.

#2. What does `rpy2_wrapper` enable us to do?

The statistical functions implemented by `rpy2_wrapper` are listed below. Some are available in `scipy.stats`.

Function (R code)

- ANOVA (`aov`, `anova`)
- Tukey-Kramer test (`TukeyHSD`)
- Welch's ANOVA (`oneway.test` with `var.equal=False`)
- Steel-Dwass test (`pSDCFlig` with `method="Monte Carlo"` from `NSM3` package)
- Fisher's Exact Test (`fisher.test`)

#3. Procedure for environment building

###Environment

- MacOS Sierra
- Xcode9.1
- Python 3.6.6
- R version 3.5.1

###Python packages

- jupyter==1.0.0
- jupyterlab==0.32.1
- pandas==0.23.3
- rpy2==2.9.4

###R packages

- multcomp
- NSM3

###Install R

First of all, install R as `homebrew` so that it can be referenced from Python.
Install it separately from the Standalone version of R.

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

`brew link` to deal with the error.

```
$ brew link --overwrite r
```

###Install R packages

Run R in Terminal.

```
$ r
```
```r
R version 3.5.1 (2018-07-02) -- "Feather Spray"
Copyright (C) 2018 The R Foundation for Statistical Computing
Platform: x86_64-apple-darwin16.7.0 (64-bit)

...
```
When R opens, install the packages, `multcomp` and` NSM 3`..

```r
> install.packages("multcomp")
> install.packages("NSM3")
```

###Install Rpy2 and Pandas

Install them with `pip`.

```
$ pip install rpy2
$ pip install pandas
```
Jupyter and Jupyterlab are also installed.

```
$ pip install jupyter
$ pip install jupyterlab
```

###Install rpy2_wrapper

Go to the appropriate directory with `cd` command and run `git clone`.

```
$ git clone https://github.com/MTNakata/rpy2_wrapper/
```

The `rpy2_wrapper` directory is downloaded, in which a Python file (` rpy2_wrapper.py`) and a usage example (`examples.ipynb`) are included.

###Test

Go to the `rpy2_wrapper` directory in Terminal and start Jupyterlab.

```
$ jupyter lab
```

Select `examples.ipynb` from the screen on the left and open it by double clicking.


Execute `Kernel> Restart Kernel and Run All Cells` from the above tab.

If everything runs without errors, the environment building is going well.
