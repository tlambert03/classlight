/**
 * @typedef {import('../types/supabase').Database} Database
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
