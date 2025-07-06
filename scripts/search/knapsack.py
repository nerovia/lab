def pack(ws, vs, rem_w):
    # rem_w: remaining volume 
    # ws: weight vector
    # vs: value vector
    return pack_rec(ws, vs, rem_w, sum(vs), 0, 0, [])

def pack_rec(ws, vs, rem_w, pot_v, acc_v, k, lst):
    # pot_v: potential value
    # acc_v: accumulated value
    # lst: combinations of items
    # n: the number of items
    # k: next item to consider 

    max_v = acc_v
    max_lst = lst

    print(lst, acc_v, pot_v)
    
    for i in range(k, len(ws)):

        if rem_w < ws[i]:
            pot_v -= vs[i]
            print(lst + [i], 'full, skipping')
            continue

        if pot_v < acc_v:
            pot_v -= vs[i]
            print('pruned!')
            break
        
        (l, v) = pack_rec(ws, vs, rem_w - ws[i], pot_v, acc_v + vs[i], i+1, lst + [i])

        if max_v < v:
            max_v = v
            max_lst = l
    
    return (max_lst, max_v)

if __name__ == "__main__":

    ws = [3, 6, 9, 5]
    vs = [7, 2, 10, 4]

    print("solution:", pack(ws, vs, 15))