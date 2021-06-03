import matplotlib.pyplot as plt

def property_1_time():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [0.31, 0.60, 1.25, 3.82, 6.82]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI CS points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [1.89, 9.46, 22.00, 72.93, 250.55]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [0.19, 0.35, 1.28, 4.42, 17.32]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [0.03, 0.05, 0.15, 0.52, 1.96]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Time in seconds')
    # giving a title to my graph
    plt.title('Property 1 - Time')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()

def property_2_time():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [0.17, 0.30, 0.61, 1.20, 2.47]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [0.37, 0.83, 2.88, 7.98, 10.65]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [0.25, 0.41, 1.19, 4.32, 18.73]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [0.02, 0.04, 0.14, 0.52, 1.98]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Time in seconds')
    # giving a title to my graph
    plt.title('Property 2 - Time')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()


def property_3_time():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [0.19, 0.36, 0.82, 1.69, 3.58]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [1.20, 3.89, 13.06, 61.25, 385.18]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [0.24, 0.44, 1.29, 4.78, 19.82]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [0.02, 0.05, 0.15, 0.54, 2.12]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Time in seconds')
    # giving a title to my graph
    plt.title('Property 3 - Time')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()


def property_4_time():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [0.18, 0.32, 0.72, 1.30, 2.74]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [0.51, 1.49, 4.74, 17.31, 54.80]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [0.20, 0.39, 1.23, 4.86, 18.29]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [0.02, 0.05, 0.15, 0.54, 2.16]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Time in seconds')
    # giving a title to my graph
    plt.title('Property 4 - Time')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()


def property_1_memory():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [51.74, 52.48, 54.56, 58.94, 86.47]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [51.86, 52.43, 54.19, 78.02, 90.50]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [140.41, 164.09, 395.83, 365.73, 385.23]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [11.03, 11.48, 12.70, 15.15, 19.85]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Memory in MB')
    # giving a title to my graph
    plt.title('Property 1 - Memory')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()

def property_2_memory():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [51.76, 52.27, 54.34, 57.06, 64.27]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [51.71, 52.65, 54.35, 57.30, 63.39]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [147.85, 196.26, 352.84, 392.45, 662.18]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [11.00, 11.48, 12.75, 15.12, 19.89]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Memory in KB')
    # giving a title to my graph
    plt.title('Property 2 - Memory')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()


def property_3_memory():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [51.82, 52.48, 54.35, 57.09, 66.90]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [51.69, 52.62, 54.30, 59.08, 86.24]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [142.16, 191.50, 332.99, 391.98, 562.61]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [11.05, 11.49, 12.77, 15.18, 19.91]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Memory in KB')
    # giving a title to my graph
    plt.title('Property 3 - Memory')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()


def property_4_memory():
    # MonaAmI CB points
    x0 = [1000, 2000, 4000, 8000, 16000]
    y0 = [51.70, 52.25, 53.88, 57.09, 65.87]
    # plotting MonAmI points
    plt.plot(x0, y0, label="MonAmI CB")

    # MonaAmI points
    x1 = [1000, 2000, 4000, 8000, 16000]
    y1 = [51.85, 52.55, 53.91, 57.21, 64.79]
    # plotting MonAmI points
    plt.plot(x1, y1, label="MonAmI CS")

    # nfer scala points
    x2 = [1000, 2000, 4000, 8000, 16000]
    y2 = [150.56, 199.01, 402.66, 361.00, 531.94]
    # plotting MonAmI points
    plt.plot(x2, y2, label="nfer Scala")

    # nfer C points
    x3 = [1000, 2000, 4000, 8000, 16000]
    y3 = [11.10, 11.63, 13.01, 15.67, 21.08]
    # plotting MonAmI points
    plt.plot(x3, y3, label="nfer C")

    # naming the x axis
    plt.xlabel('Trace size')
    # naming the y axis
    plt.ylabel('Memory in KB')
    # giving a title to my graph
    plt.title('Property 4 - Memory')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()

if __name__ == '__main__':
    property_1_time()
    property_2_time()
    property_3_time()
    property_4_time()
    property_1_memory()
    property_2_memory()
    property_3_memory()
    property_4_memory()

