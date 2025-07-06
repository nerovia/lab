def lcs_length(s: str, t: str) -> list[list[int]]:     # Θ(1)-space
                                                       #
    n = len(s)                                         # Θ(1)-space   Θ(1)-time   
    m = len(t)                                         # Θ(1)-space   Θ(1)-time
                                                       #
    A = [[0 for _ in range(m+1)] for _ in range(n+1)]  # Θ(nm)-space  Θ(nm)-time
                                                       #
    for i in range(1, n+1):                            # Θ(1)-space   Θ(n)-time
        for j in range(1, m+1):                        # Θ(1)-space   Θ(m)-time
            if s[i-1] == t[j-1]:                       #              Θ(1)-time
                A[i][j] = A[i-1][j-1] + 1              #              Θ(1)-time
            else:                                      #
                A[i][j] = max(A[i-1][j], A[i][j-1])    #              Θ(1)-time
                                                       #
    return A                                           #              Θ(1)-time

def lcs(s: str, t: str) -> str:
    
    A = lcs_length(s, t)
    i = len(s)
    j = len(t)
    r = ''
    
    path = []

    while i > 0 and j > 0:
        if s[i-1] == t[j-1]:
            path.append((i, j, 'match'))
            r = s[i-1] + r
            i -= 1
            j -= 1
        elif A[i-1][j] < A[i][j-1]:
            path.append((i, j, 'visit'))
            j -= 1
        else:
            path.append((i, j, 'visit'))
            i -= 1

    return r, path


if __name__ == '__main__':
    s = 'cgataattgaga'
    t = 'gttcctaata'
    A = lcs_length(s, t)
    r, path = lcs(s, t)

    n = len(s)
    m = len(t)

    # for y in range(-1, m+1):
    #     print(t[y-1] if y > 0 else ' ', end=' & ')
    # print('\\\\')

    for i in range(0, n+1):
        for j in range(0, m+1):
            a = A[i][j]
            end = ' & ' if j < m else ' '
            if (i, j, 'match') in path:
                print('\\textcolor{green}{', a, '}', sep='', end=end)
            elif (i, j, 'visit') in path:
                print('\\textcolor{red}{', a, '}', sep='', end=end)
            else:
                print(f'{a}', end=end)
        print('\\\\')

    # for i in range(0, n+1):
    #     for j in range(0, m+1):
    #         if (i, j, 'match') in path:
    #             print('\033[32m', end='')
    #         elif (i, j, 'visit') in path:
    #             print('\033[31m', end='')
    #         else:
    #             print('\033[39m', end='')
    #         print(A[i][j], end=' ')
    #     print()
    # print(lcs(s, t))

