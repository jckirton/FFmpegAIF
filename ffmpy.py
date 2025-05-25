class FFmpy:
    from os import system
    from sys import argv

    def __init__(self, *, pytest: list | None = None):
        self.pytest: bool = False

        if pytest is not None:
            self.pytest = True
            self.rawArgs = pytest
            self.args = pytest.copy()
        else:
            self.rawArgs = self.argv
            self.args = self.argv.copy()
            self.args.remove(self.args[0])

        self.debug: bool = False
        self.inFile: str | None = None
        self.outFile: str | None = None
        self.outVcodec: str | None = None
        self.inOptions: list = [].copy()
        self.outOptions: list = [].copy()

        try:

            if self.args[0] == "debug":
                self.debug = True
                while self.args[0] == "debug":
                    self.args.remove(self.args[0])

            if "-i" in self.args:
                self.inFile = self.args[self.args.index("-i") + 1]

            self.outFile = self.args[len(self.args) - 1]

            self.inOptions = self.args[: self.args.index("-i")]

            self.outOptions = self.args[
                self.args.index(self.inFile) + 1 : (len(self.args) - 1)
            ]

            if "-vcodec" in self.outOptions:
                self.outVcodec = self.outOptions[self.outOptions.index("-vcodec") + 1]
            elif "-c:v" in self.outOptions:
                self.outVcodec = self.outOptions[self.outOptions.index("-c:v") + 1]
            elif "-codec:v" in self.outOptions:
                self.outVcodec = self.outOptions[self.outOptions.index("-codec:v") + 1]
            else:
                self.outVcodec = None

            if self.outVcodec == "h264":
                self.args[self.args.index(self.outVcodec)] = "h264_videotoolbox"
                self.outOptions[self.outOptions.index(self.outVcodec)] = (
                    "h264_videotoolbox"
                )
                if "-q:v" not in self.outOptions and "-qscale:v" not in self.outOptions:
                    self.outOptions.append("-q:v")
                    self.outOptions.append("65")
                    # self.args.insert(self.args.index(self.outFile), "-q:v")
                    # self.args.insert(self.args.index(self.outFile), "65")
                if "-tag:v" not in self.outOptions and "-vtag" not in self.outOptions:
                    self.outOptions.append("-tag:v")
                    self.outOptions.append("avc1")
                    # self.args.insert(self.args.index(self.outFile), "-tag:v")
                    # self.args.insert(self.args.index(self.outFile), "avc1")
            if self.outVcodec == "hevc":
                # self.args[self.args.index(self.outVcodec)] = "hevc_videotoolbox"
                self.outOptions[self.outOptions.index(self.outVcodec)] = (
                    "hevc_videotoolbox"
                )
                if "-q:v" not in self.outOptions and "-qscale:v" not in self.outOptions:
                    self.outOptions.append("-q:v")
                    self.outOptions.append("65")
                    # self.args.insert(self.args.index(self.outFile), "-q:v")
                    # self.args.insert(self.args.index(self.outFile), "65")
                if "-tag:v" not in self.outOptions and "-vtag" not in self.outOptions:
                    self.outOptions.append("-tag:v")
                    self.outOptions.append("hvc1")
                    # self.args.insert(self.args.index(self.outFile), "-tag:v")
                    # self.args.insert(self.args.index(self.outFile), "hvc1")

        except Exception as err:
            print(err)

        self.sorted = {
            "debug": self.debug,
            "inOptions": self.inOptions,
            "inputFile": self.inFile,
            "outputVcodec": self.outVcodec,
            "outputOptions": self.outOptions,
            "outputFile": self.outFile,
        }

        self.runArgs = [].copy()
        for opt in self.inOptions:
            self.runArgs.append(opt)
        if self.inFile:
            self.runArgs.append("-i")
            self.runArgs.append(self.inFile)
        for opt in self.outOptions:
            self.runArgs.append(opt)
        self.runArgs.append(self.outFile)

        self.command = f"ffmpeg {" ".join(self.runArgs)}"

    def run(self, *, confirm: bool = False, debug: bool = False):
        """
        Actually running the ffmpeg command.

        Args:
            confirm (bool, optional): If confirmation dialog should be displayed before command execution. Defaults to False.
            debug (bool, optional): If the sorted arguments, raw sys.argv, and finished command should be printed, without command execution. Defaults to False.
            pytest (bool, optional): Streamlined debug output for pytest interpretation. Defaults to False.
        """
        if debug:
            self.debug = True

        if not confirm and not self.debug and not self.pytest:
            # print("Command Run", self.command)
            self.system(self.command)
        elif self.debug:
            print(f"\n\nSorted Arguments:\n{self}")
            print(f"\nProcessed Args:\n{self.runArgs}")
            print(f"\nUntouched Args:\n{self.rawArgs}")
            print(f"\nCommand:\n{self.command}")
            subsequentDebug = input(f"\n\n{" ":5}Subsequent Debug Arguments\n\n")
            if subsequentDebug:
                # print(f"python3 {self.rawArgs[0]} debug {subsequentDebug}")
                self.system(f"python3 {self.rawArgs[0]} debug {subsequentDebug}")
        elif confirm:
            conf = input(
                f"The command that will be run is:\n\t{self.command}\n\nAre you sure? (Y/n)\n"
            )

            if conf.lower() in "yes":
                self.system(self.command)
            else:
                pass
        else:
            raise Exception(
                'Something went weird. Check "To run, or not to run?" logic.'
            )

    def __str__(self):
        return str(self.sorted)


if __name__ == "__main__":
    FFmpy().run()
