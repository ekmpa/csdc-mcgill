"use client";

import { useEffect, useState } from "react";

type ThemeMode = "default" | "blue" | "formal" | "warm";

const THEMES: Array<{ value: ThemeMode; label: string }> = [
  { value: "default", label: "Default" },
  { value: "blue", label: "Blue" },
  { value: "formal", label: "Formal" },
  { value: "warm", label: "Warm" }
];

const STORAGE_KEY = "csdc-theme";
const COOKIE_KEY = "csdc-theme";

function readThemeFromCookie(): ThemeMode | null {
  if (typeof document === "undefined") {
    return null;
  }

  const match = document.cookie.match(/(?:^|; )csdc-theme=([^;]+)/);
  if (!match) {
    return null;
  }

  const value = decodeURIComponent(match[1]);
  return THEMES.some((theme) => theme.value === value) ? (value as ThemeMode) : null;
}

function applyTheme(nextTheme: ThemeMode) {
  document.documentElement.setAttribute("data-theme", nextTheme);
  document.body.setAttribute("data-theme", nextTheme);
}

export default function ThemeSwitcher() {
  const [theme, setTheme] = useState<ThemeMode>("default");

  useEffect(() => {
    const savedTheme = localStorage.getItem(STORAGE_KEY) as ThemeMode | null;
    const cookieTheme = readThemeFromCookie();
    const currentTheme = (document.documentElement.getAttribute("data-theme") as ThemeMode | null) ?? "default";
    const activeTheme = savedTheme ?? cookieTheme ?? currentTheme;

    setTheme(activeTheme);
    applyTheme(activeTheme);
  }, []);

  const onThemeChange = (nextTheme: ThemeMode) => {
    setTheme(nextTheme);
    applyTheme(nextTheme);

    try {
      localStorage.setItem(STORAGE_KEY, nextTheme);
    } catch {
      // Ignore private mode storage failures and rely on cookie fallback.
    }

    document.cookie = `${COOKIE_KEY}=${encodeURIComponent(nextTheme)}; path=/; max-age=31536000; samesite=lax`;
  };

  return (
    <div className="flex items-center gap-2">
      <label htmlFor="theme-mode" className="text-xs text-gray-300 whitespace-nowrap">
        Theme
      </label>
      <select
        id="theme-mode"
        value={theme}
        onChange={(event) => onThemeChange(event.target.value as ThemeMode)}
        className="rounded-md border border-white/30 bg-white/10 px-2 py-1 text-xs text-white outline-none transition hover:bg-white/20 focus:ring-2 focus:ring-white/40"
        aria-label="Select website theme"
      >
        {THEMES.map((option) => (
          <option key={option.value} value={option.value} className="text-gray-900">
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
