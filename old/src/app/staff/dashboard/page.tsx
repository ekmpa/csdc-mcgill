"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  getCurrentUser,
  getCurrentProfile,
  updateProfile,
  uploadProfileImage,
  signOut,
  getUserEvents,
} from "@/lib/supabase";

export default function StaffDashboard() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("profile");
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  // Form state
  const [formData, setFormData] = useState({
    full_name: "",
    title: "",
    bio: "",
    email_public: "",
    website_url: "",
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        const { user: currentUser } = await getCurrentUser();
        if (!currentUser) {
          router.push("/staff/login");
          return;
        }

        setUser(currentUser);

        const currentProfile = await getCurrentProfile();
        setProfile(currentProfile);

        if (currentProfile) {
          setFormData({
            full_name: currentProfile.full_name || "",
            title: currentProfile.title || "",
            bio: currentProfile.bio || "",
            email_public: currentProfile.email_public || "",
            website_url: currentProfile.website_url || "",
          });
        }

        if (activeTab === "events") {
          const userEvents = await getUserEvents();
          setEvents(userEvents);
        }
      } catch (err) {
        console.error("Error loading dashboard:", err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [router, activeTab]);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleProfileSave = async () => {
    setSaving(true);
    setMessage("");
    const { error } = await updateProfile(formData);
    setSaving(false);

    if (error) {
      setMessage(`Error: ${error.message || error}`);
    } else {
      setMessage("✓ Profile updated successfully!");
      const updated = await getCurrentProfile();
      setProfile(updated);
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !user) return;

    setSaving(true);
    const { publicUrl, error } = await uploadProfileImage(file, user.id);
    setSaving(false);

    if (error) {
      setMessage(`Upload error: ${error.message || error}`);
    } else {
      // Update profile with new image URL
      await updateProfile({ photo_url: publicUrl });
      setMessage("✓ Photo updated!");
      const updated = await getCurrentProfile();
      setProfile(updated);
    }
  };

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-16 text-center">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-16">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-mcgillRed">Staff Dashboard</h1>
        <button
          onClick={handleSignOut}
          className="btn-secondary"
        >
          Sign Out
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 mb-8 border-b-2 border-gray-200">
        <button
          onClick={() => setActiveTab("profile")}
          className={`px-4 py-2 font-semibold border-b-2 transition ${
            activeTab === "profile"
              ? "border-mcgillRed text-mcgillRed"
              : "border-transparent text-gray-600 hover:text-gray-900"
          }`}
        >
          My Profile
        </button>
        <button
          onClick={() => setActiveTab("events")}
          className={`px-4 py-2 font-semibold border-b-2 transition ${
            activeTab === "events"
              ? "border-mcgillRed text-mcgillRed"
              : "border-transparent text-gray-600 hover:text-gray-900"
          }`}
        >
          Manage Events
        </button>
      </div>

      {/* Content */}
      {activeTab === "profile" && (
        <div className="card max-w-2xl">
          <h2 className="text-2xl font-bold text-mcgillRed mb-6">Edit Your Profile</h2>

          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Full Name
              </label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-mcgillRed"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Title / Role
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-mcgillRed"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Bio
              </label>
              <textarea
                name="bio"
                value={formData.bio}
                onChange={handleInputChange}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-mcgillRed"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email (Public)
              </label>
              <input
                type="email"
                name="email_public"
                value={formData.email_public}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-mcgillRed"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Website / Portfolio
              </label>
              <input
                type="url"
                name="website_url"
                value={formData.website_url}
                onChange={handleInputChange}
                placeholder="https://..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-mcgillRed"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Profile Photo
              </label>
              {profile?.photo_url && (
                <div className="mb-3">
                  <img
                    src={profile.photo_url}
                    alt={profile.full_name}
                    className="w-24 h-24 rounded-lg object-cover"
                  />
                </div>
              )}
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                disabled={saving}
                className="w-full"
              />
            </div>
          </div>

          {message && (
            <div
              className={`mb-4 p-3 rounded-lg text-sm ${
                message.startsWith("✓")
                  ? "bg-green-50 border border-green-200 text-green-800"
                  : "bg-red-50 border border-red-200 text-red-800"
              }`}
            >
              {message}
            </div>
          )}

          <button
            onClick={handleProfileSave}
            disabled={saving}
            className="btn-primary"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      )}

      {activeTab === "events" && (
        <div className="card max-w-4xl">
          <h2 className="text-2xl font-bold text-mcgillRed mb-6">Your Events</h2>

          {events.length === 0 ? (
            <p className="text-gray-600">No events yet. Create one to get started.</p>
          ) : (
            <div className="space-y-4">
              {events.map((event) => (
                <div
                  key={event.id}
                  className="bg-gray-50 border border-gray-200 rounded-lg p-4"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-gray-900">{event.title}</h3>
                      <p className="text-gray-600 text-sm">
                        {new Date(event.start_at).toLocaleDateString()}
                      </p>
                    </div>
                    <span
                      className={`text-xs font-semibold px-2 py-1 rounded ${
                        event.is_published
                          ? "bg-green-100 text-green-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {event.is_published ? "Published" : "Draft"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          <button className="btn-primary mt-6">+ Create New Event</button>
        </div>
      )}
    </div>
  );
}
