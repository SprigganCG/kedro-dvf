# kedro-dvf

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

Ce code lance un pipeline python qui charge et prépare automatiquement les données dvf de valeur foncieres françaises publiées en open data couvrant la période 2020-2024. Ce pipeline génère en sortie les valeurs medianes des ventes pour chaque commune, pour chaque année.(un fichier pour les maisons, un second pour les appartements)


## How to run this pipeline locally

This repo contains a kedro pipeline named 'data_processing'. Just run kedro and the code will download the data, process them and generate the output in the data folder of your computer.

Your computer must have enough disk space (data will be loaded into data folder), and enough ram to process.(tested only on a 16gb ram machine)

From terminal

- Clone this repository

```
git clone https://github.com/SprigganCG/kedro-dvf.git
```

- Setup a virtualenv inside the repository and activate it
```
python -m venv .venv
source .venv/bin/activate
```

- install requirements from the kedro folder
```
cd kedro-dvf
pip install -r requirements.txt
```

- test the installation


```
kedro info
```

- You can run your Kedro project with:

```
kedro run
```

- When the pipeline has finished successfully, check the created parquet datasets with visidata
```
visidata
```



## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, 'session', `catalog`, and `pipelines`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.
