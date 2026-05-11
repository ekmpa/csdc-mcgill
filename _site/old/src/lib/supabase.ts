import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

export const supabase = createClient(supabaseUrl, supabaseKey);

// Helper: fetch visible profiles
export async function getProfiles() {
  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("is_visible", true);
  if (error) console.error(error);
  return data || [];
}

// Helper: fetch published events
export async function getEvents() {
  const { data, error } = await supabase
    .from("events")
    .select("*")
    .eq("is_published", true)
    .order("start_at", { ascending: true });
  if (error) console.error(error);
  return data || [];
}

// Helper: fetch published lab meetings
export async function getLabMeetings() {
  const { data, error } = await supabase
    .from("lab_meetings")
    .select("*")
    .eq("is_published", true)
    .order("meeting_at", { ascending: true });
  if (error) console.error(error);
  return data || [];
}

// Helper: fetch published announcements
export async function getAnnouncements() {
  const { data, error } = await supabase
    .from("announcements")
    .select("*")
    .eq("is_published", true)
    .order("created_at", { ascending: false });
  if (error) console.error(error);
  return data || [];
}

// Auth: Sign in with magic link
export async function signInWithMagicLink(email: string) {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: `${typeof window !== "undefined" ? window.location.origin : ""}/staff/dashboard`,
    },
  });
  return { error };
}

// Auth: Sign out
export async function signOut() {
  return await supabase.auth.signOut();
}

// Auth: Get current session
export async function getSession() {
  const { data, error } = await supabase.auth.getSession();
  return { session: data.session, error };
}

// Auth: Get current user
export async function getCurrentUser() {
  const { data, error } = await supabase.auth.getUser();
  return { user: data.user, error };
}

// Profile: Get current user's profile
export async function getCurrentProfile() {
  const { user } = await getCurrentUser();
  if (!user) return null;

  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", user.id)
    .single();
  if (error) console.error(error);
  return data || null;
}

// Profile: Update own profile
export async function updateProfile(
  updates: Record<string, any>
) {
  const { user } = await getCurrentUser();
  if (!user) return { error: "Not authenticated" };

  const { error } = await supabase
    .from("profiles")
    .update(updates)
    .eq("id", user.id);
  return { error };
}

// Storage: Upload profile image
export async function uploadProfileImage(file: File, userId: string) {
  const filename = `${userId}/${Date.now()}_${file.name}`;
  const { error } = await supabase.storage
    .from("profile-images")
    .upload(filename, file, { upsert: false });
  if (error) {
    console.error(error);
    return { error };
  }

  // Get public URL
  const {
    data: { publicUrl },
  } = supabase.storage.from("profile-images").getPublicUrl(filename);

  return { publicUrl, error: null };
}

// Events: Get all events created by user (drafts + published)
export async function getUserEvents() {
  const { user } = await getCurrentUser();
  if (!user) return [];

  const { data, error } = await supabase
    .from("events")
    .select("*")
    .eq("created_by", user.id)
    .order("start_at", { ascending: true });
  if (error) console.error(error);
  return data || [];
}

// Events: Create event
export async function createEvent(
  event: Record<string, any>
) {
  const { user } = await getCurrentUser();
  if (!user) return { error: "Not authenticated" };

  const { error } = await supabase
    .from("events")
    .insert([{ ...event, created_by: user.id }]);
  return { error };
}

// Events: Update event
export async function updateEvent(
  id: string,
  updates: Record<string, any>
) {
  const { user } = await getCurrentUser();
  if (!user) return { error: "Not authenticated" };

  const { error } = await supabase
    .from("events")
    .update(updates)
    .eq("id", id)
    .eq("created_by", user.id);
  return { error };
}

// Lab Meetings: Get all lab meetings created by user
export async function getUserLabMeetings() {
  const { user } = await getCurrentUser();
  if (!user) return [];

  const { data, error } = await supabase
    .from("lab_meetings")
    .select("*")
    .eq("created_by", user.id)
    .order("meeting_at", { ascending: true });
  if (error) console.error(error);
  return data || [];
}

// Announcements: Get all announcements created by user
export async function getUserAnnouncements() {
  const { user } = await getCurrentUser();
  if (!user) return [];

  const { data, error } = await supabase
    .from("announcements")
    .select("*")
    .eq("created_by", user.id)
    .order("created_at", { ascending: false });
  if (error) console.error(error);
  return data || [];
}
