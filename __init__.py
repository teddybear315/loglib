from neotermcolor import cprint
from datetime import *
import sys

class Logger:
    # flags in order of bit placement, LTR
    # ex: 0b1010 =
    # verbose = True, whitespace = False, channels = True, 256 = False
    verbose = False # prints all unseen modifiable variables
    use_whitespace = False
    use_channels = False
    use_256 = False
    # end flags

    levels = {"LOG": ('white', 15), "WRN": ('yellow', 11), "ERR":('red', 9)}
    GLOBAL_CHANNEL = 0 # if observing channel shows all messages, if message sent it will always show
    DEFAULT_CHANNEL = GLOBAL_CHANNEL
    current_channel = DEFAULT_CHANNEL
    flags = 0

    def __init__(self, use_256 = False, use_channels = False, use_whitespace =
                False, flags = 0):
                # Decent logging system that has a few options
                # If you experience compatibility issues please try toggling use_256 either via flags or args
                # flag bits in order of: verbose, use_whitespace, use_channels, use_256
        if flags:
            self.flags = flags
            if flags & 1 == 1: self.use_256 = True
            if flags & 2 == 2: self.use_channels = True
            if flags & 4 == 4: self.use_whitespace = True
            if flags & 8 == 8:
                self.verbose = True
                print("Logger setup flags:", f"{self.use_256=}", f"{self.use_channels=}", f"{self.use_whitespace=}")
        else:
            self.use_256 = use_256
            self.use_channels = use_channels
            self.use_whitespace = use_whitespace
            self.flags = self._generate_flags()


    def log(self, message: str, lvl: str = "LOG", timestamp: datetime = None, nt_attrs =
            [], prefix = "", prefixes = [], channel = DEFAULT_CHANNEL):
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

    def err(self, message: str, timestamp: datetime = None, nt_attrs =
            [], prefix = "", prefixes = [], channel = DEFAULT_CHANNEL): # Shorthand function for predefined logging levels
            self.log(message, "ERR", timestamp, nt_attrs, prefix, prefixes, channel)

    def warn(self, message: str, timestamp: datetime = None, nt_attrs =
            [], prefix = "", prefixes = [], channel = DEFAULT_CHANNEL): # Shorthand function for predefined logging levels
            self.log(message, "WRN", timestamp, nt_attrs, prefix, prefixes, channel)

    def _(self, override = 0):
        return ' ' if (override or self.use_whitespace) else ''

    def set_flags(self, new_flags = 0):
        # Set option flags
        #
        # Keyword arguments:
        # flags -- flag bits (default 0)
        # Returns flags
        if self.verbose:
            print("Logger old flags:", self.flags)
            print("Logger new flags:", new_flags)
        self.__init__(flags=new_flags)
        return new_flags

    def _generate_flags(self) -> int:
        # Returns flag int based on current settings
        return self.use_256 + (self.use_channels*2) + (self.use_whitespace*4) + (self.verbose*8)

    def observe_channel(self, new_channel=0):
        # Send messages to custom channels so you dont have to see them all at once
        #
        # Keyword arguments:
        # new_channel -- channel you want to observe, 0 is all (default 0)
        if self.verbose: print("Logger channel change:", new_channel)
        self.current_channel = new_channel

    def add_level(self, key, color_tuple):
        # Add custom logging level
        #
        # Keyword arguments:
        # key -- name for level (2nd print arg)
        # color_tuple -- ('16 color string', 256_color_int)
        # Returns color_tuple
        #
        # Levels are a way to set a word/3 letter value to a color set to be able to identify what message means what
        self.levels[key] = color_tuple
        if self.verbose: print("Level added, all log levels:", self.levels)
        return color_tuple

def _bis(boolean) -> str: return str(int(boolean))
