import adapter from '@sveltejs/adapter-static'

// https://kit.svelte.dev/docs/adapter-static#github-pages
/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		paths: {
			base: process.argv.includes('dev') ? '' : process.env.BASE_PATH
		}
	}
}

export default config
