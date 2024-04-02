<script>
	import Chart from 'chart.js/auto'

	/** @type {number[]} 
	 * array of counts of each status [red, yellow, green]
	*/
	export let chartData

	const red = 'rgb(240, 0, 40)'
	const yellow = 'rgb(255, 255, 86)'
	const green = 'rgb(30, 192, 150)'

	/**
	 * @param {HTMLCanvasElement} ctx
	 * @param {number[]} data
	 * @returns {{ update: (u: number[]) => void, destroy: () => void }}
	 */
	function makeChart(ctx, data) {
		// Create a new chart
		const myChart = new Chart(ctx, {
			type: 'pie',
			data: { datasets: [{ data, backgroundColor: [red, yellow, green] }] },
			options: {}
		})
		// Return the chart object
		return {
			update(u) {
				myChart.data.datasets[0].data = u
				myChart.update()
			},
			destroy() {
				myChart.destroy()
			}
		}
	}
</script>

<div class="counter">
	{ chartData.reduce((a, b) => a + b, 0) }
</div>
<canvas use:makeChart={chartData} width="400" height="200" />

<style>
	.counter {
		font-size: 2em;
		font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
		text-align: center;
		position: absolute;
		top: 40px;
		left: 40px;
	}
</style>