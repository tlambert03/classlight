<script>
	import TrafficLight from '$lib/TrafficLight.svelte'
	import { page } from '$app/stores'
</script>

<h1>Class</h1>

<TrafficLight classId={$page.params.class_id} />
