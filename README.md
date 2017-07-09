# Scopy

Python script for searching through your digital books and cataloguing them in an easy-to-share list of files.

&nbsp;

## How To Use

### Basic usage:

```bash
$ python scopy.py
```
Searches current folder and all its subfolders for .epub, .mobi, and .pdf files. Outputs the results to the console:

```
Filename:                                          Ext:     Size:    Relative path:
Epub In First Sub                                  .epub    515  B   /first_subdirectory
Epub In Second Sub                                 .epub      3 KB   /second_subdirectory
Mobi In First Sub                                  .mobi      2 KB   /first_subdirectory
Pdf In Dir                                         .pdf      63 KB
Pdf In Second Sub                                  .pdf       1 KB   /second_subdirectory
```

If you want to save the results in the easy to share file, provide the `--outfile` (`-o`) argument:

```bash
$ python scopy.py -o my_books.txt
```
---

The list of all options can be seen by calling `help` with:
```bash
$ python scopy.py -h
```

```
usage: scopy.py [-h] [-d DIR] [-e [EXT [EXT ...]]] [-c] [-f [F [F ...]]]
                [-m N] [-i [DIR [DIR ...]]] [-r] [-s [S [S ...]]] [-z] [-v]
                [-o FILE]

Catalogue your digital books (and more)

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --directory DIR
                        Path to the directory you want to scan. Default:
                        current directory
  -e [EXT [EXT ...]], --ext [EXT [EXT ...]]
                        Choose wanted file extensions. Default: ['pdf',
                        'epub', 'mobi']
  -c, --current         Scan just the current directory, without subfolders.
                        Default: False
  -f [F [F ...]], --filter [F [F ...]]
                        Filter results to include only the filenames
                        containing these words. Default: None
  -m N, --minsize N     Include only the files larger than the provided size
                        (in bytes). Can use suffixes `k`, `m`, and `g` for
                        kilo-, mega-, and giga-bytes. For example: 64k.
                        Default: 0
  -i [DIR [DIR ...]], --ignore [DIR [DIR ...]]
                        Ignores subdirectories containing these words.
                        Default: None
  -r, --raw             Keep the original filenames, don't change to Title
                        Case, and don't replace symbols such as -, _, +, etc.
                        Default: False
  -s [S [S ...]], --sort [S [S ...]]
                        Sort files by: [n]ame, [e]xtension, [s]ize,
                        [d]irectory, or their combination. Default: by Name
  -z, --descending      Sort file descending: from Z to A, from larger to
                        smaller. Default: False
  -v, --verbose         Output summary statistics at the top. Default: False
  -o FILE, --outfile FILE
                        Choose an output file to save the results. Default:
                        None, prints to console
```


### More examples

```bash
$ python scopy.py -e pdf -i first
```
Searches current folder and all its subfolders for files with `.pdf` extension (`-e`), ignoring subdirectories (`-i`) containing the word `first`:

```
Filename:                                          Ext:     Size:    Relative path:
Pdf In Dir                                         .pdf      63 KB
Pdf In Second Sub                                  .pdf       1 KB   /second_subdirectory
```

---

```bash
$ python scopy.py -f sub -s d e n -r -v
```
Filter (`-f`) the results to only the filenames including the word `sub`, sort by (`-s`) directory (`d`), then extension (`e`), then name (`n`). Keep raw (`-r`) filenames (without Title Case and without replacing symbols). Make verbose (`-v`) output:

```
Scanned directory:                  [absolute path]/scopy/scopy_example
Looking for files containing:       sub
With extensions:                    .epub, .pdf, .mobi
Found:                              4 files


Filename:                                          Ext:     Size:    Relative path:
epub_in_first_sub                                  .epub    515  B   /first_subdirectory
mobi_in_first_sub                                  .mobi      2 KB   /first_subdirectory
epub_in_second_sub                                 .epub      3 KB   /second_subdirectory
pdf_in_second_sub                                  .pdf       1 KB   /second_subdirectory
```

---

```bash
$ python scopy.py -d D:/Documents/Books -c -o book_list.txt
```

Scan `D:/Documents/Books` folder (both absolute and relative paths can be used), without subfolders (`-c`), and save the results in the output file (`-o`) called `book_list.txt`.

&nbsp;

## Installation

### Requirements

Python 3.4+

No other dependencies.

### Install

Clone this repo:
```bash
git clone https://github.com/narimiran/scopy.git
```
or just manually download the file [`scopy.py`](scopy.py).

&nbsp;

## FAQ

> Why the name Scopy?

From the Greek verb σκοπέω (skopéō), meaning "I search". The suffix `py` is, of course, because of Python.

> Can't I just use X or Y, to get the same (or better) result?

You probably can. Scopy was done as a fun weekend project to practice my Python skills. It wasn't meant to be groundbreaking.

> Is there really a limit to search only for digital books? Can't I just search for any extension?

Scopy was started because I wanted to catalogue my .pdf collection, but as you figured it out - it can be used to search any format you like.

&nbsp;

## License

MIT License.  
See the details at [LICENSE](/LICENSE.txt).
