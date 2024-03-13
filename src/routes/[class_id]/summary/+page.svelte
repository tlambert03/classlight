<script>
	import { page } from '$app/stores'
	import { onMount, onDestroy } from 'svelte'
	import { getRows, subscribeToInsert } from '$lib/supabaseClient'
	import PieChart from '$lib/PieChart.svelte'
	$: chartData = [0, 0, 1]
	const classId = $page.params.class_id

	// map of user_id to status
	// e.g. { 'xxx-xxx': 'green', 'yyy-yyy': 'red' }
	/** @type {Record<string, string | null | undefined >} */
	let userStatus = {}

	const updateChart = () => {
		// Count the number of each status
		/** @type {Record<string, number>} */
		const counts = { green: 0, yellow: 0, red: 0 }
		for (const status of Object.values(userStatus)) {
			if (status && Object.prototype.hasOwnProperty.call(counts, status)) {
				counts[status]++
			}
		}

		// Update the chart data
		console.log('updateChart:', userStatus, counts)
		chartData = [counts.red, counts.yellow, counts.green]
	}

	onMount(() => {
		getRows(classId, (rows) => {
			for (const row of rows) {
				if (!row.user_id) continue
				userStatus[row.user_id] = row.status
			}
			updateChart()
		})

		subscribeToInsert(classId, (new_row) => {
			if (!new_row.user_id) return
			userStatus[new_row.user_id] = new_row.status
			updateChart()
		})
	})

	onDestroy(() => {
		/** Remove all subscriptions when the component is destroyed */
	})
</script>

<main>
	<PieChart {chartData} />
</main>
