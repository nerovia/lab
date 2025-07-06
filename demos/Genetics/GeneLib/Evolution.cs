using GeneLib;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Transactions;

namespace GeneLib
{
	public sealed class Evolution<T>(IGenetics<T> genetics)
	{
		public double EliteThreshold { get; set; } = 0.0;
		public double PurgeThreshold { get; set; } = 0.0;
		public double Temperature { get; set; } = 0.4;

		void Evaluate(Population<T> population)
		{
			for (int i = 0; i < population.Chromosomes.Length; i++)
				population.Fitness[i] = genetics.Fitness(population.Chromosomes[i]);
			Array.Sort(population.Fitness, population.Chromosomes);
		}

		public Population<T> CreatePopulation(int size)
		{
			var population = new Population<T>(size);
			for (int i = 0; i < population.Chromosomes.Length; i++)
			{
				population.Chromosomes[i] = genetics.Create();
				genetics.Populate(population.Chromosomes[i]);
			}
			Evaluate(population);
			return population;
		}

		public double Evolve(Population<T> population)
		{
			// Convert fittness into distribution
			double tot = population.Fitness.Sum();
			double acc = 0.0;
			for (int i = 0; i < population.Fitness.Length; i++)
			{
				acc += population.Fitness[i] / tot;
				population.Fitness[i] = acc;
			}

			// Create Selection
			var selection = new Chromosome<T>[population.Chromosomes.Length];

			// Select Elite
			var elite = (int)Math.Floor(EliteThreshold * selection.Length);
			for (int i = 1; i <= elite; i++)
			{
				selection[i - 1] = population.Chromosomes[^i];
				selection[i - 1].Maturity++;
			}

			// Select Rest
			for (int i = elite; i < selection.Length; i++)
			{
			RETRY:
				var r = Random.Shared.NextDouble();
				for (int j = 0; j < population.Chromosomes.Length; j++)
				{
					if (r < population.Fitness[j])
					{
						// Exclude self replication
						//if (i == j)
						//{
						//	Console.WriteLine("DING!");
						//	goto RETRY;
						//}
						selection[i] = population.Chromosomes[j].Clone();
						break;
					}
				}
			}

			// Crossover
			// Console.WriteLine("Crossover: ");
			// Console.WriteLine();
			for (int i = elite + 1; i < selection.Length; i += 2)
			{
				var a = selection[i - 1];
				var b = selection[i];
				a.Maturity = b.Maturity = (a.Maturity + b.Maturity) / 2;
				// Console.Write($"{a} x {b} ~~> ");
				genetics.Crossover(a, b);
				// Console.WriteLine($"{a}, {b}");
			}
			// Console.WriteLine();

			// Mutation
			//Console.WriteLine($"Mutating: {temp}°");
			// Console.WriteLine();

			for (int i = elite; i < selection.Length; i++)
			{
				//Console.Write($"{chrom} ~~> ");
				genetics.Mutate(selection[i], Temperature);
				//Console.WriteLine(chrom);
			}

			Array.Copy(selection, population.Chromosomes, selection.Length);
			Evaluate(population);
			population.Age++;
			population.Increase = population.Fitness.Sum() - tot;

			return population.Fitness[^1];
		}
	}
}

public class Population<T>(int size) : IEnumerable<(double fitness, Chromosome<T> chromosome)>
{
	public int Age { get; internal set; }
	internal double Increase;
	internal readonly Chromosome<T>[] Chromosomes = new Chromosome<T>[size];
	internal readonly double[] Fitness = new double[size];

	public Chromosome<T> TopChromosome { get => Chromosomes[^1]; }
	public double TopFitness { get => Fitness[^1]; }

	public IEnumerator<(double, Chromosome<T>)> GetEnumerator()
	{
		return Fitness.Zip(Chromosomes).GetEnumerator();
	}

	IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
