<script>
	import Chart from 'chart.js/auto'

	/** @type {number[]} */
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

<canvas use:makeChart={chartData} width="400" height="200" />
