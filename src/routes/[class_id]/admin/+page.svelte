<script>
	import { onMount, onDestroy } from 'svelte'
	import { writable } from 'svelte/store'
	import { supabase } from '$lib/supabaseClient'

	onMount(() => {
		console.log('Mounted')
		const channel = supabase
			.channel('table-db-changes')
			.on(
				'postgres_changes',
				{
					event: '*',
					schema: 'public',
					table: 'feedback'
				},
				(payload) => console.log(payload)
			)
			.subscribe()
	})

	onDestroy(() => {
		/** Remove all subscriptions when the component is destroyed */
	})
</script>
