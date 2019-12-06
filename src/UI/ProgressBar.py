from src.utils.Singleton import Singleton

class ProgressBar(Singleton, object):

    def print(self, iteration, total, suffix=''):
        """
        from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
        """
        decimals = 1
        length = 50
        fill = '█'
        print_end = "\r"
        prefix = ''
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()
