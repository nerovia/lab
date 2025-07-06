using GeneLib;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GeneLib.Genetics
{
	public class QueenGenetics(int boardSize) : IGenetics<int>
	{
		public int BoardSize { get; } = boardSize;
		public double MaxFitness { get; } = boardSize * (boardSize - 1) / 2;

		public Chromosome<int> Create()
		{
			return new Chromosome<int>(BoardSize);
		}

		public void Crossover(Chromosome<int> a, Chromosome<int> b)
		{
			var split = Random.Shared.Next(1, BoardSize - 1);
			var swap = new int[split];
			a[..split].CopyTo(swap);
			a[..split] = b[..split];
			b[..split] = swap;
		}

		public double Fitness(Chromosome<int> chromo)
		{
			var sum = MaxFitness;
			for (int i = 0; i < chromo.Length; i++)
			{
				for (int j = i + 1; j < chromo.Length; j++)
				{
					var d = Math.Abs(chromo[i] - chromo[j]);
					if (d == 0 || d == j - i)
						sum--;
				}
			}
			return sum;
		}

		public void Mutate(Chromosome<int> chromo, double temp)
		{
			foreach (ref var gene in chromo[..])
			{
				if (Random.Shared.NextDouble() < temp)
					gene = Random.Shared.Next(BoardSize);
			}
		}

		public void Populate(Chromosome<int> chromo)
		{
			foreach (ref var gene in chromo[..])
				gene = Random.Shared.Next(BoardSize);
		}
	}
}
