/**
 * @typedef {import('../types/supabase').Database} Database
 * @typedef {import('../types/supabase').Tables<'feedback'>} FeedbackRow
 * @typedef {import('../types/supabase').TablesInsert<'feedback'>} FeedbackInsert
 */

import { createClient } from '@supabase/supabase-js'
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

/**
 * Creates a Supabase client instance.
 *
 * @param {string} url - The Supabase URL.
 * @param {string} key - The Supabase Anon Key.
 * @returns {import('@supabase/supabase-js').SupabaseClient<Database>}
 */
function createSupabaseClient(url, key) {
	return createClient(url, key)
}

// Assuming process.env.SUPABASE_URL and process.env.SUPABASE_ANON_KEY are defined elsewhere in your environment
export const supabase = createSupabaseClient(supabaseUrl, supabaseAnonKey)

/**
 * @param {FeedbackInsert} row
 * @returns {void}
 * */
export function insertFeedback(row) {
	// send a message to supabase to add a row to the feedback table
	supabase
		.from('feedback')
		.insert([row])
		.then((response) => {
			console.log('Feedback added:', response)
		})
}

/**
 *
 * @param {string | undefined} classId
 * @param {(row: FeedbackInsert) => void} callback
 * @param {string} table
 * @returns
 */
export function subscribeToInsert(classId, callback, table = 'feedback') {
	const channel = supabase
		.channel('table-db-changes')
		.on(
			'postgres_changes',
			{
				event: 'INSERT',
				schema: 'public',
				table: table
			},
			(payload) => {
				if (classId && payload.new.class_id !== classId) return
				console.log('INSERT:', payload)
				callback(payload.new)
				// userStatus[payload.new.user_id] = payload.new.status
				// updateChart()
			}
		)
		.subscribe()
	return channel
}

/**
 * Function to get the initial state of the feedback
 * @param {string} classId - The class ID
 * @param {(rows: FeedbackRow[]) => void} callback - The callback function
 * @param {string} [table='feedback'] - The table to query
 */
export function getRows(classId, callback, table = 'feedback') {
	supabase
		.from(table)
		.select()
		.eq('class_id', classId)
		.then((response) => {
			let rows = response.data ?? []
			console.log(`Initial state of ${classId}: ${rows.length} rows`)
			callback(rows)
		})
}

/**
 * Function to get the initial state of the feedback
 * @param {string} classId - The class ID
 * @param {string} userId - The user ID
 * @param {(status: string) => void} callback - The callback function
 * @param {string} [table='feedback'] - The table to query
 */
export function getLastStatus(classId, userId, callback = () => {}, table = 'feedback') {
	supabase
		.from(table)
		.select('status')
		.eq('class_id', classId)
		.eq('user_id', userId)
		.order('id', { ascending: false })
		.limit(1)
		.then((response) => {
			// console.log(classId, userId, response.data)
			let status = response.data?.[0]?.status ?? ''
			console.log(`Last status of ${userId} in ${classId}: ${status}`)
			callback(status)
		})
}
