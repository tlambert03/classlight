<script>
	export let data
</script>

<h1>Class</h1>

<ul>
	{JSON.stringify(data)}
	{#each data.feedback as row}
		<li>{row.class_id}, {row.user_id} {row.status} {row.created_at}</li>
	{/each}
</ul>
