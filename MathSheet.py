#!/usr/bin/python
import os, csv, platform, sys, random, datetime, math

# Globals
operations = {"multiply" : "x",
              "subtract" : "-",
              "add"      : "+",
              "divide"   : "/"}

def error(msg):
    print("ERROR: %s" % msg)
    quit(1)

def help():
    #     0         10        20        30        40        50        60        70        80
    #     |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    print("Math Sheet")
    print("")
    print("Description")
    print("    This utility creates random math problem with answers in a printable PDF")
    print("    document.")
    print("")
    print("Usage")
    print("    ./MathSheet.py <options>")
    print("")
    print("Options")
    print("    -h        Show this help page")
    print("    -n <num>  Specify number of problems to put on the sheet of paper")
    print("    -m <num>  Specify the maximum size of integers used")
    print("    -o <name> Specify cusomt output filename (default is MathSheet.pdf)")
    print("    -v        Increase verbosity")
    print("    -add      Create addition problems")
    print("    -sub      Create subtraction problems")
    print("    -mul      Create multiplication problems")
    print("    -div      Create division problems")
    print("")

def writeSVGFile(outBuffer):
    tempFileName = "tmp.svg"
    with open(tempFileName, 'wb') as output:
        for line in outBuffer:
            output.write(line)
    return tempFileName

def findInkscape():
    inkscapeScriptPath = ""
    inkscapePath = ""

    # Default Location(s)
    checkPaths = ["/Applications",
                  "/Volumes/Documents/Applications Less Used"]

    # Check in default locations for application
    for path in checkPaths:
        checkPath = os.path.join(path, "Inkscape.app")
        if os.path.isdir(checkPath):
            inkscapePath = checkPath
            break

    # If not found...
    if inkscapePath == "":
        error("Unable to locate Inkscape application")

    # Look for scripting engine
    scriptPath = "Contents/Resources/script"
    inkscapeScriptPath = os.path.join(inkscapePath, scriptPath)
    if not os.path.isfile(inkscapeScriptPath):
        error("Unable to locate Inkscape Scripting Binary")

    return inkscapeScriptPath

def createPDFFile(svgFile, pdfFile):
    inkscape = findInkscape()

    # Get current path
    path = os.path.abspath(".")

    import subprocess
    subprocess.call([inkscape, os.path.join(path, svgFile), "--export-pdf=%s" % os.path.join(path, pdfFile), "--without-gui"])
    return pdfFile

def createTextBox(x, y, value, size, color="#000000", rightAlign=False):
    align = "text-align:end;text-anchor:end;" if rightAlign == True else ""

    textObject = """<text
        xml:space="preserve"
        style="font-style:normal;font-weight:normal;font-size:%spx;font-family:sans-serif;fill:%s;fill-opacity:1;%s"
        x="%s"
        y="%s"><tspan
            sodipodi:role="line"
            x="%s"
            y="%s"
            style="font-size:%spx;%s">%s</tspan></text>
""" % (size, color, align, x, y, x, y, size, align, value)
    return textObject

def generateSVGProblem(number, int1, int2, operation, x, y):
    fontSize = 20
    pnumber  = createTextBox(x,    y,    "%d." % number, fontSize, "#808080")
    topInt   = createTextBox(x+75, y+10, int1,           fontSize, "#000000", True)
    botInt   = createTextBox(x+75, y+35, int2,           fontSize, "#000000", True)
    operand  = createTextBox(x+5,  y+35, operation,      fontSize, "#000000")

    line = """    <path
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       d="m %s,%s 80,0"
       id="path4162-8-0-5"
       inkscape:connector-curvature="0" />
""" % (x, y+40)

    rectangle = """    <rect
       style="opacity:1;fill:none;fill-opacity:1;stroke:#808080;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       id="rect4168-2-5-1"
       width="80"
       height="30"
       x="%s"
       y="%s" />
""" % (x, y+45)

    problem = "%s\n%s\n%s\n%s\n%s\n%s\n" % (pnumber, topInt, botInt, operand, line, rectangle)
    return problem

def generateSVGAnswer(number, answer, x, y):
    numberText = createTextBox(x + 40, y, "%d." % number, 20, "#808080", True)
    answerText = createTextBox(x + 50, y, answer, 20, "#000000")
    return "%s\n%s" % (numberText, answerText)

def generateSVGDocument(date, content, answers):
    document = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="8.5in"
   height="11in"
   viewBox="0 0 765 990"
   id="svg2"
   version="1.1"
   inkscape:version="0.91 r13725"
   sodipodi:docname="test.svg">
  <defs
     id="defs4" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="1.4"
     inkscape:cx="315.41704"
     inkscape:cy="258.71292"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     units="in"
     inkscape:window-width="1920"
     inkscape:window-height="1148"
     inkscape:window-x="-8"
     inkscape:window-y="-8"
     inkscape:window-maximized="1"/>
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(0,-62.362205)">

    <text
      xml:space="preserve"
      style="font-style:normal;font-weight:normal;font-size:40px;line-height:125%;font-family:sans-serif;fill:#000000;fill-opacity:1;"
      x="80"
      y="150">
    <tspan
      sodipodi:role="line"
      x="80"
      y="150"
      style="font-size:17.5px">Date: """+date+"""</tspan>
    </text>

"""+content+"""
"""+answers+"""

  </g>
