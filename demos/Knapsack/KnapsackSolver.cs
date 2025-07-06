namespace Knapsack;

/// <summary>
/// Represents an item with a value and weight.
/// </summary>
/// <param name="Value">The value of the item.</param>
/// <param name="Weight">The weight of the item.</param>
record KnapsackItem(double Value, double Weight)
{
	public override string ToString()
	{
		return $"({Value}, {Weight})";
	}
}

/// <summary>
/// Represents a node in the configuration tree.
/// </summary>
record KnapsackConfig
{
	/// <summary>
	/// The preceding configuration.
	/// </summary>
	public required KnapsackConfig? Parent { get; init; }

	/// <summary>
	/// The index (item) that is considered in this configuration.
	/// </summary>
	public required int ConsideredIndex { get; init; }

	/// <summary>
	/// The accumulated value of this configuration branch.
	/// </summary>
	public required double AccumulatedValue { get; init; }

	/// <summary>
	/// The potential value for descendants of this configuration.
	/// </summary>
	public required double PotentialValues { get; init; }

	/// <summary>
	/// The accumulated remaining capacity of this configuration branch.
	/// </summary>
	public required double RemainingCapacity { get; init; }

	/// <summary>
	/// Collects the considered indices over this configuration branch.
	/// </summary>
	/// <returns>The collection of indices</returns>
	public IEnumerable<int> Collect()
	{
		KnapsackConfig? current = this;
		while (current.Parent != null)
		{
			yield return current.ConsideredIndex;
			current = current.Parent;
		}
	}

	public override string ToString()
	{
		return $"[{string.Join(',', Collect())}] {AccumulatedValue}/{PotentialValues} {RemainingCapacity}";
	}

	public string ToColorString()
	{
		return $"[{string.Join(',', Collect())}] \x1b[33m{AccumulatedValue}/{PotentialValues} \x1b[32m+{RemainingCapacity}\x1b[0m";
	}
}

class KnapsackSolver
{
	public event KnapsackVisitedHandler? Visited;

	public event KnapsackPrunedHandler? Pruned;

	/// <summary>
	/// Finds a solution to the provided Knapsack Problem.
	/// </summary>
	/// <param name="items">The items to consider.</param>
	/// <param name="capacity">The capacity of the knapsack.</param>
	/// <returns>A configuration branch with maximized value.</returns>
	public KnapsackConfig Solve(KnapsackItem[] items, double capacity)
	{
		return Recurse(items, new() {
			Parent = null,
			ConsideredIndex = -1,
			AccumulatedValue = 0,
			PotentialValues = items.Sum(it => it.Value),
			RemainingCapacity = capacity
		});
	}

	private KnapsackConfig Recurse(KnapsackItem[] items, KnapsackConfig current, int depth = 0)
	{
		KnapsackConfig max = current;
		double pot = current.PotentialValues;

		Visited?.Invoke(depth, current);

		for (int i = current.ConsideredIndex + 1; i < items.Length; ++i)
		{
			var item = items[i];

			if (current.RemainingCapacity < item.Weight)
			{
				pot -= item.Value;
				continue;
			}

			if (pot < max.AccumulatedValue)
			{
				Pruned?.Invoke(depth, i);
				break;
			}

			var res = Recurse(items, new() {
				Parent = current,
				ConsideredIndex = i,
				PotentialValues = pot,
				AccumulatedValue = current.AccumulatedValue + item.Value,
				RemainingCapacity = current.RemainingCapacity - item.Weight
			}, depth + 1);

			if (max.AccumulatedValue < res.AccumulatedValue)
				max = res;

			// the item will no longer be considered
			pot -= item.Value;
		}

		return max;
	}
}

delegate void KnapsackVisitedHandler(int depth, KnapsackConfig config);

delegate void KnapsackPrunedHandler(int depth, int i);
