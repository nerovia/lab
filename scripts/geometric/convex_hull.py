def convex_hull(lst):
    # phase 1
    lst.sort(key=lambda it: it[0])
    lst.sort(key=lambda it: it[1])
    a = lst[0]

    # phase 2
    S = lst[1:]
    S.sort(key=lambda p, q: ccw_cmp(a, p, q))
    S.insert(0, a)
    S.append(a)

    # phase 3
    p = 0
    c = 1
    while True: 
        n = c+1
        if (signed_area(S[p], S[c], S[n]) > 0):
            p = c
        else:
            p = p-1
        c = p+1





def ccw_cmp(a, p, q):
    return p if signed_area(a, p, q) > 0 else q



def signed_area(a, b, c):
    return 1;

if __name__ == "__main__":
    convex_hull([ (9, 5), (2, 5), (3, 5), (8, 5)])

    