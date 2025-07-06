using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace DivideAndConquer
{
	public interface IDivideAndConquerable<TResult>
	{
		bool IsBasic { get; }

		TResult BaseFun();

		IDivideAndConquerable<TResult>[] Decompose();

		TResult Recombine(TResult[] results);
	}

	public static class DivideAndConquerExtensions
	{
		public static T Solve<T>(this IDivideAndConquerable<T> problem)
		{
			if (problem.IsBasic)
				return problem.BaseFun();
			var subproblems = problem.Decompose();
			var subresults = subproblems.Select(Solve).ToArray();
			var result = problem.Recombine(subresults);
			return result;
		}

		public static async Task<T> SolveAsync<T>(this IDivideAndConquerable<T> problem)
		{
			
			if (problem.IsBasic)
				return problem.BaseFun();

			var subproblems = problem.Decompose().Select(SolveAsync).ToArray();

			var results = await Task.WhenAll(subproblems);  // This should already manage thread count etc.

			return problem.Recombine(results);
		}

		public static T SolveThreaded<T>(this IDivideAndConquerable<T> problem, int maxThreads)
		{
			if (problem.IsBasic)
				return problem.BaseFun();

			var subproblems = problem.Decompose();
			var subresults = new ConcurrentQueue<T>();

			foreach (var subproblem in subproblems)
			{
				if (ThreadPool.ThreadCount < maxThreads)
				{
					ThreadPool.QueueUserWorkItem(state =>
					{
						var subresult = SolveThreaded(subproblem, maxThreads);
						subresults.Enqueue(subresult);
					});
				}
				else
				{
					var subresult = SolveThreaded(subproblem, maxThreads);
					subresults.Enqueue(subresult);
				}
			}

			SpinWait.SpinUntil(() => subresults.Count == subproblems.Length);
			
			return problem.Recombine(subresults.ToArray());
		}
	}
}
