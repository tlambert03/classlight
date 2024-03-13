<script>
	import TrafficLight from '$lib/TrafficLight.svelte'
	import { page } from '$app/stores'
</script>

<main>
	<TrafficLight classId={$page.params.class_id} />
</main>
