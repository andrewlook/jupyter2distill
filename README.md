# jupyter2distill

Utility for converting a jupyter/colab notebook into a publishable static site codebase

## Installation

```
pip install jupyter2distill

# install latest directly f/ github
pip install git+https://github.com/andrewlook/jupyter2distill.git#egg=jupyter2distill
```

## Usage

### Downloading Notebooks from Google Colab

Here's a way to download notebooks from Google Colab and extract some metadata in the
process (author, modified date, etc) to be used when rendering the templates. This
metadata can be stored as JSON alongside the downloaded notebook file.
```
jupyter2distill download \
    --colab-url <url> \
    --output-dir ./notebooks 
```

TODOs:
- describe PyDrive setup for this

### Initializing a Static Site Repository

Often we'll want to bootstrap a git repository into which we can download our notebook
and run the conversion.
```
jupyter2distill init_repo \
    --notebook ./notebooks/test.ipynb \
    --metadata ./notebooks/test.ipynb.meta \
    --cookiecutter-url <url>
```

TODOs:
- add reference to sample cookiecutter URLs
- github integration?

### Producing an Example Template for Jupyter nbconvert

It's likely that the jupyter nbconvert template may need some tweaks. So we recommend
dumping the nbconvert template into the repo and making any necessary modifications
in the template. This can streamline the process of re-rendering from a notebook.
```
jupyter2distill template \
    --type distill_v2 \
    --output_path ./templates

# outputs to './templates/distill_v2.tpl'
```

TODOs:
- add reference for where to learn about nbconvert formatting, reference `basic.tpl`

### Rendering the Jupyter Notebook

Finally, actually running the renderer.

```
jupyter2distill render \
    --notebook-src ./notebooks/test.ipynb \
    --render-dest <cookiecutter repo root>/public/index.html \
    --notebook-dest <cookiecutter repo root>/notebooks/ \
    --images-dest <cookiecutter repo root>/public/images
```

## License

This project is distributed under the MIT license.
