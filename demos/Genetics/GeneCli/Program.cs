
using GeneLib;
using System.Runtime.InteropServices;

const int SIZE = 16;

var genetics = new GeneLib.Genetics.QueenGenetics(SIZE);
var evolution = new Evolution<int>(genetics)
{
	EliteThreshold = 0.1,
	Temperature = 0.2,
};
var population = evolution.CreatePopulation(128);

Console.CursorVisible = false;
while (evolution.Evolve(population) < genetics.MaxFitness)
{
	
	if (population.Age % 100 == 0)
	{
		Console.SetCursorPosition(0, 0);
		//ShowPop(population);
		Console.WriteLine(population.Age);
		Console.WriteLine($"{population.TopFitness:N2}/{genetics.MaxFitness} {population.TopChromosome}            ");
		ShowBoard(population.TopChromosome);
		//Console.ReadLine();

		Thread.Sleep(TimeSpan.FromSeconds(0.1));
	}
}
ShowPop(population);
ShowBoard(population.TopChromosome);

void ShowPop<T>(Population<T> pop)
{
	Console.WriteLine();
	Console.WriteLine($"Generation: {pop.Age}");
	Console.WriteLine();

	var table = new ConsoleTables.ConsoleTable("Fitness", "Chromosome");
	foreach (var (fit, chrom) in pop)
		table.AddRow(fit.ToString("N2"), chrom);
	table.Write(ConsoleTables.Format.Minimal);
}

void ShowBoard(Chromosome<int> chrom)
{
	for (int i = 0; i < SIZE; i++)
	{
		for (int j = 0; j < SIZE; j++)
			Console.Write(chrom[i] == j ? "& " : ". ");
		Console.WriteLine();
	}
}

double Deteriation(double age, double halflife)
{
	//return 1.0;
	return age > halflife ? 0.5 : 1.0;
	return Math.Exp(-0.693147 / halflife * age);
}
