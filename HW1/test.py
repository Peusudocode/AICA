s = "3[a2[c]]"
res, num = '', 0
stack = []
for c in s:
    if c.isdigit():
        num = num * 10 + int(c)
        print(num)
    elif c == '[':
        stack.append(res)
        stack.append(num)
        res = ''
        print(stack)
        num = 0
    elif c == ']':
        snum = stack.pop()
        print(snum)
        sstr = stack.pop()
        print(sstr)
        print(res)
        res = sstr + snum * res
    else:
        res += c
print(res)