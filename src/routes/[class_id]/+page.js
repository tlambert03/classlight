import { supabase } from '$lib/supabaseClient'

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
	const classId = params.class_id
	const { data } = await supabase.from('feedback').select().eq('class_id', classId)
	return {
		feedback: data ?? []
	}
}
