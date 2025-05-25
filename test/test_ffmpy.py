from ffmpy import FFmpy
from random import randint


def sep_test_junk_gen(
    argsToID: list[str, str],
    *,
    afterOption: str | None = None,
    beforeOption: str | None = None,
    preInsert: list | None = None
):
    junkData = [
        "inputargs",
        "args",
        "options",
        "ohWow",
        "loooooootsOfOptions",
        "maaagickkkk",
        ":3",
        ">:3",
        ":P",
        "ladeedaaaaa",
        "hehehe-youllNeverfindtheInFile",
    ]

    testArgs = []

    if preInsert is not None:
        for ins in preInsert:
            testArgs.append(ins)

    junkCount = randint(5, 25)
    for _ in range(junkCount):
        testArgs.append(junkData[randint(0, (len(junkData) - 1))])

    if afterOption is not None and beforeOption is not None:
        insertIndex = randint(
            (testArgs.index(afterOption) + 2), (testArgs.index(beforeOption) - 1)
        )
    elif afterOption is not None:
        insertIndex = randint((testArgs.index(afterOption) + 2), (len(testArgs) - 1))
    elif beforeOption is not None:
        insertIndex = randint(0, (testArgs.index(beforeOption) - 1))
    else:
        insertIndex = randint(0, (len(testArgs) - 1))

    for a in argsToID:
        testArgs.insert(insertIndex, a)
        insertIndex += 1

    return FFmpy(pytest=testArgs)


def test_pytest_mode():
    testArgs = ["pytesting"]
    ffmpy = FFmpy(pytest=testArgs)

    assert ffmpy.pytest is True
    assert ffmpy.rawArgs == ["pytesting"]


def test_infile_sep():
    assert sep_test_junk_gen(["-i", "inFile"]).inFile == "inFile"


def test_vcodec_sep():
    assert (
        sep_test_junk_gen(
            ["-vcodec", "av1"], preInsert=["-i", "inFile"], afterOption="-i"
        ).outVcodec
        == "av1"
    )
    assert (
        sep_test_junk_gen(
            ["-c:v", "av1"], preInsert=["-i", "inFile"], afterOption="-i"
        ).outVcodec
        == "av1"
    )
    assert (
        sep_test_junk_gen(
            ["-codec:v", "av1"], preInsert=["-i", "inFile"], afterOption="-i"
        ).outVcodec
        == "av1"
    )


def test_vcodec_replace():
    test264 = "-i inFile.mkv -vcodec h264 outFile.mkv"
    ffmpy264 = FFmpy(pytest=test264.split())
    testhevc = "-i inFile.mkv -vcodec hevc outFile.mkv"
    ffmpyhevc = FFmpy(pytest=testhevc.split())

    assert ffmpy264.runArgs[ffmpy264.runArgs.index("-vcodec") + 1] == "h264_videotoolbox"
    assert ffmpyhevc.runArgs[ffmpyhevc.runArgs.index("-vcodec") + 1] == "hevc_videotoolbox"

    test264 = "-i inFile.mkv -c:v h264 outFile.mkv"
    ffmpy264 = FFmpy(pytest=test264.split())
    testhevc = "-i inFile.mkv -c:v hevc outFile.mkv"
    ffmpyhevc = FFmpy(pytest=testhevc.split())

    assert ffmpy264.runArgs[ffmpy264.runArgs.index("-c:v") + 1] == "h264_videotoolbox"
    assert ffmpyhevc.runArgs[ffmpyhevc.runArgs.index("-c:v") + 1] == "hevc_videotoolbox"

    test264 = "-i inFile.mkv -codec:v h264 outFile.mkv"
    ffmpy264 = FFmpy(pytest=test264.split())
    testhevc = "-i inFile.mkv -codec:v hevc outFile.mkv"
    ffmpyhevc = FFmpy(pytest=testhevc.split())

    assert ffmpy264.runArgs[ffmpy264.runArgs.index("-codec:v") + 1] == "h264_videotoolbox"
    assert ffmpyhevc.runArgs[ffmpyhevc.runArgs.index("-codec:v") + 1] == "hevc_videotoolbox"

    testav1 = "-i inFile.mkv -vcodec av1 outFile.mkv"
    ffmpyav1 = FFmpy(pytest=testav1.split())

    assert ffmpyav1.runArgs[ffmpyav1.runArgs.index("-vcodec") + 1] == "av1"


def test_outfile_options_replacer():
    testArgs = "-i inFile.mkv -vcodec h264 outFile.mkv"
    assert (
        FFmpy(pytest=testArgs.split()).command
        == "ffmpeg -i inFile.mkv -vcodec h264_videotoolbox -q:v 65 -tag:v avc1 outFile.mkv"
    )

    testArgs = "-i inFile.mkv -vcodec hevc -q:v 47 outFile.mkv"
    assert (
        FFmpy(pytest=testArgs.split()).command
        == "ffmpeg -i inFile.mkv -vcodec hevc_videotoolbox -q:v 47 -tag:v hvc1 outFile.mkv"
    )

    testArgs = "-i inFile.mkv -vcodec hevc -tag:v hev1 outFile.mkv"
    assert (
        FFmpy(pytest=testArgs.split()).command
        == "ffmpeg -i inFile.mkv -vcodec hevc_videotoolbox -tag:v hev1 -q:v 65 outFile.mkv"
    )

    testArgs = "-i inFile.mkv -vcodec av1 outFile.mkv"
    assert (
        FFmpy(pytest=testArgs.split()).command
        == "ffmpeg -i inFile.mkv -vcodec av1 outFile.mkv"
    )


def test_actual_command_out():
    testArgs = "-i inFile.mkv -vcodec h264 outFile.mkv"
    assert (
        FFmpy(pytest=testArgs.split()).command
        == "ffmpeg -i inFile.mkv -vcodec h264_videotoolbox -q:v 65 -tag:v avc1 outFile.mkv"
    )

    testArgs = "-i inFile.mkv -vcodec av1 outFile.mkv"
    assert (
        FFmpy(pytest=testArgs.split()).command
        == "ffmpeg -i inFile.mkv -vcodec av1 outFile.mkv"
    )
