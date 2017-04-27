#!/usr/bin/python
import os, csv, platform, sys, random, datetime

# Globals
operations = {"multiply" : "x",
              "subtract" : "-",
              "add"      : "+"}
#              "divide"   : "/"}

def error(msg):
    print("ERROR: %s" % msg)
    quit(1)

def readFile(file):
    inputBuffer = ""
    with open(file, "rb") as fileIn:
        fileIn.seek(0, 0)
        for line in fileIn.readlines():
            # Decaode text as LATIN for python 3 support
            inputBuffer += line
    return inputBuffer

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

    # Make sure template is available
    file = "template.svg"
    if not os.path.isfile(file):
        error("Unable to locate template file, '%s'." % file)

    # Read file in
    buffer = readFile(file)

    # Generate 12 problems, modify buffer
    for i in range(1, 13):
        operation = operations.keys()[random.randint(0,len(operations)-1)]
        sign = operations[operation]

        int1, int2, answer = generateProblem(operation, 20)

        # Debug
        if debug == True:
            print("%d %s %d = %d" % (int1, sign, int2, answer))

        output = ""
        for line in buffer.split():
            line = line.replace("$date", datetime.datetime.now().strftime("%m/%d/%y")) if "$date" in line else line
            line = line.replace("$%dT" % i, str(int1)) if "$%dT" % i in line else line 
            line = line.replace("$%dB" % i, str(int2)) if "$%dB" % i in line else line 
            line = line.replace("$%dO" % i, sign) if "$%dO" % i in line else line
            line = line.replace("$%dA" % i, str(answer)) if "$%dA" % i in line else line  
            output += line+"\n"
        buffer = output

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
    main(*sys.argv)
