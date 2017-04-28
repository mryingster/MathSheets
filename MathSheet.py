#!/usr/bin/python
import os, csv, platform, sys, random, datetime, math

# Globals
operations = {"multiply" : "x",
              "subtract" : "-",
              "add"      : "+"}
#              "divide"   : "/"}

def error(msg):
    print("ERROR: %s" % msg)
    quit(1)

def writeSVGFile(outBuffer):
    tempFileName = "tmp.svg"
    with open(tempFileName, 'wb') as output:
        for line in outBuffer:
            output.write(line)
    return tempFileName

def createPDFFile(svgFile):
    # Verify Inkscape is available
    inkscape = "/Volumes/Documents/Applications Less Used/Inkscape.app/Contents/Resources/script"
    if not os.path.isfile(inkscape):
        error("Unable to locate Inkscape")

    # Get current path
    path = os.path.abspath(".")

    # To Do: better naming convention
    pdfFile = "MathSheet.pdf"
        
    import subprocess
    subprocess.call([inkscape, os.path.join(path, svgFile), "--export-pdf=%s" % os.path.join(path, pdfFile), "--without-gui"])
    return pdfFile

def createTextBox(x, y, value, size, rightAlign=False):
    align = "text-align:end;text-anchor:end;" if rightAlign == True else ""

    textObject = """<text
        xml:space="preserve"
        style="font-style:normal;font-weight:normal;font-size:%spx;font-family:sans-serif;fill:#000000;fill-opacity:1;%s"
        x="%s"
        y="%s"><tspan
            sodipodi:role="line"
            x="%s"
            y="%s"
            style="font-size:%spx;%s">%s</tspan></text>
""" % (size, align, x, y, x, y, size, align, value)
    return textObject

def generateSVGProblem(number, int1, int2, operation, x, y):
    fontSize = 20
    pnumber  = createTextBox(x+10,  y,    "%d." % number, fontSize)
    topInt   = createTextBox(x+100, y+10, int1,      fontSize, True)
    botInt   = createTextBox(x+100, y+35, int2,      fontSize, True)
    operand  = createTextBox(x+25,  y+35, operation, fontSize)

    line = """    <path
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       d="m %s,%s 80,0"
       id="path4162-8-0-5"
       inkscape:connector-curvature="0" />
""" % (x+20, y+40)

    rectangle = """    <rect
       style="opacity:1;fill:none;fill-opacity:1;stroke:#808080;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       id="rect4168-2-5-1"
       width="80"
       height="30"
       x="%s"
       y="%s" />
""" % (x+20, y+45)

    problem = "%s\n%s\n%s\n%s\n%s\n%s\n" % (pnumber, topInt, botInt, operand, line, rectangle)
    return problem

def generateSVGAnswer(number, answer, x, y):
    numberText = createTextBox(x + 40, y, "%d." % number, 20, True)
    answerText = createTextBox(x + 50, y, answer, 20)
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
      x="84"
      y="152">
    <tspan
      sodipodi:role="line"
      x="84"
      y="152"
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
      x="85"
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

def generateProblem(operation, limit1 = 20):
    if operation in ["multiply", "divide"]:
        limit1 /= 2

    limit2 = limit1
    int1 = random.randint(0, limit1)

    if operation == "subtract":
        limit2 = int1 - 1

    int2 = random.randint(0, limit2)

    if   operation == "multiply":
        answer = int1 * int2;
    elif operation == "subtract":
        answer = int1 - int2;
    elif operation == "add":
        answer = int1 + int2;
    elif operation == "divide":
        answer = int1
        int1 = answer * int2;

    return int1, int2, answer

def main(argv):
    debug = False
    numberOfProblems = 20

    # Parse Options
    if "-n" in argv:
        try:
            numberOfProblems = int(argv[argv.index("-n") + 1])
        except:
            error("Bad argument value, '-n'.")

    # Figure out spacing
    columns = math.floor(math.sqrt(numberOfProblems))
    colWidthProblem = 670 / columns
    colWidthAnswer = 360 / columns
    rows = math.ceil(numberOfProblems / columns)
    rowHeightProblem = 550 / rows
    rowHeightAnswer = 30

    # Generate SVG rendering of problems
    questions = ""
    answers = ""
    for i in range(numberOfProblems):
        operation = operations.keys()[random.randint(0,len(operations)-1)]
        sign = operations[operation]
        problem = i + 1
        int1, int2, answer = generateProblem(operation, 20)

        # Debug
        if debug == True:
            print("%d %s %d = %d" % (int1, sign, int2, answer))

        x = (i % columns) * colWidthProblem + 80
        y = math.floor(i / columns) * rowHeightProblem + 190

        questions += generateSVGProblem(problem, int1, int2, sign, x, y)

        x = (i % columns) * colWidthAnswer + 80
        y = math.floor(i / columns) * rowHeightAnswer + 875

        answers += generateSVGAnswer(problem, answer, x, y)

    answerBlock = generateSVGAnswerBlock(numberOfProblems, answers)
    buffer = generateSVGDocument(datetime.datetime.now().strftime("%m/%d/%y"), questions, answerBlock)

    # Write SVG File (tmp)
    svgFile = writeSVGFile(buffer)

    # Create PDF using Inkscape
    if not createPDFFile(svgFile):
        error("Unable to create PDF File.")

    # Delete SVG File
    try:
        os.remove(svgFile)
    except:
        error("Unable to remove temporary SVG file.")


if __name__ == "__main__":
    main(sys.argv)
