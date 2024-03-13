<script>
	/** @type {import('./$types').PageData} */
	export let data

	import { onMount, onDestroy } from 'svelte'
	import { supabase } from '$lib/supabaseClient'
	import PieChart from '$lib/PieChart.svelte'
	$: chartdata = [10, 20, 30]

	// Create a variable to store the user's status
	// this is a map of user_id to status
	// e.g. { '234': 'green', '235': 'red' }
	/** @type {Record<string, ('red'|'green'|'yellow')>} */
	let userStatus = {}

	const updateChart = () => {
		// Count the number of each status
		const counts = { green: 0, yellow: 0, red: 0 }
		for (const status of Object.values(userStatus)) {
			counts[status]++
		}
		// Update the chart data
		chartdata = [counts.red, counts.yellow, counts.green]
	}

	const handleFeedback = (payload) => {
		console.log('Change received!', payload.new)
		userStatus[payload.new.user_id] = payload.new.status
		updateChart()
	}

	onMount(() => {
		for (const row of data.feedback) {
			userStatus[row.user_id] = row.status
		}
		updateChart()
		const channel = supabase
			.channel('table-db-changes')
			.on(
				'postgres_changes',
				{
					event: '*',
					schema: 'public',
					table: 'feedback'
				},
				handleFeedback
			)
			.subscribe()
	})

	onDestroy(() => {
		/** Remove all subscriptions when the component is destroyed */
	})
</script>

<main>
	<PieChart {chartdata} />
</main>
