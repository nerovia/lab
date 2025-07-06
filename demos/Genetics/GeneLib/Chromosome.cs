namespace GeneLib
{
	public struct Chromosome<T>
	{
		public int Maturity;
		public readonly T[] Genes;

		public Chromosome(T[] genes)
		{
			Maturity = 0;
			Genes = genes;
		}

		public Chromosome(int length) : this(new T[length]) { }

		public int Length { get => Genes.Length; }

		public T this[int index]
		{
			get => Genes[index];
			set => Genes[index] = value;
		}

		public T this[Index index]
		{
			get => Genes[index];
			set => Genes[index] = value;
		}

		public Span<T> this[Range range]
		{
			get => Genes.AsSpan(range);
			set => value.CopyTo(this[range]);
		}

		public Chromosome<T> Clone()
		{
			return new Chromosome<T>((T[])Genes.Clone());
		}

		public override string ToString()
		{
			return $"[{string.Join("-", Genes)}]'{Maturity}";
		}
	}
}
