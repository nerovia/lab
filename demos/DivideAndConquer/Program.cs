// See https://aka.ms/new-console-template for more information
using DivideAndConquer;
using System.Diagnostics;
using System.Diagnostics.Metrics;
using System.Threading.Tasks;

byte[] items = new byte[100_000_000];

Random.Shared.NextBytes(items);

var problem = new MergeSort<byte>(items);

var watch = new Stopwatch();
watch.Start();
var result = problem.SolveThreaded(10);
watch.Stop();
Console.WriteLine(string.Join(", ", result.Take(10)));
Console.WriteLine($"in {watch}");
