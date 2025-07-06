using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;

namespace GeneLib
{
	/// <summary>
	/// Defines the behaviour of a genome
	/// </summary>
	public interface IGenetics<T>
	{
		/// <summary>
		/// The maximum obtainable fitness
		/// </summary>
		double MaxFitness { get; }

		/// <summary>
		/// Create a new empty chromosome
		/// </summary>
		Chromosome<T> Create();

		/// <summary>
		/// Initialize the genes of the chromosome
		/// </summary>
		void Populate(Chromosome<T> chromosome);

		/// <summary>
		/// Evaluate the fitness of a chromosome
		/// </summary>
		double Fitness(Chromosome<T> chromosome);

		/// <summary>
		/// Mutates the genes of chromosome
		/// </summary>
		void Mutate(Chromosome<T> chromosome, double temperature);

		/// <summary>
		/// Mixes the genes of the two chromosomes
		/// </summary>
		void Crossover(Chromosome<T> a, Chromosome<T> b);
	}

	public delegate double FitnessHandler<T>(Chromosome<T> chromosome);
	public delegate void MutationHandler<T>(Chromosome<T> chromosome, double temperatue);
	public delegate void PopulationHandler<T>(Chromosome<T> chromosome);
	public delegate void CrossoverHandler<T>(Chromosome<T> a, Chromosome<T> b);

	public sealed class Genetics<T>(int chromosomeLength) : IGenetics<T>
	{
		public required double MaxFitness { get; set; }
		public required FitnessHandler<T> FitnessHandler { get; set; }
		public PopulationHandler<T>? PopulationHandler { get; set; }
		public MutationHandler<T>? MutationHandler { get; set; }
		public CrossoverHandler<T>? CrossoverHandler { get; set; }

		public Chromosome<T> Create()
		{
			return new Chromosome<T>(chromosomeLength);
		}

		public void Populate(Chromosome<T> chromosome)
		{
			PopulationHandler?.Invoke(chromosome);
		}

		public void Mutate(Chromosome<T> chromosome, double temperature)
		{
			MutationHandler?.Invoke(chromosome, temperature);
		}

		public double Fitness(Chromosome<T> chromosome)
		{
			return FitnessHandler.Invoke(chromosome);
		}

		public void Crossover(Chromosome<T> a, Chromosome<T> b)
		{
			CrossoverHandler?.Invoke(a, b);
		}
	}
}
