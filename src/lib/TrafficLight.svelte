<script>
	import { getUserId } from '$lib'
	import { onMount } from 'svelte'
	import { insertFeedback, getLastStatus } from '$lib/supabaseClient'

	/** @type {string} */
	export let classId

	// Import the necessary Svelte features if needed
	/** @type {string} */
	let selectedLight = ''
	/** @type {string} */
	let userId

	/**
	 * Function to select a light
	 * @param {string} color - The color of the light
	 */
	function selectLight(color) {
		if (selectedLight === color) return
		selectedLight = color
		insertFeedback({ status: color, user_id: userId, class_id: classId })
	}

	onMount(async () => {
		userId = getUserId()
		console.log('hello userId:', userId)
		// Set the light to the last status, or green if no status is found
		getLastStatus(classId, userId, (status) => {
			status ? (selectedLight = status) : selectLight('green')
		})
	})
</script>

<div class="wrapper">
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
	.wrapper {
		display: flex;
		align-items: center;
		height: 95vh; /* Using vh to ensure it takes the full viewport height */
	}
	.traffic-light {
		display: flex;
		flex-direction: column;
		justify-content: center;
		width: calc(100vh * 0.32); /* Adjust width based on viewport size */
		height: calc(100vh * 0.83); /* Height adjusted to maintain aspect ratio */
		background: black;
		margin: 0 auto;
		border-radius: calc(100vmin * 0.02); /* Ensure rounded corners scale */
		box-sizing: border-box; /* Include padding and border in the element's size */
	}

	.light {
		border: none;
		cursor: pointer;
		height: calc(100vh * 0.2); /* Adjust button size based on viewport size */
		width: calc(100vh * 0.2); /* Ensure buttons are circles with equal height and width */
		border-radius: 50%;
		margin: calc(100vh * 0.025) auto; /* Adjust margin based on viewport size */
		transition: opacity 0.3s ease;
	}

	.red {
		background: #e70000;
	}

	.yellow {
		background: #ffff00;
	}

	.green {
		background: #00ff66;
	}
	.light:not(.selected) {
		opacity: 0.2;
	}
	@media (hover: hover) {
		.light:hover {
			opacity: 1;
		}
	}
</style>
