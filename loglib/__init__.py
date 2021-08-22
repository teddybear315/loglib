from neotermcolor import cprint
from datetime import *
import sys, os
__version__ = "1.2.1"
__author__ = 'Logan Houston'
class Logger:
	"""
    Flags in order of bit placement, LTR
    ex: 0b1010 =
    	verbose = True, whitespace = False, channels = True, 256 = False
	"""
    use_file = False
    verbose = False
    use_whitespace = True
    use_channels = True
    use_256 = False

    levels = {"LOG": ('white', 15), "WRN": ('yellow', 11), "ERR":('red', 9)}
    GLOBAL_CHANNEL = 0 # if observing channel shows all messages, if message sent it will always show
    DEFAULT_CHANNEL = GLOBAL_CHANNEL
    current_channel = DEFAULT_CHANNEL
    flags = 0

    def __init__(self, use_256 = False, use_channels = False, use_whitespace =
                False, use_verbose = False, use_file = False, file_dir = "./logs/", file_type = ".log", file_name = "%Y-%m-%d %H-%M-%S", flags = 0):"""
		Decent logging system that has a few options

		Args:
			use_256 (bool, optional): Use 256 color palette instead of 16, use if you experience color issues. Defaults to False.
			use_channels (bool, optional): Use output channels. Defaults to False.
			use_whitespace (bool, optional): Use whitespace in log. Defaults to False.
			use_verbose (bool, optional): Print extra information. Defaults to False.
			use_file (bool, optional): Use output file. Defaults to False.
				file_dir (str, required if use_file True): Directory of log file. Defaults to "./logs/".
				file_type (str, required if use_file True): File extension, doesn't change output format. Defaults to ".log".
				file_name (str, required if use_file True): Log file name, passed through datetime.now.strftime(). Defaults to "%Y-%m-%d %H-%M-%S".
			flags (int, optional): Fast way to setup parameters, bit order RTL reverse order of parameters. Defaults to 0.
		"""
        if flags:
            self.flags = flags
            if flags & 1 == 1: self.use_256 = True
            if flags & 2 == 2: self.use_channels = True
            if flags & 4 == 4: self.use_whitespace = True
            if flags & 8 == 8:
                self.verbose = True
                print("Logger setup flags:", f"{self.use_256=}", f"{self.use_channels=}", f"{self.use_whitespace=}")
            if flags & 16 == 16:
                self.use_file = True
        else:
            self.use_256 = use_256
            self.use_channels = use_channels
            self.use_whitespace = use_whitespace
            self.use_verbose = use_verbose
            self.use_file = use_file
            self.flags = self._generate_flags()
        if self.use_file:
            self.log_path = os.path.abspath(file_dir)
            if not os.path.isdir(self.log_path):
                print("Log dir doesn\'t exist, creating one...")
                os.mkdir(self.log_path)
            self.file_name = datetime.now().strftime(file_name) + file_type
            self.log_file = self.log_path + "/" + self.file_name

    def log(self, message: str, lvl: str = "LOG", timestamp: datetime = None, nt_attrs =
            [], prefix = "", prefixes = [], channel = DEFAULT_CHANNEL):
		"""
		Log a message

		Args:
			message (str): Output message
			lvl (str, optional): Output level/type. Defaults to "LOG".
			timestamp (datetime, optional): If None, gets current time. Defaults to None.
			nt_attrs (list, optional): NeoTerm attributes. Defaults to [].
			prefix (str, optional): Custom message prefix. Defaults to "".
			prefixes (list, optional): Array of custom message prefixes, similar to lvl and channel. Defaults to [].
			channel ([type], optional): Channel to output to, think radio frequencies. Defaults to DEFAULT_CHANNEL (0).
		"""
        if self.current_channel != self.GLOBAL_CHANNEL and channel not in [self.GLOBAL_CHANNEL, self.current_channel]: return
        if prefixes: prefix = ", ".join(prefixes)
        if not timestamp: timestamp = str(datetime.now(timezone.utc))[:19]
        message = f"{self._()}{timestamp}: {message}"
        if prefix: message = f"{self._()}[{prefix}]{message}"
        if self.use_channels: message = f"{self._()}[{channel}]{message}"
        if self.verbose:
            print("Logger print args:", f"{nt_attrs=}", f"{prefix=}", f"{channel=}",
                   f"color={self.levels[lvl.upper()][int(self.use_256)]}")
        cprint(f"[{lvl}]"+message, self.levels[lvl.upper()][int(self.use_256)], attrs=nt_attrs)
        if self.use_file:
            with open(self.log_file) as lf:
                lf.write(f"[{lvl}]"+message+os.linesep)
                lf.close()

    def err(self, message: str, timestamp: datetime = None, nt_attrs =
            [], prefix = "", prefixes = [], channel = DEFAULT_CHANNEL):
            """
			Shorthand function for predefined logging levels
			See Logger.log
			"""
			self.log(message, "ERR", timestamp, nt_attrs, prefix, prefixes, channel)

    def warn(self, message: str, timestamp: datetime = None, nt_attrs =
            [], prefix = "", prefixes = [], channel = DEFAULT_CHANNEL):
            """
			Shorthand function for predefined logging levels
			See Logger.log
			"""
            self.log(message, "WRN", timestamp, nt_attrs, prefix, prefixes, channel)

    def _(self, override = 0):
		"""
		Function that enforces use_whitespace option
		
		Returns:
			str: Space char if override or use_whitespace, else \'\'
		"""
        return ' ' if (override or self.use_whitespace) else ''

    def set_flags(self, new_flags = 0):
		"""
		Set option flags

		Args:
			new_flags (int, optional): Flag bits. Defaults to 0.

		Returns:
			int: Flag int
		"""
        if self.verbose:
            print("Logger old flags:", self.flags)
            print("Logger new flags:", new_flags)
        self.__init__(flags=new_flags)
        return new_flags

    def _generate_flags(self) -> int:
		"""
		Generates flag int from current settings

		Returns:
			int: Flag int
		"""
        return self.use_256 + (self.use_channels*2) + (self.use_whitespace*4) + (self.verbose*8) + (self.use_file*16)

    def observe_channel(self, new_channel=0):
		"""
		Send messages to custom channels so you dont have to see them all at once

		Args:
			new_channel (int, optional): Channel to observe, 0 is global. Defaults to 0.
		"""
        if self.verbose: print("Logger channel change:", new_channel)
        self.current_channel = new_channel

    def add_level(self, key, color_tuple):
		"""
		Add custom logging level
		Levels are a way to set a word/3 letter value to a color set to be able to use colors and change lvl prefix

		Args:
			key (str): Level name, used in parameters
			color_tuple (tuple): Colors to use (16-bit-color-str, 256-palette-color-int)
		See NeoTerm/TermColor docs for more info on `color_tuple`

		Returns: color_tuple
		"""
        self.levels[key] = color_tuple
        if self.verbose: print("Level added, all log levels:", self.levels)
        return color_tuple

def _bis(boolean) -> str: return str(int(boolean))
