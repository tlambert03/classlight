// place files you want to import through the `$lib` alias in this folder.

// re-export supabase from the supabaseClient file
export { supabase } from './supabaseClient'

/** @type {() => string} */
export function uuidv4() {
	return '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, (c) =>
		// @ts-ignore
		(c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
	)
}

/** @type {() => string} */
export function getUserId() {
	let userId = localStorage.getItem('userId')
	if (!userId) {
		userId = uuidv4()
		localStorage.setItem('userId', userId)
	}
	return userId
}
