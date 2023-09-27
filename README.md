# Visual Analytics Lab Project
Submission for the Visual Analytics lab project at the Johannes Kepler University Linz.

## General Information

### Group Members

| Student ID    | First Name  | Last Name      | E-Mail             | Workload [%]  |
| --------------|-------------|----------------|--------------------|---------------|
| k01547577     | Hanna      | Messner         |hannajuni@web.de                |10%|
| k12017433     | Ádám       | Párkányi        |adam.parkanyi@gmail.com         | 0%|
| k12137202     | Mohamed    | Abdelaziz       |mohamed.yz.abdelaziz@gmail.com  |70%|
| k12104744     | Ivan       | Drinovac        |drinovacivan1@gmail.com         |20%|

### Dataset

* What is the dataset about?
* Where did you get this dataset from (i.e., source of the dataset)?
* How big is the dataset?

**Description:**
It is about historical data of various causes of deaths across different countries along the timeline from 1990 up until 2019.
This Dataset is created from Our World in Data. https://ourworldindata.org/. Composed of 34 Columns, covering 204 Countries from 1990-2019 with around 200000 different datapoints.


## General Submission Information

* Make sure that you pushed your GitHub repository and not just committed it locally.
* Sending us an email with the code is not necessary.
* Please update the *environment.yml* file if you need additional libraries, otherwise the code is not executeable.
* Save your executed submission notebooks as HTML and add them to your repository.  
  * Select 'File' -> 'Save and Export Notebook As...' -> 'HTML'
* Upload the exported HTML file on Moodle, if it is required for the submission.

## Usage

### Locally
Checkout this repo and change into the folder:

```shell
git clone https://github.com/jku-icg-classroom/va-project-2022-thefantasticfour.git
cd va-project-2022-thefantasticfour
```

Load the conda environment from the `environment.yml` file, if you haven't already in previous assignments:

```sh
conda env create -f environment.yml
```

Activate the loaded conda environment:

```sh
conda activate python-tutorial
```

Install Jupyter Lab extension to use *ipywidgets* in JupyterLab:

```sh
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

Launch Jupyter :

```shell
jupyter lab
```

Jupyter should open a new tab with url http://localhost:8888/ and display the tutorial files.



