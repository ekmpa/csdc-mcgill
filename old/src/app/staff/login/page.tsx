"use client";

import { useState } from "react";
import { signInWithMagicLink } from "@/lib/supabase";

export default function StaffLoginPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");

    const { error: authError } = await signInWithMagicLink(email);
    
    setLoading(false);
    if (authError) {
      setError(`Error: ${authError.message}`);
    } else {
      setMessage("✓ Magic link sent! Check your email and click the link to continue.");
      setEmail("");
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <div className="card">
        <h1 className="text-3xl font-bold text-mcgillRed mb-6 text-center">
          Staff Portal
        </h1>
        
        <form onSubmit={handleSignIn} className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@mcgill.ca"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-mcgillRed"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? "Sending..." : "Sign In with Magic Link"}
          </button>
        </form>
        
        {message && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm">
            {message}
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
          </div>
        )}
        
        <p className="text-center text-sm text-gray-600 mt-6">
          We'll send you a secure link to sign in—no password needed.
        </p>
      </div>
    </div>
  );
}
