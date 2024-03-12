<script>
	import { supabase } from '$lib/supabaseClient'
	/** @type {string} */
	export let classId

	// Import the necessary Svelte features if needed
	let selectedLight = ''

	/**
	 * Function to select a light
	 * @param {string} color - The color of the light
	 */
	function selectLight(color) {
		selectedLight = color
		// Add any actions you want to perform on light selection
		console.log('Selected light:', color)

		// send a message to supabase to add a row to the feedback table
		supabase
			.from('feedback')
			.insert([{ status: 0, user_id: '234', class_id: classId }])
			.then((response) => {
				console.log('Feedback added:', response)
			})

	}
</script>

<div class="traffic-light">
	<button class="light red" on:click={() => selectLight('red')}></button>
	<button class="light yellow" on:click={() => selectLight('yellow')}></button>
	<button class="light green" on:click={() => selectLight('green')}></button>
</div>

<style>
	.traffic-light {
		display: flex;
		flex-direction: column;
		width: 100px;
		background: black;
		padding: 20px;
		border-radius: 20px;
	}

	.light {
		border: none;
		cursor: pointer;
		height: 60px;
		width: 60px;
		border-radius: 50%;
		margin: 10px auto;
		transition: opacity 0.3s ease;
	}

	.red {
		background: #ff0000;
	}

	.yellow {
		background: #ffff00;
	}

	.green {
		background: #00ff00;
	}

	.light:not(:hover) {
		opacity: 0.4;
	}
</style>
