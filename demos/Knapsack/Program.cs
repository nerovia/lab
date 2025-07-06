using System.CommandLine;

namespace Knapsack;

public class Program : RootCommand
{
	public readonly Argument<int> Capacity;
	public readonly Argument<int> Count;
	public readonly Option<double[]> Values;
	public readonly Option<double[]> Weights;
	public readonly Option<bool> Verbose;
	public readonly Option<int?> Seed;

	public readonly Command Pack;
	public readonly Command Rand;

	public static int Main(string[] args) => new Program().Invoke(args);

	public Program()
	{
		Capacity = new Argument<int>("capacity", "Capacity of the knapsack");
		Count = new Argument<int>("count", "Number of items");
		Values = new Option<double[]>("--values", "Value vector") 
		{ 
			IsRequired = true,
			AllowMultipleArgumentsPerToken = true,
		};
		Weights = new Option<double[]>("--weights", "Weight vector")
		{
			IsRequired = true,
			AllowMultipleArgumentsPerToken = true
		};
		Verbose = new Option<bool>(["--verbose", "-v"], "Verbose Output");
		Seed = new Option<int?>(["--seed", "-s"], "Randomizer Seed");

		Pack = new Command("pack", "Packs the given items");
		Rand = new Command("rand", "Packs random items");

		Pack.AddArgument(Capacity);
		Pack.AddOption(Values);
		Pack.AddOption(Weights);
		Pack.AddOption(Verbose);
		Pack.SetHandler(HandlePack, Capacity, Values, Weights, Verbose);

		Rand.AddArgument(Capacity);
		Rand.AddArgument(Count);
		Rand.AddOption(Seed);
		Rand.AddOption(Verbose);
		Rand.SetHandler(HandleRand, Capacity, Count, Seed, Verbose);

		AddCommand(Pack);
		AddCommand(Rand);
		this.SetHandler(() => Handle([new(7, 3), new(2, 6), new(10, 9), new(4, 5)], 15, true));
	}

	private void HandleRand(int capacity, int count, int? seed, bool verbose)
	{
		Console.WriteLine();
		Random random = seed.HasValue ? new Random(seed.Value) : new();
		KnapsackItem[] items = Enumerable.Range(0, count)
			.Select(it => new KnapsackItem(random.Next(1, capacity * 10), random.Next(1, capacity / 2)))
			.ToArray();
		Handle(items, capacity, verbose);
	}

	private void HandlePack(int capacity, double[] values, double[] weigths, bool verbose)
	{
		KnapsackItem[] items = values.Zip(weigths)
			.Select((it) => new KnapsackItem(it.First, it.Second))
			.ToArray();
		Handle(items, capacity, verbose);
	}

	private void Handle(KnapsackItem[] items, double capacity, bool verbose)
	{
		Console.ResetColor();
		Console.WriteLine($"ITEMS: [{string.Join(",", (object[])items)}]");
		KnapsackSolver solver = new();
		if (verbose)
		{
			Console.WriteLine();
			solver.Visited += (depth, config) => Printer.Print(config.ToColorString(), depth);
			solver.Pruned += (depth, i) => Printer.Print("\x1b[3mPRUNED!", depth, ConsoleColor.Red);
		}
		var sol = solver.Solve(items, capacity);
		Console.WriteLine();
		Console.Write($"KNAPSACK: {sol.ToColorString()}");
	}
}

class Printer
{
	public static void Print(object o, int indent = 0, ConsoleColor color = ConsoleColor.Gray)
	{
		Console.ForegroundColor = color;
		if (indent > 0)
			Console.Write(new string(' ', indent * 2));
		Console.Write("> ");
		Console.WriteLine(o);
		Console.ResetColor();
	}
}