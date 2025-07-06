public class Main {

    public static void main(String args[]) {

        int n = 5; // number of variables (incl. slack variables)
        int m = 3; // number of constraints
        double eps = 1.0e-5;

        double a[][] = {
            {0, -1, 3, 0, 0, 0},
            {2, -1, 1, 1, 0, 0},
            {8, 2, 1, 0, 1, 0},
            {5, 1, 1, 0, 0, 1}
        };

        int basicvar[] = new int[m + 3];

        Simplex.revisedSimplex(true, n, m, a, eps, basicvar);

        if (basicvar[m + 1] > 0) {
            System.out.println("No feasible solution.");
        } else {
            if (basicvar[m + 2] > 0) {
                System.out.println("Objective function is unbounded.");
            } else {
                System.out.println("Optimal solution found.\n\nBasic variable       Value");
                for (int i = 1; i <= m; i++) {
                    System.out.printf("%6d %17.5f\n", basicvar[i], a[i][0]);
                }
                System.out.println("\nOptimal value of the objective function = " + a[0][0]);
            }
        }
    }
}
