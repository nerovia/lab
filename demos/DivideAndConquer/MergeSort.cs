using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DivideAndConquer
{
	public class MergeSort<T>(T[] items) : IDivideAndConquerable<T[]> where T : IComparable<T>
	{
		public bool IsBasic => items.Length < 2;

		public T[] BaseFun() => items;

		public IDivideAndConquerable<T[]>[] Decompose()
		{
			var m = items.Length / 2;
			return new MergeSort<T>[] { new(items[..m]), new(items[m..]) };
		}

		public T[] Recombine(T[][] results)
		{
			T[] a = results[0];
			T[] b = results[1];
			
			int i = 0;
			int j = 0;
			int k = 0;

			while (i < a.Length && j < b.Length) 
			{
				if (a[i].CompareTo(b[j]) < 0)
					items[k++] = a[i++];
				else
					items[k++] = b[j++];
			}

			while (i < a.Length)
				items[k++] = a[i++];

			while (j < b.Length)
				items[k++] = b[j++];

			return items;
		}
	}
}
