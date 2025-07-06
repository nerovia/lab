using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DivideAndConquer
{
	internal class MinMax<T>(T[] items) : IDivideAndConquerable<(T, T)> where T : IComparable<T>
	{
		public bool IsBasic => items.Length <= 3;

		public (T, T) BaseFun()
		{
			return (items.Min()!, items.Max()!);
		}

		public IDivideAndConquerable<(T, T)>[] Decompose()
		{
			var m = items.Length / 2;
			return new MinMax<T>[] { new(items[..m]), new(items[m..]) };
		}

		public (T, T) Recombine((T, T)[] results)
		{
			return (results.Min(it => it.Item1)!, results.Max(it => it.Item2)!);
		}
	}
}
