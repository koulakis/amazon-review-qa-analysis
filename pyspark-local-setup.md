# Setup jupyter notebook & pyspark

## Prerequisites

1. MacOS or Linux operating system (otherwise follow the links for other operating systems)
1. All the prerequisites from the installed packages

## Notes

1. Accept the instructions with a grain of salt. I used them a couple of months ago on my linux machine.
1. If you get stuck you can look in this [guide](https://blog.sicara.com/get-started-pyspark-jupyter-guide-tutorial-ae2fe84f594f) 
1. For the changes on `~/.bashrc` you need to load a new shell or run `source ~/.bashrc`

## Setup

1. Install Anaconda
    - Download [anaconda](https://www.continuum.io/downloads)
    - Follow the [interactive installer](https://docs.continuum.io/anaconda/install/mac-os) steps
1. Run jupyter notebook
    - After installing anaconda, [jupyter notebook](jupyter notebook) should be lanched on your default browser by running the following command on the terminal: `jupyter notebook`
1. Install spark - it will include pyspark
    - Download spark from [here](http://spark.apache.org/downloads.html) using the default options
    - Extract and move spark to some directory where you store applications (e.g. /opt):
    
        ```tar -xzf <downloaded filename>.tgz```
        
        ```mv <downloaded filename> /opt/spark-<version>```
    - Export the bin path. To do that append the following lines in the `~/.bashrc` file (or any other shell config file you use):
        ```
        export SPARK_HOME=/opt/<downloaded filename>
        export PATH="$SPARK_HOME/bin:$PATH"
        ```
        
1. The `pyspark` command enters per default the pyspark repl on the terminal. To run it on jupyter notebook you need to pass some environmental variables. One way to make this efficient is to append the following lines, again in `~/.bashrc`:
    ```
    alias pyspark-notebook="PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook' pyspark"
    ```
    Then you can launch it with the command `pyspark-notebook`.
