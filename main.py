def main(test=False):
    import os
    from sys import path
    from menu import Menu

    programDir = path[0]
    tempDir = f"{programDir}/temp"
    os.system(f"mkdir {tempDir}")

    os.system(f'ffmpeg -hide_banner -encoders > "{tempDir}/encoders.txt"')
    os.system(
        f'ffmpeg -hide_banner -encoders | grep "^\\ V" > "{tempDir}/encodersVideo.txt"'
    )
    os.system(
        f'ffmpeg -hide_banner -encoders | grep "^\\ A" > "{tempDir}/encodersAudio.txt"'
    )

    os.system(f'ffmpeg -hide_banner -decoders > "{tempDir}/decoders.txt"')
    os.system(
        f'ffmpeg -hide_banner -decoders | grep "^\\ V" > "{tempDir}/decodersVideo.txt"'
    )
    os.system(
        f'ffmpeg -hide_banner -decoders | grep "^\\ A" > "{tempDir}/decodersAudio.txt"'
    )

    compileErr = ""
    menuMain = Menu("root")

    inFile: str | None = None
    outFile: str | None = None
    outVcodec: str | None = None
    outAcodec: str | None = None
    globalSettings = [].copy()
    inSettings = [].copy()
    outSettings = [].copy()

    menuInFile = Menu("inFile")
    menuOutFile = Menu("outFile")
    menuSettingsOut = Menu("settingsOutput")
    menuVcodecSet = Menu("vcodecSet")
    menuAcodecSet = Menu("acodecSet")
    menuCustomSettings = Menu("customSet")

    while True:
        selection = menuMain.prompt(input_note=compileErr)
        compileErr = ""
        if selection == "inFile":
            inFileInput = menuInFile.prompt(
                input_note=f"Selected: {inFile}\n",
                err_msg=f"invalid input\nSelected: {inFile}\n",
            )
            if inFileInput != "":
                inFile = inFileInput

        elif selection == "outFile":
            outFileInput = menuOutFile.prompt(
                input_note=f"Selected: {outFile}\n",
                err_msg=f"invalid input\nSelected: {outFile}\n",
            )
            if outFileInput != "":
                outFile = outFileInput

        elif selection == "settingsOutput":
            while True:
                selection = menuSettingsOut.prompt()
                if selection == "vcodec":
                    outVcodecInput = menuVcodecSet.prompt(
                        input_note=f"Selected: {outVcodec}\n",
                        err_msg=f"invalid input\nSelected: {outVcodec}\n",
                    )
                    if outVcodecInput != "":
                        outVcodec = outVcodecInput

                elif selection == "acodec":
                    outAcodecInput = menuAcodecSet.prompt(
                        input_note=f"Selected: {outAcodec}\n",
                        err_msg=f"invalid input\nSelected: {outAcodec}\n",
                    )
                    if outAcodecInput != "":
                        outAcodec = outAcodecInput

                elif selection == "custom":
                    customInput = menuCustomSettings.prompt()
                    if customInput != "":
                        outSettings.append(customInput)

                elif selection == "reset":
                    outAcodec = None
                    outVcodec = None
                    outSettings = [].copy()
                    break

                elif selection == "exit":
                    selection = None
                    break

        elif selection == "compile":
            if inFile is None:
                compileErr = "No input file given.\n"
            elif outFile is None:
                compileErr = "No output file given.\n"
            else:
                print(inFile, outFile, outVcodec, outAcodec, sep="\n")

                if outVcodec:
                    outSettings.append(f"-c:v {outVcodec}")
                if outAcodec:
                    outSettings.append(f"-c:a {outAcodec}")

                runArgs = [].copy()
                for opt in globalSettings:
                    runArgs.append(opt)
                for opt in inSettings:
                    runArgs.append(opt)
                if inFile:
                    runArgs.append("-i")
                    runArgs.append(inFile)
                for opt in outSettings:
                    runArgs.append(opt)
                runArgs.append(outFile)

                command = f"ffmpeg {" ".join(runArgs)}"
                break

    os.system(f"rm -r {tempDir}")

    if test:
        os.system(f"echo {command}")
        return command

    os.system(f"echo {command}")
    # os.system(command)

    return command


if __name__ == "__main__":
    try:
        import os
        from sys import path

        programDir = path[0]
        tempDir = f"{programDir}/temp"
        main()
    except KeyboardInterrupt:
        os.system(f"rm -r {tempDir}")
