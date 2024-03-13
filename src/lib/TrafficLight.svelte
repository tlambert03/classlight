<script>
	import { supabase, getUserId } from '$lib'
	import { onMount } from 'svelte'

	/** @type {string} */
	export let classId

	// Import the necessary Svelte features if needed
	/** @type {string} */
	let selectedLight = 'green'
	/** @type {string} */
	let userId

	/**
	 * Function to select a light
	 * @param {string} color - The color of the light
	 */
	function selectLight(color) {
		if (selectedLight === color) return
		selectedLight = color

		// send a message to supabase to add a row to the feedback table
		supabase
			.from('feedback')
			.insert([{ status: color, user_id: userId, class_id: classId }])
			.then((response) => {
				console.log('Feedback added:', response)
			})
	}

	onMount(async () => {
		userId = getUserId()
	})
</script>

<div class="box">
	<div class="traffic-light">
		<button
			class="light red {selectedLight === 'red' ? 'selected' : ''}"
			on:click={() => selectLight('red')}
		></button>
		<button
			class="light yellow {selectedLight === 'yellow' ? 'selected' : ''}"
			on:click={() => selectLight('yellow')}
		></button>
		<button
			class="light green {selectedLight === 'green' ? 'selected' : ''}"
			on:click={() => selectLight('green')}
		></button>
	</div>
</div>

<style>
	.box {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}
	.traffic-light {
		display: flex;
		flex-direction: column;
		width: 45vw;
		background: black;
		padding: 10vw 5vw;
		margin: 0 auto;
		border-radius: 20px;
	}

	.light {
		border: none;
		cursor: pointer;
		height: 35vw;
		width: 35vw;
		border-radius: 50%;
		margin: 5vw auto;
		transition: opacity 0.3s ease;
	}

	.red {
		background: #e70000;
	}

	.yellow {
		background: #ffff00;
	}

	.green {
		background: #36ffab;
	}

	.light:not(:hover).light:not(.selected) {
		opacity: 0.3;
	}
</style>
