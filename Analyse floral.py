w1=1
w2=1
b=-1.5

def fct_activation(x):
    if(x>=0):
        return 1
    else:
        return 0

def perceptron(x1, x2):
    s = x1*w1+x2*w2+b
    return fct_activation(s)

print(perceptron(1, 2))