</svg>"""

    return document

def generateSVGAnswerBlock(numberOfProblems, answers):
    return """    <path
      style="fill:none;fill-rule:evenodd;stroke:#808080;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:8, 8;stroke-dashoffset:0;stroke-opacity:1"
      d="m -0.7,773 767,0"
      id="path4401"
      inkscape:connector-curvature="0" />

    <text
      xml:space="preserve"
      style="font-style:normal;font-weight:normal;font-size:40px;line-height:125%;font-family:sans-serif;fill:#000000;fill-opacity:1"
      x="85"
      y="840">
    <tspan
      sodipodi:role="line"
      id="tspan4283"
      x="80"
      y="840"
      style="font-size:20px">Answers</tspan>
    </text>

"""+answers+"""

    <rect
      style="opacity:1;fill:none;fill-opacity:1;stroke:#808080;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
      width="155"
      height="135"
      x="540"
      y="850" />

    <text
      xml:space="preserve"
      style="font-style:normal;font-weight:normal;font-size:40px;font-family:sans-serif;fill:#000000;fill-opacity:1"
      x="590"
      y="960">
    <tspan
      sodipodi:role="line"
      id="tspan4420"
      x="590"
      y="960">"""+str(numberOfProblems)+"""</tspan>
    </text>

    <path
      style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
      d="m 567.8571,913.79078 101.42857,0"
      id="path4422"
      inkscape:connector-curvature="0" />"""

def generateProblem(operation, limit = 20, simple = True):
    int1 = random.randint(1, limit)
    int2 = random.randint(0, int1)

    if   operation == "multiply":
        int1 %= 13
        int2 %= 6
        answer = int1 * int2;

    elif operation == "subtract":
        # Keeps from requiring carrying
        if simple == True:
            str1 = str(int1)
            str2 = str(int2)
            str3 = ""
            for i in reversed(range(1, len(str2)+1)):
                if str1[-1 * i] == "0":
                    str3 = "0"
                else:
                    str3 += str(int(str2[-1 * i]) % (int(str1[-1 * i]) + 1))
        int2 = int(str3)
        answer = int1 - int2;

    elif operation == "add":
        answer = int1 + int2;

    elif operation == "divide":
        answer = int1
        int1 = answer * int2;

    return int1, int2, answer

def main(argv):
    verbose = False
    numberOfProblems = 16
    numberLimit = 20
    selectedOperations = []
    outputFilename = ""

    # Parse Options (Skip first argument)
    index = 1
    while index < len(argv):
        arg = argv[index]
        if arg == "-h":
            help()
            quit()
        elif arg == "-n":
            try:
                index += 1
                numberOfProblems = int(argv[index])
            except:
                error("Bad argument value, \"-n\".")
        elif arg == "-m":
            try:
                index += 1
                numberLimit = int(argv[index])
            except:
                error("Bad argument value, \"-m\".")
        elif arg == "-o":
            try:
                index += 1
                outputFilename = argv[index]
            except:
                error("Bad argument value, \"-o\".")
        elif arg == "-add":
            selectedOperations.append("add")
        elif arg == "-sub":
            selectedOperations.append("subtract")
        elif arg == "-mul":
            selectedOperations.append("multiply")
        elif arg == "-div":
            selectedOperations.append("divide")
        elif arg == "-v":
            verbose = True
        else:
            error("Unrecognized argument, \"%s\"" % arg)
        index += 1

    # Make sure operations are selected
    if len(selectedOperations) == 0:
        selectedOperations = operations.keys()

    # Figure out spacing
    columns = math.floor(math.sqrt(numberOfProblems))
    colWidthProblem = 670 / columns
    colWidthAnswer = 450 / columns
    rows = math.ceil(numberOfProblems / columns)
    rowHeightProblem = 550 / rows
    rowHeightAnswer = 30

    # Generate SVG rendering of problems
    questions = ""
    answers = ""
    for i in range(numberOfProblems):
        operation = selectedOperations[random.randint(0,len(selectedOperations)-1)]
        sign = operations[operation]
        problem = i + 1
        int1, int2, answer = generateProblem(operation, numberLimit)

        # Print resulting problems
        if verbose == True:
            print("%d %s %d = %d" % (int1, sign, int2, answer))

        x = (i % columns) * colWidthProblem + 80
        y = math.floor(i / columns) * rowHeightProblem + 190

        questions += generateSVGProblem(problem, int1, int2, sign, x, y)

        x = (i % columns) * colWidthAnswer + 80
        y = math.floor(i / columns) * rowHeightAnswer + 875

        answers += generateSVGAnswer(problem, answer, x, y)

    # Create SVG Buffer
    answerBlock = generateSVGAnswerBlock(numberOfProblems, answers)
    svgBuffer = generateSVGDocument(datetime.datetime.now().strftime("%m/%d/%y"), questions, answerBlock)

    # Write SVG File (tmp)
    svgFile = writeSVGFile(svgBuffer)
    if verbose == True: print("SVG File, \"%s\", generated." % svgFile)

    # Create PDF name if none specified using -o option
    if outputFilename == "":
        operationString = '_'.join(i[:3] for i in selectedOperations)
        creationDate = datetime.datetime.now().strftime("%m-%d-%y")
        outputFilename = "MathSheet_%s_%s.pdf" % (creationDate, operationString)

    # Create PDF using Inkscape
    if not createPDFFile(svgFile, outputFilename):
        error("Unable to create PDF File.")
    if verbose == True: print("PDF File, \"%s\", generated." % outputFilename)

    # Delete SVG File
    try:
        os.remove(svgFile)
        if verbose == True: print("SVG File, \"%s\", deleted." % svgFile)
    except:
        error("Unable to remove temporary SVG file.")

if __name__ == "__main__":
    main(sys.argv)
