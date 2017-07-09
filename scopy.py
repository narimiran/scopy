import argparse
import os
import re


class Scopy:
    """Object which holds parsed arguments, and depending on them searches for files.

    Public methods:
        run: runs all other public methods
        get_results: searches for files satisfying the provided criteria
        sort_results: sorts the results based on the `sort_by` argument
        format_results: formats content into columns, trims too long columns
        output_results: outputs formatted content
    """
    def __init__(self, args):
        self.directory = args.directory.replace('\\', '/')
        self.ext = self._set_extensions(args.ext)
        self.no_subs = args.no_subs
        self.filters = args.filters
        self.ignore = args.ignore
        self.minsize = self._set_minsize(args.minsize)
        self.raw = args.raw
        self.sort_by = args.sort_by
        self.descending = args.descending
        self.verbose = args.verbose
        self.outfile = self._set_outfile(args.outfile)

    def run(self):
        """The main method, used to run all other methods.

        Checks if the provided directory is valid and gets the results, based on
        the given criteria.
        Sorts the results based on `sort_by` attribute.
        Formats the sorted results in the columns.
        Outputs the formatted content either to console or to provided outfile.

        See other public methods for more information.
        """
        results = self.get_results()
        if results:
            sorted_results = self.sort_results(results)
            formatted_content = self.format_results(sorted_results)
            self.output_results(formatted_content)

    def get_results(self):
        """Gets the results for the provided arguments.

        Checks if the provided directory is valid.
        If it is not, prints the warning to the console and returns None.

        Otherwise:
        Depending on `no_subs` attribute, either gets the results only from
        the current directory or the current directory and all its subdirectories.
        Returns the results satisfying the provided criteria (extensions, filenames),
        as the list of tuples (filename, extension, size, path).
        """
        if os.path.isdir(self.directory):
            return self._search_directory(self.directory) if self.no_subs else self._search_all()
        else:
            print('{} is not a valid directory!'.format(self.directory))

    def sort_results(self, results):
        """Sorts the results based on the `sort_by` attribute.

        Args:
            results: list of 4-tuples (filename, extension, size, path)
                     provided by `get_results` method

        Columns can be sorted by name, extension, directory, or any combination
        of those. For example: first sort by directory, then by name.
        Returns the sorted list of tuples.
        """
        translate = {
            'n': 0,
            'e': 1,
            's': 2,
            'd': 3,
        }
        sort_order = lambda x: [x[translate[column]] for column in self.sort_by]
        return sorted(results, key=sort_order, reverse=self.descending)

    def format_results(self, results):
        """Formats the results in four columns. Trims too long columns.

        Args:
            results: list of 4-tuples (filename, extension, size, path)
                     provided by `sort_results` (or `get_results`) method

        Too long filenames are trimmed to fit in the `MAX_WIDTH`.
        Subdirectories in too long paths are stripped until path can fit in
        the `MAX_WIDTH`.
        The value for `MAX_WIDTH` is chosen in such way that the total width of
        the output is less than 120 characters, so two outputs can be shown
        side by side on a typical computer screen.

        Returns a string containing all the results.
        """
        def _trimmed(filename, path):
            relative_path = path[HOME_LENGTH:].replace('\\', '/')
            if not self.raw:
                filename = self._replace_symbols(filename)

            if len(filename) > MAX_WIDTH:
                filename = filename[:MAX_WIDTH-3] + '...'
            if len(relative_path) > MAX_WIDTH:
                while len(relative_path) > MAX_WIDTH-3:
                    relative_path = relative_path[relative_path.find('/', 1):]
                relative_path = '...' + relative_path
            return filename, relative_path

        MAX_WIDTH = 50
        COLUMNS = '{0:<{WIDTH}} {2:<8} {3:<8} {1}'
        HOME_LENGTH = len(self.directory)

        column_names = COLUMNS.format(
            'Filename:', 'Relative path:', 'Ext:', 'Size:',
            WIDTH=MAX_WIDTH
        )
        results_string = '\n'.join(
            COLUMNS.format(
                *_trimmed(filename, path),
                ext,
                self._convert_bytes(size),
                WIDTH=MAX_WIDTH)
            for filename, ext, size, path in results)

        if self.verbose:
            header = self._get_header(results)
            return '\n\n\n'.join([header, '\n'.join([column_names, results_string])])
        else:
            return '\n'.join(['', column_names, results_string])

    def output_results(self, contents):
        """Outputs given content, either to a file or to the console.

        Args:
            contents: string with all the results
                      provided by `format_results` method

        If `outfile` attribute is provided, writes to a file.
        Otherwise, prints to the console.
        """
        self._write_to_file(contents) if self.outfile else print(contents)


    def _search_directory(self, directory):
        results = []
        for file in os.listdir(directory):
            filepath = os.path.join(directory, file)
            if os.path.isfile(filepath):
                filename, ext = self._split(file)
                filesize = os.path.getsize(filepath)
                if self._satisfies_filters(filename, ext, filesize):
                    results.append((filename, ext, filesize, directory))
        return results

    def _search_all(self):
        def _ignore_directories(dirs):
            for d in dirs:
                if any(word.lower() in d.lower() for word in self.ignore):
                    dirs.remove(d)
            return dirs

        results = []
        for path, dirs, _ in os.walk(self.directory):
            if self.ignore:
                dirs = _ignore_directories(dirs)
            results.extend(self._search_directory(path))
        return results

    def _satisfies_filters(self, filename, ext, filesize):
        is_valid_file = any(filt.lower() in filename.lower()
                            for filt in self.filters) if self.filters else True
        is_valid_ext = ext in self.ext
        is_valid_size = filesize >= self.minsize
        return is_valid_file and is_valid_ext and is_valid_size

    def _get_header(self, results):
        header = [('', '')]
        header.append(('Scanned directory:', os.path.abspath(self.directory).replace('\\', '/')))
        if self.ignore:
            header.append(('Ignoring subdirectories containing:', ', '.join(self.ignore)))
        if self.filters:
            header.append(('Looking for files containing:', ', '.join(self.filters)))
        header.append(('With extensions:', ', '.join(self.ext)))
        header.append(('Found:', '{} files'.format(len(results))))
        return '\n'.join('{0:<36}{1}'.format(*line) for line in header)

    def _write_to_file(self, contens):
        with open(self.outfile, 'w') as f:
            f.writelines(contens)
            f.writelines('\n\n\nCreated with Scopy. https://github.com/narimiran/scopy \n')
        print('Results saved in {}'.format(self.outfile))


    @staticmethod
    def _set_extensions(extensions):
        return {'.{}'.format(ext) if not ext.startswith('.') else ext
                for ext in extensions}

    @staticmethod
    def _set_minsize(minsize):
        def parse_size(size, multi=1):
            try:
                size = multi * int(size)
            except ValueError:
                print('WARNING: Not a valid format for file size!')
                print('Using the default value: 0\n')
                size = 0
            return size

        translate = {
            'k': 1024,
            'm': 1024**2,
            'g': 1024**3
        }
        if minsize[-1].isalpha():
            multiplier = translate.get(minsize[-1].lower(), 1)
            return parse_size(minsize[:-1], multiplier)
        else:
            return parse_size(minsize)

    @staticmethod
    def _set_outfile(outfile):
        if outfile:
            if outfile.find('.') == -1:
                return outfile + '.txt'
        return outfile

    @staticmethod
    def _split(file):
        ext_index = file.rfind('.')
        return file[:ext_index], file[ext_index:]

    @staticmethod
    def _replace_symbols(filename):
        return ' '.join(re.sub(r'[.$%_-]', ' ', filename).split()).title()

    @staticmethod
    def _convert_bytes(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return '{:3.0f} {:>2}'.format(size, unit)
            size /= 1024


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Catalogue your digital books (and more)"
    )

    parser.add_argument(
        '-d', '--directory',
        default='.',
        metavar='DIR',
        help='Path to the directory you want to scan. Default: current directory'
    )
    parser.add_argument(
        '-e', '--ext',
        default=['pdf', 'epub', 'mobi'],
        nargs='*',
        help="Choose wanted file extensions. Default: ['pdf', 'epub', 'mobi']",
    )
    parser.add_argument(
        '-c', '--current',
        action='store_true',
        dest='no_subs',
        help='Scan just the current directory, without subfolders. Default: False',
    )
    parser.add_argument(
        '-f', '--filter',
        default=None,
        metavar='F',
        nargs='*',
        dest='filters',
        help='Filter results to include only the filenames containing these words. '
             'Default: None',
    )
    parser.add_argument(
        '-m', '--minsize',
        default='0',
        metavar='N',
        help='Include only the files larger than the provided size (in bytes). '
             'Can use suffixes `k`, `m`, and `g` for kilo-, mega-, and giga-bytes. '
             'For example: 64k. Default: 0',
    )
    parser.add_argument(
        '-i', '--ignore',
        default=None,
        nargs='*',
        metavar='DIR',
        help='Ignores subdirectories containing these words. Default: None',
    )
    parser.add_argument(
        '-r', '--raw',
        action='store_true',
        help="Keep the original filenames, don't change to Title Case, and "
             "don't replace symbols such as -, _, +, etc. Default: False",
    )
    parser.add_argument(
        '-s', '--sort',
        default=['n'],
        choices=['n', 'e', 's', 'd'],
        nargs='*',
        metavar='S',
        dest='sort_by',
        help='Sort files by: [n]ame, [e]xtension, [s]ize, [d]irectory, '
             'or their combination. Default: by Name',
    )
    parser.add_argument(
        '-z', '--descending',
        action='store_true',
        help='Sort file descending: from Z to A, from larger to smaller. '
             'Default: False'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Output summary statistics at the top. Default: False',
    )
    parser.add_argument(
        '-o', '--outfile',
        default=None,
        metavar='FILE',
        help='Choose an output file to save the results. Default: None, prints to console',
    )
    return parser.parse_args()


def main():
    args = arg_parser()
    sc = Scopy(args)
    sc.run()


if __name__ == '__main__':
    main()
