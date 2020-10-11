import matplotlib.pyplot, matplotlib.font_manager
import sys
import ast

try:
    matplotlib.pyplot.rcParams['font.family'] = ['SimHei']
except:
    matplotlib.pyplot.rcParams['font.family'] = ['Times New Roman']
def draw(data, f):
    this = []
    for i in data:
        if i[0] == f:
            this = i[1:]
    print(this)
    x = range(1, len(this) + 1)
    matplotlib.pyplot.plot(x, this, label=f)
    matplotlib.pyplot.suptitle(f)
    matplotlib.pyplot.xticks(range(1, len(this) + 1))
    matplotlib.pyplot.title("By ScoreLib")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()


def draw2(data: list):
    this = []
    for i in data:
        this = i[1:]
        x = range(1, len(this) + 1)
        matplotlib.pyplot.plot(x, this, label=i[0])
    print(this)
    matplotlib.pyplot.xticks(range(1,len(this)+1))
    matplotlib.pyplot.title("By ScoreLib")
    matplotlib.pyplot.suptitle("Students")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()


try:
    if sys.argv[2] == 'a':
        draw2(ast.literal_eval(sys.argv[1]))
        exit(0)
    if sys.argv[3] == 'd':
        draw(ast.literal_eval(sys.argv[1]), sys.argv[2])
        exit(0)

except IndexError:
    print("Error")
