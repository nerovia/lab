import java.lang.Math.*;

public class Simplex extends Object {

    public static void revisedSimplex(boolean maximize, int n, int m,
                                      double a[][], double epsilon, int basicvar[]) {
        int i, j, k, m2, p, idx = 0;
        double objcoeff[] = new double[n + 1];
        double varsum[] = new double[n + 1];
        double optbasicval[] = new double[m + 3];
        double aux[] = new double[m + 3];
        double work[][] = new double[m + 3][m + 3];
        double part, sum;
        boolean infeasible, unbound, abort, out, iterate;

        if (maximize) {
            for (j = 1; j <= n; j++) {
                a[0][j] = -a[0][j];
            }
        }

        infeasible = false;
        unbound = false;
        m2 = m + 2;
        p = m + 2;
        out = true;
        k = m + 1;

        for (j = 1; j <= n; j++) {
            objcoeff[j] = a[0][j];
            sum = 0.0;
            for (i = 1; i <= m; i++) {
                sum -= a[i][j];
            }
            varsum[j] = sum;
        }

        sum = 0.0;
        for (i = 1; i <= m; i++) {
            basicvar[i] = n + i;
            optbasicval[i] = a[i][0];
            sum -= a[i][0];
        }

        optbasicval[k] = 0.0;
        optbasicval[m2] = sum;

        for (i = 1; i <= m2; i++) {
            for (j = 1; j <= m2; j++) {
                work[i][j] = 0.0;
            }
            work[i][i] = 1.0;
        }

        iterate = true;
        do {
            // Phase 1
            if ((optbasicval[m2] >= -epsilon) && out) {
                out = false;
                p = m + 1;
            }
            part = 0.0;

            // Phase 2
            for (j = 1; j <= n; j++) {
                sum = work[p][m + 1] * objcoeff[j] + work[p][m + 2] * varsum[j];
                for (i = 1; i <= m; i++) {
                    sum += work[p][i] * a[i][j];
                }
                if (part > sum) {
                    part = sum;
                    k = j;
                }
            }

            if (part > -epsilon) {
                iterate = false;
                if (out) {
                    infeasible = true;
                } else {
                    a[0][0] = -optbasicval[p];
                }
            } else {
                for (i = 1; i <= p; i++) {
                    sum = work[i][m + 1] * objcoeff[k] + work[i][m + 2] * varsum[k];
                    for (j = 1; j <= m; j++) {
                        sum += work[i][j] * a[j][k];
                    }
                    aux[i] = sum;
                }

                abort = true;
                for (i = 1; i <= m; i++) {
                    if (aux[i] >= epsilon) {
                        sum = optbasicval[i] / aux[i];
                        if (abort || (sum < part)) {
                            part = sum;
                            idx = i;
                        }
                        abort = false;
                    }
                }

                if (abort) {
                    unbound = true;
                    iterate = false;
                } else {
                    basicvar[idx] = k;
                    sum = 1.0 / aux[idx];
                    for (j = 1; j <= m; j++) {
                        work[idx][j] *= sum;
                    }
                    i = (idx == 1) ? 2 : 1;
                    do {
                        sum = aux[i];
                        optbasicval[i] -= part * sum;
                        for (j = 1; j <= m; j++) {
                            work[i][j] -= work[idx][j] * sum;
                        }
                        i += (i == idx - 1) ? 2 : 1;
                    } while (i <= p);
                    optbasicval[idx] = part;
                }
            }
        } while (iterate);

        // Return results
        basicvar[m + 1] = (infeasible ? 1 : 0);
        basicvar[m + 2] = (unbound ? 1 : 0);

        for (i = 1; i <= m; i++) {
            a[i][0] = optbasicval[i];
        }

        if (maximize) {
            for (j = 1; j <= n; j++) {
                a[0][j] = -a[0][j];
            }
            a[0][0] = -a[0][0];
        }
    }
}
