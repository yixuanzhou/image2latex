# im2latex-dataset
Python tools for creating suitable dataset for OpenAI's im2latex task: https://openai.com/requests-for-research/#im2latex.
You can download a prebuilt dataset from [here](https://zenodo.org/record/56198#.V2px0jXT6eA). The data is split into train (~84k), validation (~9k) and test (~10k) sets, which possibly
isn't quite enough for this task. I can build bigger sets on request.

**Note: This code is very ad-hoc and requires tinkering with the source**

## Ultimate goals
- To provide dataset suitable for solving im2latex task
  - So people can compare performances between systems
- To provide the tools used to generate said dataset
  - So people can generate different kind of images (quality, size), different formulas (different fonts), etc
- Misc tools for handling the datasets
  - TeX Math tokenizer (possibly)
  - Performance metric (takes list of true formulas and list of estimated formulas, outputs performance/accuracy)
  - Tools for modifying the images in wanted way

## Contents

- `/src/latex2formulas.py`
  - Script for parsing downloaded latex sources for formulas. Stores formulas in single .txt file (one formula per line)
- `/src/stackexchange2formulas.py`
  - Similar to `latex2formulas.py`, but for parsing StackExchange XMLs.
- `/src/arxiv2formulas.py`
  - Similar to `latex2formulas.py`, but for parsing arXiv .tar/.tar.gz files (source downloads).
- `/src/formula2image.py`
  - Creates images and dataset from a file of formulas
- `/src/im2latex_utils.py`
  - Collection of misc functions for handling these formulas
- `latex_urls.txt`
  - Text file containing urls to LaTeX dataset from [here](http://www.cs.cornell.edu/projects/kddcup/datasets.html). Use `wget -i latex_urls.txt` to download these files.
  
## Dependencies 
- Python 2.x or 3.x (only ran on 2.x, should work on 3.x too. Haven't tried running on Windows)
- For running the script with current settings and generating full-page images:
    - Properly installed LaTeX-to-PDF chain (eg. calling `pdflatex` outputs .pdf for .tex file) 
    - [ImageMagick](http://www.imagemagick.org/script/index.php) installed so that `convert` command works
- For creating more compact images of formulas (image cropped so that formula fits)
    - [textogif](https://www.fourmilab.ch/webtools/textogif/textogif.html) and its dependencies
    - `textogif` needs to be placed in same directory where images are generated, otherwise it won't work.

## Building your own dataset
1. Download bunch of LaTeX sources packed in .tar files (by using the latex_urls.txt, for example)
2. Run `python latex2formulas.py [directory where .tars are stored]`
3. Run `python formula2image.py [path to generated formula text file]`
4. Run `python formula2image.py [dataset_file] [formula_file] [image_dir]` to confirm dataset is valid

- The end result should have two files and one directory (names can be changed in `formula2image.py`:
  - `im2latex.lst`
    - Each line is in format `formula_idx image_name render_type`
      - formula_idx is the line number where formula is in `im2latex_formulas.lst`
      - image_name is the name of the image connected to this rendering (without '.png')
      - render_type is the name of render setup used, defined in `formula2image.py`
  - `im2latex_formulas.lst`
    - Each line contains one formula
  - `/formula_images` 
    - Directory where images are stored

- Sometimes pdflatex gets stuck inside an infinite loop when compiling an image.
  - To fix this you need to manually kill stuck pdflatex processes, otherwise script won't end
  
## Issues and possible TODOs
- If `pdflatex` is used with `convert` this will generate pictures of whole page
    - While this might be a good thing (eg. fixed input size), it might also severly slow down training
- `textogif` generates smaller images but these will have varying dimensions.

- Possible TODOs:
  - Finish tokenizer function / output list of tokens instead of raw formula in formula list
  - Add accuracy metric (eg. word-error-rate or similar).
    - Check this repository for some evaluation scripts: https://github.com/harvardnlp/im2markup
  - Combine `...2formula.py` scripts into one, or at least make system more sensible rather than bunch of separate scripts.
